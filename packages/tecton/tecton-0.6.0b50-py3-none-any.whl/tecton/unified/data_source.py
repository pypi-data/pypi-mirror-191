from __future__ import annotations

import datetime
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import attrs
from pyspark.sql import dataframe as pyspark_dataframe
from pyspark.sql import streaming as pyspark_streaming
from typeguard import typechecked

from tecton import conf
from tecton import types
from tecton._internals import display
from tecton._internals import errors
from tecton._internals import fco as internal_fco
from tecton._internals import metadata_service
from tecton._internals import sdk_decorators
from tecton._internals import type_utils
from tecton.declarative import base as declarative_base
from tecton.declarative import data_source as declarative_data_source
from tecton.interactive import data_frame
from tecton.interactive import snowflake_api
from tecton.interactive import spark_api
from tecton.unified import common as unified_common
from tecton.unified import utils as unified_utils
from tecton.unified import validations_api
from tecton_core import id_helper
from tecton_core import specs
from tecton_proto.args import basic_info_pb2
from tecton_proto.args import fco_args_pb2
from tecton_proto.args import virtual_data_source_pb2 as virtual_data_source__args_pb2
from tecton_proto.common import data_source_type_pb2
from tecton_proto.common import fco_locator_pb2
from tecton_proto.common import framework_version_pb2
from tecton_proto.common import schema_container_pb2
from tecton_proto.metadataservice import metadata_service_pb2
from tecton_proto.validation import validator_pb2
from tecton_spark import spark_schema_wrapper

BatchConfigType = Union[
    declarative_data_source.FileConfig,
    declarative_data_source.HiveConfig,
    declarative_data_source.RedshiftConfig,
    declarative_data_source.SnowflakeConfig,
    declarative_data_source.SparkBatchConfig,
]

StreamConfigType = Union[
    declarative_data_source.KinesisConfig,
    declarative_data_source.KafkaConfig,
    declarative_data_source.SparkStreamConfig,
]


@attrs.define(eq=False)
class DataSource(unified_common.BaseTectonObject, declarative_base.BaseDataSource):
    """Base class for Data Source classes.

    Attributes:
        _spec: A data source spec, i.e. a dataclass representation of the Tecton object that is used in most functional
            use cases, e.g. constructing queries. Set only after the object has been validated. Remote objects, i.e.
            applied objects fetched from the backend, are assumed valid.
        _args: A Tecton "args" proto. Only set if this object was defined locally, i.e. this object was not applied
            and fetched from the Tecton backend.
        _args_supplement: A supplement to the _args proto that is needed to create the Data Source spec.
    """

    _spec: Optional[specs.DataSourceSpec] = attrs.field(repr=False)
    _args: Optional[virtual_data_source__args_pb2.VirtualDataSourceArgs] = attrs.field(
        repr=False, on_setattr=attrs.setters.frozen
    )
    _args_supplement: Optional[specs.DataSourceSpecArgsSupplement] = attrs.field(
        repr=False, on_setattr=attrs.setters.frozen
    )

    @unified_utils.requires_local_object
    def _build_args(self) -> fco_args_pb2.FcoArgs:
        return fco_args_pb2.FcoArgs(virtual_data_source=self._args)

    def _build_fco_validation_args(self) -> validator_pb2.FcoValidationArgs:
        if self.info._is_local_object:
            return validator_pb2.FcoValidationArgs(
                virtual_data_source=validator_pb2.VirtualDataSourceValidationArgs(
                    args=self._args,
                    batch_schema=self._args_supplement.batch_schema,
                    stream_schema=self._args_supplement.stream_schema,
                )
            )
        else:
            return validator_pb2.FcoValidationArgs(virtual_data_source=self._spec.data_proto.validation_args)

    @property
    def _is_valid(self) -> bool:
        return self._spec is not None

    def _validate(self, indentation_level: int = 0) -> None:
        if self._is_valid:
            return

        try:
            self._derive_schemas(indentation_level)
        except Exception as e:
            # TODO(jake): Chain the schema derivation error with a better validation error.
            print(f"{self.__class__.__name__} '{self.name}' has failed to derive schema for validation.")
            raise e

        validations_api.run_backend_validation_and_assert_valid(
            self,
            validator_pb2.ValidationRequest(validation_args=[self._build_fco_validation_args()]),
            indentation_level,
        )

        self._spec = specs.DataSourceSpec.from_args_proto(self._args, self._args_supplement)

    @unified_utils.requires_local_object
    def _create_unvalidated_spec(self, mock_data: pyspark_dataframe.DataFrame) -> specs.DataSourceSpec:
        """Create an unvalidated spec. Used for user unit testing, where backend validation is unavailable."""
        schema = spark_schema_wrapper.SparkSchemaWrapper.from_spark_schema(mock_data.schema)
        # Use the mock schema as both the batch and stream schema because StreamSource specs expect a non-nil stream
        # schema.
        supplement = specs.DataSourceSpecArgsSupplement(batch_schema=schema, stream_schema=schema)
        return specs.DataSourceSpec.from_args_proto(self._args, supplement)

    def _derive_schemas(self, indentation_level: int) -> None:
        raise NotImplementedError

    @sdk_decorators.sdk_public_method
    @unified_utils.requires_remote_object
    def summary(self) -> display.Displayable:
        """Displays a human readable summary of this Data Source."""
        request = metadata_service_pb2.GetVirtualDataSourceSummaryRequest(
            fco_locator=fco_locator_pb2.FcoLocator(id=self._spec.id_proto, workspace=self._spec.workspace)
        )
        response = metadata_service.instance().GetVirtualDataSourceSummary(request)
        return display.Displayable.from_fco_summary(response.fco_summary)

    @sdk_decorators.sdk_public_method
    @unified_utils.requires_validation
    def get_dataframe(
        self,
        start_time: Optional[datetime.datetime] = None,
        end_time: Optional[datetime.datetime] = None,
        *,
        apply_translator: bool = True,
    ) -> data_frame.TectonDataFrame:
        if self._spec.type == data_source_type_pb2.DataSourceType.PUSH_NO_BATCH:
            raise errors.DATA_SOURCE_HAS_NO_BATCH_CONFIG(self.name)
        if conf.get_bool("ALPHA_SNOWFLAKE_COMPUTE_ENABLED"):
            return snowflake_api.get_dataframe_for_data_source(self._spec, start_time, end_time)
        else:
            return spark_api.get_dataframe_for_data_source(self._spec, start_time, end_time, apply_translator)

    @property
    def data_source_type(self) -> data_source_type_pb2.DataSourceType.ValueType:
        if self._spec is not None:
            return self._spec.type
        else:
            return self._args.type

    @property
    def data_delay(self) -> Optional[datetime.timedelta]:
        if self._spec is not None:
            return self._spec.batch_source.data_delay

        # This args data delay utility is needed so that feature view args can be constructed from unvalidated
        # data sources objects.
        if self._args.HasField("hive_ds_config"):
            return self._args.hive_ds_config.common_args.data_delay.ToTimedelta()
        elif self._args.HasField("spark_batch_config"):
            return self._args.spark_batch_config.data_delay.ToTimedelta()
        elif self._args.HasField("redshift_ds_config"):
            return self._args.redshift_ds_config.common_args.data_delay.ToTimedelta()
        elif self._args.HasField("snowflake_ds_config"):
            return self._args.snowflake_ds_config.common_args.data_delay.ToTimedelta()
        elif self._args.HasField("file_ds_config"):
            return self._args.file_ds_config.common_args.data_delay.ToTimedelta()
        elif self._args.type == data_source_type_pb2.DataSourceType.PUSH_NO_BATCH:
            return None
        else:
            raise ValueError(f"Invalid batch source args: {self._args}")


@attrs.define
class BatchSource(DataSource):
    @typechecked
    def __init__(
        self,
        *,
        name: str,
        description: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None,
        owner: Optional[str] = None,
        prevent_destroy: bool = False,
        batch_config: BatchConfigType,
    ):
        from tecton.cli import common as cli_common

        ds_args = virtual_data_source__args_pb2.VirtualDataSourceArgs(
            virtual_data_source_id=id_helper.IdHelper.generate_id(),
            info=basic_info_pb2.BasicInfo(name=name, description=description, tags=tags, owner=owner),
            version=framework_version_pb2.FrameworkVersion.FWV5,
            type=data_source_type_pb2.DataSourceType.BATCH,
            prevent_destroy=prevent_destroy,
        )
        batch_config._merge_batch_args(ds_args)

        info = unified_common.TectonObjectInfo.from_args_proto(ds_args.info, ds_args.virtual_data_source_id)
        source_info = cli_common.construct_fco_source_info(ds_args.virtual_data_source_id)

        self.__attrs_init__(
            info=info,
            spec=None,
            args=ds_args,
            source_info=source_info,
            args_supplement=_build_args_supplement(batch_config, None),
        )

        internal_fco.Fco._register(self)

    @classmethod
    @typechecked
    def _from_spec(cls, spec: specs.DataSourceSpec) -> "BatchSource":
        """Create a BatchSource from directly from a spec. Specs are assumed valid and will not be re-validated."""
        info = unified_common.TectonObjectInfo.from_spec(spec)
        obj = cls.__new__(cls)  # Instantiate the object. Does not call init.
        obj.__attrs_init__(
            info=info,
            spec=spec,
            args=None,
            source_info=None,
            args_supplement=None,
        )
        return obj

    def _derive_schemas(self, indentation_level: int) -> None:
        validations_api.print_deriving_schemas(self, indentation_level)
        if conf.get_bool("ALPHA_SNOWFLAKE_COMPUTE_ENABLED"):
            self._args_supplement.batch_schema = snowflake_api.derive_batch_schema(self._args)
        else:
            self._args_supplement.batch_schema = spark_api.derive_batch_schema(
                self._args, self._args_supplement.batch_post_processor, self._args_supplement.batch_data_source_function
            )

    @sdk_decorators.sdk_public_method
    @unified_utils.requires_validation
    def get_columns(self) -> List[str]:
        """Returns the column names of the data source's schema."""
        schema = self._spec.batch_source.spark_schema
        return [field.name for field in schema.fields]


@attrs.define
class StreamSource(DataSource):
    @typechecked
    def __init__(
        self,
        *,
        name: str,
        description: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None,
        owner: Optional[str] = None,
        prevent_destroy: bool = False,
        batch_config: BatchConfigType,
        stream_config: StreamConfigType,
    ):
        from tecton.cli import common as cli_common

        ds_args = virtual_data_source__args_pb2.VirtualDataSourceArgs(
            virtual_data_source_id=id_helper.IdHelper.generate_id(),
            info=basic_info_pb2.BasicInfo(name=name, description=description, tags=tags, owner=owner),
            version=framework_version_pb2.FrameworkVersion.FWV5,
            type=data_source_type_pb2.DataSourceType.STREAM_WITH_BATCH,
            prevent_destroy=prevent_destroy,
        )
        batch_config._merge_batch_args(ds_args)
        stream_config._merge_stream_args(ds_args)
        info = unified_common.TectonObjectInfo.from_args_proto(ds_args.info, ds_args.virtual_data_source_id)
        source_info = cli_common.construct_fco_source_info(ds_args.virtual_data_source_id)

        self.__attrs_init__(
            info=info,
            spec=None,
            args=ds_args,
            source_info=source_info,
            args_supplement=_build_args_supplement(batch_config, stream_config),
        )

        internal_fco.Fco._register(self)

    @classmethod
    @typechecked
    def _from_spec(cls, spec: specs.DataSourceSpec) -> "StreamSource":
        """Create a StreamSource from directly from a spec. Specs are assumed valid and will not be re-validated."""
        info = unified_common.TectonObjectInfo.from_spec(spec)
        obj = cls.__new__(cls)  # Instantiate the object. Does not call init.
        obj.__attrs_init__(
            info=info,
            spec=spec,
            args=None,
            source_info=None,
            args_supplement=None,
        )
        return obj

    def _derive_schemas(self, indentation_level: int) -> None:
        validations_api.print_deriving_schemas(self, indentation_level)
        self._args_supplement.batch_schema = spark_api.derive_batch_schema(
            self._args, self._args_supplement.batch_post_processor, self._args_supplement.batch_data_source_function
        )
        self._args_supplement.stream_schema = spark_api.derive_stream_schema(
            self._args, self._args_supplement.stream_post_processor, self._args_supplement.stream_data_source_function
        )

    @sdk_decorators.sdk_public_method
    @unified_utils.requires_validation
    def start_stream_preview(
        self, table_name: str, *, apply_translator: bool = True, option_overrides: Optional[Dict[str, str]] = None
    ) -> pyspark_streaming.StreamingQuery:
        """
        Starts a streaming job to write incoming records from this DS's stream to a temporary table with a given name.

        After records have been written to the table, they can be queried using ``spark.sql()``. If ran in a Databricks
        notebook, Databricks will also automatically visualize the number of incoming records.

        This is a testing method, most commonly used to verify a StreamDataSource is correctly receiving streaming events.
        Note that the table will grow infinitely large, so this is only really useful for debugging in notebooks.

        :param table_name: The name of the temporary table that this method will write to.
        :param apply_translator: Whether to apply this data source's ``raw_stream_translator``.
            When True, the translated data will be written to the table. When False, the
            raw, untranslated data will be written. ``apply_translator`` is not applicable to stream sources configured
            with ``spark_stream_config`` because it does not have a ``post_processor``.
        :param option_overrides: A dictionary of Spark readStream options that will override any readStream options set
            by the data source. Can be used to configure behavior only for the preview, e.g. setting
            ``startingOffsets:latest`` to preview only the most recent events in a Kafka stream.
        """
        return spark_api.start_stream_preview(self._spec, table_name, apply_translator, option_overrides)

    @sdk_decorators.sdk_public_method
    @unified_utils.requires_validation
    def get_columns(self) -> List[str]:
        """Returns the column names of the data source's streaming schema."""
        schema = self._spec.stream_source.spark_schema
        return [field.name for field in schema.fields]


@attrs.define
class PushSource(DataSource):
    @typechecked
    def __init__(
        self,
        *,
        name: str,
        description: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None,
        owner: Optional[str] = None,
        prevent_destroy: bool = False,
        schema: List[types.Field],
        batch_config: Optional[BatchConfigType] = None,
    ):
        from tecton.cli import common as cli_common

        data_source_type = (
            data_source_type_pb2.DataSourceType.PUSH_WITH_BATCH
            if batch_config is not None
            else data_source_type_pb2.DataSourceType.PUSH_NO_BATCH
        )

        ds_args = virtual_data_source__args_pb2.VirtualDataSourceArgs(
            virtual_data_source_id=id_helper.IdHelper.generate_id(),
            info=basic_info_pb2.BasicInfo(name=name, description=description, tags=tags, owner=owner),
            version=framework_version_pb2.FrameworkVersion.FWV5,
            type=data_source_type,
            prevent_destroy=prevent_destroy,
            schema=schema_container_pb2.SchemaContainer(tecton_schema=type_utils.to_tecton_schema(schema)),
        )
        if batch_config is not None:
            batch_config._merge_batch_args(ds_args)
        info = unified_common.TectonObjectInfo.from_args_proto(ds_args.info, ds_args.virtual_data_source_id)
        source_info = cli_common.construct_fco_source_info(ds_args.virtual_data_source_id)

        self.__attrs_init__(
            info=info,
            spec=None,
            args=ds_args,
            source_info=source_info,
            args_supplement=_build_args_supplement(batch_config, None),
        )

        internal_fco.Fco._register(self)

    @classmethod
    @typechecked
    def _from_spec(cls, spec: specs.DataSourceSpec) -> "PushSource":
        """Create a PushSource from directly from a spec. Specs are assumed valid and will not be re-validated."""
        info = unified_common.TectonObjectInfo.from_spec(spec)
        obj = cls.__new__(cls)  # Instantiate the object. Does not call init.
        obj.__attrs_init__(
            info=info,
            spec=spec,
            args=None,
            source_info=None,
            args_supplement=None,
        )
        return obj

    def _derive_schemas(self, indentation_level: int) -> None:
        assert self._args is not None
        if self._args.type == data_source_type_pb2.DataSourceType.PUSH_NO_BATCH:
            return

        validations_api.print_deriving_schemas(self, indentation_level)
        if conf.get_bool("ALPHA_SNOWFLAKE_COMPUTE_ENABLED"):
            self._args_supplement.batch_schema = snowflake_api.derive_batch_schema(self._args)
        else:
            self._args_supplement.batch_schema = spark_api.derive_batch_schema(
                self._args, self._args_supplement.batch_post_processor, self._args_supplement.batch_data_source_function
            )

    @sdk_decorators.sdk_public_method
    @unified_utils.requires_validation
    def get_columns(self) -> List[str]:
        """Returns the column names of the data source's push schema."""
        schema = self._spec.schema.tecton_schema
        return [column.name for column in schema.columns]


def data_source_from_spec(data_source_spec: specs.DataSourceSpec):
    """Create a Data Source (of the correct type) from the provided spec."""
    if data_source_spec.type == data_source_type_pb2.DataSourceType.STREAM_WITH_BATCH:
        return StreamSource._from_spec(data_source_spec)
    elif data_source_spec.type == data_source_type_pb2.DataSourceType.BATCH:
        return BatchSource._from_spec(data_source_spec)
    elif data_source_spec.type in (
        data_source_type_pb2.DataSourceType.PUSH_WITH_BATCH,
        data_source_type_pb2.DataSourceType.PUSH_NO_BATCH,
    ):
        return PushSource._from_spec(data_source_spec)
    else:
        raise ValueError(f"Unexpected Data Source Type. Spec: {data_source_spec}")


def _build_args_supplement(
    batch_config: Optional[BatchConfigType], stream_config: Optional[StreamConfigType]
) -> specs.DataSourceSpecArgsSupplement:
    supplement = specs.DataSourceSpecArgsSupplement()
    if isinstance(
        batch_config,
        (
            declarative_data_source.FileConfig,
            declarative_data_source.HiveConfig,
            declarative_data_source.RedshiftConfig,
            declarative_data_source.SnowflakeConfig,
        ),
    ):
        supplement.batch_post_processor = batch_config.post_processor
    elif isinstance(batch_config, declarative_data_source.SparkBatchConfig):
        supplement.batch_data_source_function = batch_config.data_source_function
    elif batch_config is not None:
        raise TypeError(f"Unexpected batch_config type: {batch_config}")

    if isinstance(stream_config, (declarative_data_source.KinesisConfig, declarative_data_source.KafkaConfig)):
        supplement.stream_post_processor = stream_config.post_processor
    elif isinstance(stream_config, declarative_data_source.SparkStreamConfig):
        supplement.stream_data_source_function = stream_config.data_source_function
    elif stream_config is not None:
        raise TypeError(f"Unexpected stream_config type: {stream_config}")

    return supplement
