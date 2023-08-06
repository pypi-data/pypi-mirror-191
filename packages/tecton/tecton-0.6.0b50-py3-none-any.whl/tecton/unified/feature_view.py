from __future__ import annotations

import datetime
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Mapping
from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import Union

import attrs
import numpy as np
import pandas
import pendulum
from pyspark import sql as pyspark_sql
from pyspark.sql import dataframe as pyspark_dataframe
from pyspark.sql import streaming
from typeguard import typechecked

from tecton import conf
from tecton import types
from tecton._internals import display
from tecton._internals import errors
from tecton._internals import fco as internal_fco
from tecton._internals import metadata_service
from tecton._internals import sdk_decorators
from tecton._internals import type_utils
from tecton._internals import utils as internal_utils
from tecton.declarative import base as declarative_base
from tecton.declarative import data_source as declarative_data_source
from tecton.declarative import feature_view as declarative_feature_view
from tecton.declarative import filtered_source
from tecton.declarative import transformation as declarative_transformation
from tecton.declarative.feature_view import BatchTriggerType
from tecton.features_common import feature_configs
from tecton.interactive import athena_api
from tecton.interactive import data_frame as tecton_dataframe
from tecton.interactive import delete_keys_api
from tecton.interactive import materialization_api
from tecton.interactive import query_helper
from tecton.interactive import run_api
from tecton.interactive import snowflake_api
from tecton.interactive import spark_api
from tecton.unified import common as unified_common
from tecton.unified import data_source as unified_data_source
from tecton.unified import entity as unified_entity
from tecton.unified import transformation as unified_transformation
from tecton.unified import utils
from tecton.unified import validations_api
from tecton_core import errors as core_errors
from tecton_core import fco_container
from tecton_core import feature_definition_wrapper
from tecton_core import feature_set_config
from tecton_core import id_helper
from tecton_core import pipeline_common
from tecton_core import specs
from tecton_core import time_utils
from tecton_proto.args import basic_info_pb2
from tecton_proto.args import fco_args_pb2
from tecton_proto.args import feature_view_pb2 as feature_view__args_pb2
from tecton_proto.args import pipeline_pb2
from tecton_proto.common import data_source_type_pb2
from tecton_proto.common import fco_locator_pb2
from tecton_proto.data import materialization_status_pb2
from tecton_proto.metadataservice import metadata_service_pb2
from tecton_proto.validation import validator_pb2
from tecton_spark import pipeline_helper
from tecton_spark import request_context
from tecton_spark import spark_schema_wrapper


@attrs.define(eq=False)
class FeatureView(unified_common.BaseTectonObject, declarative_base.BaseFeatureDefinition):
    """Base class for Feature View classes (including Feature Tables).

    Attributes:
        _feature_definition: A FeatureDefinitionWrapper instance, which contains the Feature View spec for this Feature
            View and dependent FCO specs (e.g. Data Source specs). Set only after the object has been validated. Remote
            objects, i.e. applied objects fetched from the backend, are assumed valid.
        _args: A Tecton "args" proto. Only set if this object was defined locally, i.e. this object was not applied
            and fetched from the Tecton backend.
    """

    _feature_definition: Optional[feature_definition_wrapper.FeatureDefinitionWrapper] = attrs.field(repr=False)
    _args: Optional[feature_view__args_pb2.FeatureViewArgs] = attrs.field(repr=False, on_setattr=attrs.setters.frozen)
    _args_supplement: Optional[specs.FeatureViewSpecArgsSupplement] = attrs.field(
        repr=False,
    )

    @property
    def _spec(self) -> Optional[specs.FeatureViewSpec]:
        return self._feature_definition.fv_spec if self._feature_definition is not None else None

    @utils.requires_local_object
    def _build_args(self) -> fco_args_pb2.FcoArgs:
        return fco_args_pb2.FcoArgs(feature_view=self._args)

    def _build_fco_validation_args(self) -> validator_pb2.FcoValidationArgs:
        if self.info._is_local_object:
            assert self._args_supplement is not None
            return validator_pb2.FcoValidationArgs(
                feature_view=validator_pb2.FeatureViewValidationArgs(
                    args=self._args,
                    view_schema=self._args_supplement.view_schema,
                    materialization_schema=self._args_supplement.materialization_schema,
                )
            )
        else:
            return validator_pb2.FcoValidationArgs(feature_view=self._spec.data_proto.validation_args)

    @property
    def _is_valid(self) -> bool:
        return self._spec is not None

    def _derive_schemas(self) -> None:
        raise NotImplementedError

    def _get_dependent_objects(self, include_indirect_dependencies: bool) -> List[unified_common.BaseTectonObject]:
        raise NotImplementedError

    def _validate_dependencies(self, indentation_level: int) -> None:
        dependent_objects = self._get_dependent_objects(include_indirect_dependencies=False)
        validations_api.print_validating_dependencies(self, dependent_objects, indentation_level)
        for dependent_object in dependent_objects:
            dependent_object._validate(indentation_level + 1)

    def _get_dependent_specs(self) -> List[specs.TectonObjectSpec]:
        """Returns all of the specs dependend on by this Feature View."""
        dependent_objects = self._get_dependent_objects(include_indirect_dependencies=True)
        assert all(
            obj._is_valid for obj in dependent_objects
        ), "_get_dependent_specs expects that dependent objects have been validated."
        return [obj._spec for obj in dependent_objects]

    @property
    @utils.requires_validation
    def _check_can_query_from_source(self, from_source: Optional[bool]):
        raise NotImplementedError

    @property
    @sdk_decorators.sdk_public_method
    def join_keys(self) -> List[str]:
        """The join key column names."""
        if self._args is not None:
            return list(specs.get_join_keys_from_feature_view_args(self._args))
        else:
            return list(self._feature_definition.fv_spec.join_keys)

    @property
    @sdk_decorators.sdk_public_method
    def online_serving_keys(self) -> List[str]:
        """The set of join keys that will be indexed and queryable during online serving.

        Defaults to the complete set of join keys.
        """
        if self._args is not None:
            return list(specs.get_online_serving_keys_from_feature_view_args(self._args))
        else:
            return list(self._spec.online_serving_keys)

    @property
    @sdk_decorators.sdk_public_method
    @utils.requires_remote_object
    def url(self) -> str:
        """Returns a link to the Tecton Web UI."""
        return self._feature_definition.fv_spec.url

    @sdk_decorators.sdk_public_method
    @utils.requires_validation
    def get_feature_columns(self) -> List[str]:
        """The features produced by this FeatureView."""
        return self._feature_definition.features

    def _validate(self, indentation_level: int = 0) -> None:
        if self._is_valid:
            return

        self._validate_dependencies(indentation_level)
        self._derive_schemas()

        validations_api.run_backend_validation_and_assert_valid(
            self,
            validator_pb2.ValidationRequest(
                validation_args=[
                    dependent_obj._build_fco_validation_args()
                    for dependent_obj in self._get_dependent_objects(include_indirect_dependencies=True)
                ]
                + [self._build_fco_validation_args()],
            ),
            indentation_level,
        )

        fv_spec = specs.create_feature_view_spec_from_args_proto(self._args, self._args_supplement)
        fco_container_specs = self._get_dependent_specs() + [fv_spec]
        fco_container_ = fco_container.FcoContainer.from_specs(specs=fco_container_specs, root_ids=[fv_spec.id])
        self._feature_definition = feature_definition_wrapper.FeatureDefinitionWrapper(fv_spec, fco_container_)

    @sdk_decorators.sdk_public_method
    @utils.requires_remote_object
    def summary(self) -> display.Displayable:
        """Displays a human readable summary of this data source."""
        request = metadata_service_pb2.GetFeatureViewSummaryRequest(
            fco_locator=fco_locator_pb2.FcoLocator(id=self._spec.id_proto, workspace=self.info.workspace)
        )
        response = metadata_service.instance().GetFeatureViewSummary(request)
        return display.Displayable.from_fco_summary(response.fco_summary)

    def _construct_feature_set_config(self) -> feature_set_config.FeatureSetConfig:
        return feature_set_config.FeatureSetConfig.from_feature_definition(self._feature_definition)

    # TODO(samantha): add delete keys and materialization methods from interactive class
    @sdk_decorators.sdk_public_method
    @sdk_decorators.documented_by(materialization_api.cancel_materialization_job)
    @utils.requires_remote_object
    def cancel_materialization_job(self, job_id: str) -> materialization_api.MaterializationJobData:
        return materialization_api.cancel_materialization_job(self.name, self.workspace, job_id)

    @sdk_decorators.sdk_public_method
    @sdk_decorators.documented_by(materialization_api.get_materialization_job)
    @utils.requires_remote_object
    def get_materialization_job(self, job_id: str) -> materialization_api.MaterializationJobData:
        return materialization_api.get_materialization_job(self.name, self.workspace, job_id)

    @sdk_decorators.sdk_public_method
    @sdk_decorators.documented_by(materialization_api.list_materialization_jobs)
    @utils.requires_remote_object
    def list_materialization_jobs(self) -> List[materialization_api.MaterializationJobData]:
        return materialization_api.list_materialization_jobs(self.name, self.workspace)

    @utils.requires_remote_object
    def _get_materialization_status(self) -> materialization_status_pb2.MaterializationStatus:
        # TODO(TEC-13080): delete this private method when integration tests no longer use it.
        return materialization_api.get_materialization_status_response(self._spec.id_proto)

    @utils.requires_validation
    def _batch_materialization_schedule(self) -> pendulum.Duration:
        return self._feature_definition.batch_materialization_schedule

    @utils.requires_validation
    def _schedule_offset(self) -> pendulum.Duration:
        return self._feature_definition.max_source_data_delay

    @utils.requires_remote_object
    def _get_serving_status(self):
        request = metadata_service_pb2.GetServingStatusRequest(
            feature_package_id=id_helper.IdHelper.from_string(self._feature_definition.id), workspace=self.workspace
        )
        return metadata_service.instance().GetServingStatus(request)


@attrs.define(eq=False)
class MaterializedFeatureView(FeatureView):
    """Class for BatchFeatureView and StreamFeatureView to inherit common methods from.

    Attributes:
        sources: The Data Sources for this Feature View.
        tranformations: The Transformations for this Feature View.
        entities: The Entities for this Feature View.
    """

    sources: Tuple[unified_data_source.DataSource, ...] = attrs.field(
        repr=utils.short_tecton_objects_repr, on_setattr=attrs.setters.frozen
    )
    transformations: Tuple[unified_transformation.Transformation, ...] = attrs.field(
        repr=utils.short_tecton_objects_repr, on_setattr=attrs.setters.frozen
    )
    entities: Tuple[unified_entity.Entity, ...] = attrs.field(
        repr=utils.short_tecton_objects_repr, on_setattr=attrs.setters.frozen
    )

    @classmethod
    @typechecked
    def _from_spec(
        cls, spec: specs.MaterializedFeatureViewSpec, fco_container_: fco_container.FcoContainer
    ) -> "FeatureView":
        """Create a FeatureView from directly from a spec. Specs are assumed valid and will not be re-validated."""
        feature_definition = feature_definition_wrapper.FeatureDefinitionWrapper(spec, fco_container_)
        info = unified_common.TectonObjectInfo.from_spec(spec)

        sources = []
        for data_source_spec in feature_definition.data_sources:
            sources.append(unified_data_source.data_source_from_spec(data_source_spec))

        entities = []
        for entity_spec in feature_definition.entities:
            entities.append(unified_entity.Entity._from_spec(entity_spec))

        transformations = []
        for transformation_spec in feature_definition.transformations:
            transformations.append(unified_transformation.Transformation._from_spec(transformation_spec))

        obj = cls.__new__(cls)  # Instantiate the object. Does not call init.
        obj.__attrs_init__(
            info=info,
            feature_definition=feature_definition,
            args=None,
            source_info=None,
            sources=tuple(sources),
            entities=tuple(entities),
            transformations=tuple(transformations),
            args_supplement=None,
        )

        return obj

    def _get_dependent_objects(self, include_indirect_dependencies: bool) -> List[unified_common.BaseTectonObject]:
        return list(self.sources) + list(self.entities) + list(self.transformations)

    def _derive_schemas(self) -> None:
        assert all(
            [obj._is_valid for obj in self.transformations + self.sources]
        ), "_derive_schemas expects that dependent objects have been validated."
        transformation_specs = [transformation._spec for transformation in self.transformations]
        data_source_specs = [source._spec for source in self.sources]

        if conf.get_bool("ALPHA_SNOWFLAKE_COMPUTE_ENABLED"):
            view_schema = snowflake_api.derive_view_schema_for_feature_view(
                self._args, transformation_specs, data_source_specs
            )
            materialization_schema = snowflake_api.derive_materialization_schema_for_feature_view(
                view_schema, self._args
            )
        else:
            view_schema = spark_api.derive_view_schema_for_feature_view(
                self._args, transformation_specs, data_source_specs
            )
            materialization_schema = spark_api.derive_materialization_schema_for_feature_view(view_schema, self._args)

        self._args_supplement = specs.FeatureViewSpecArgsSupplement(
            view_schema=view_schema,
            materialization_schema=materialization_schema,
        )

    @utils.requires_validation
    def _check_can_query_from_source(self, from_source: Optional[bool]):
        if self._feature_definition.is_incremental_backfill:
            if self.info._is_local_object:
                raise errors.FV_WITH_INC_BACKFILLS_GET_MATERIALIZED_FEATURES_IN_LOCAL_MODE(
                    self.name,
                )
            if not self._feature_definition.materialization_enabled:
                raise errors.FV_WITH_INC_BACKFILLS_GET_MATERIALIZED_FEATURES_FROM_DEVELOPMENT_WORKSPACE(
                    self.name, self.info.workspace
                )

            if from_source:
                raise core_errors.FV_BFC_SINGLE_FROM_SOURCE

            # from_source=None + offline=False computes from source which is not supported for incremental
            if from_source is None and (
                not self._feature_definition.materialization_enabled
                or not self._feature_definition.writes_to_offline_store
            ):
                raise core_errors.FV_BFC_SINGLE_FROM_SOURCE
        elif from_source is False:
            if self._is_local_object:
                raise errors.FD_GET_MATERIALIZED_FEATURES_FROM_LOCAL_OBJECT(self.name, "Feature View")
            elif not self._feature_definition.materialization_enabled:
                raise errors.FD_GET_MATERIALIZED_FEATURES_FROM_DEVELOPMENT_WORKSPACE_GFD(self.name, self.workspace)
            elif not self._feature_definition.writes_to_offline_store:
                raise errors.FD_GET_FEATURES_MATERIALIZATION_DISABLED(self.name)
        elif (
            from_source
            and self._feature_definition.fv_spec.data_source_type == data_source_type_pb2.DataSourceType.PUSH_NO_BATCH
        ):
            raise errors.FEATURE_VIEW_HAS_NO_BATCH_SOURCE(self.name)

    @sdk_decorators.sdk_public_method
    @utils.requires_validation
    def get_historical_features(
        self,
        spine: Optional[
            Union[pyspark_dataframe.DataFrame, pandas.DataFrame, tecton_dataframe.TectonDataFrame, str]
        ] = None,
        timestamp_key: Optional[str] = None,
        start_time: Optional[datetime.datetime] = None,
        end_time: Optional[datetime.datetime] = None,
        entities: Optional[
            Union[pyspark_dataframe.DataFrame, pandas.DataFrame, tecton_dataframe.TectonDataFrame]
        ] = None,
        from_source: Optional[bool] = None,
        save: bool = False,
        save_as: Optional[str] = None,
    ) -> tecton_dataframe.TectonDataFrame:
        """TODO(jake): Port over docs. Deferring to avoid skew while in development."""

        # TODO(jake): Port over get_historical_features() error checking.

        self._check_can_query_from_source(from_source)

        if spine is None and timestamp_key is not None:
            raise errors.GET_HISTORICAL_FEATURES_WRONG_PARAMS(["timestamp_key"], "the spine parameter is not provided")

        if spine is not None and (start_time is not None or end_time is not None or entities is not None):
            raise errors.GET_HISTORICAL_FEATURES_WRONG_PARAMS(
                ["start_time", "end_time", "entities"], "the spine parameter is provided"
            )

        if conf.get_bool("ALPHA_SNOWFLAKE_COMPUTE_ENABLED"):
            return snowflake_api.get_historical_features(
                spine=spine,
                timestamp_key=timestamp_key,
                start_time=start_time,
                end_time=end_time,
                entities=entities,
                from_source=from_source,
                save=save,
                save_as=save_as,
                feature_set_config=self._construct_feature_set_config(),
                append_prefix=False,
            )

        if conf.get_bool("ALPHA_ATHENA_COMPUTE_ENABLED"):
            if self.info.workspace is None or not self._feature_definition.materialization_enabled:
                raise errors.ATHENA_COMPUTE_ONLY_SUPPORTED_IN_LIVE_WORKSPACE

            return athena_api.get_historical_features(
                spine=spine,
                timestamp_key=timestamp_key,
                start_time=start_time,
                end_time=end_time,
                entities=entities,
                from_source=from_source,
                save=save,
                save_as=save_as,
                feature_set_config=self._construct_feature_set_config(),
            )

        return spark_api.get_historical_features_for_feature_definition(
            feature_definition=self._feature_definition,
            spine=spine,
            timestamp_key=timestamp_key,
            start_time=start_time,
            end_time=end_time,
            entities=entities,
            from_source=from_source,
            save=save,
            save_as=save_as,
        )

    @sdk_decorators.sdk_public_method
    @utils.requires_validation
    def run(
        self,
        start_time: Optional[datetime.datetime] = None,
        end_time: Optional[datetime.datetime] = None,
        aggregation_level: Optional[str] = None,
        **mock_sources: Union[pandas.DataFrame, pyspark_dataframe.DataFrame],
    ) -> tecton_dataframe.TectonDataFrame:
        """TODO(samantha): Port over docs."""
        if self._feature_definition.is_temporal and aggregation_level is not None:
            raise errors.FV_UNSUPPORTED_AGGREGATION

        if conf.get_bool("ALPHA_SNOWFLAKE_COMPUTE_ENABLED"):
            return snowflake_api.run_batch(
                fd=self._feature_definition,
                feature_start_time=start_time,
                feature_end_time=end_time,
                mock_inputs=mock_sources,
                aggregate_tiles=None,
                aggregation_level=aggregation_level,
            )

        return run_api.run_batch(
            self._feature_definition,
            start_time,
            end_time,
            mock_sources,
            feature_definition_wrapper.FrameworkVersion.FWV5,
            aggregate_tiles=None,
            aggregation_level=aggregation_level,
        )

    @sdk_decorators.sdk_public_method
    @utils.requires_local_object(error_message=errors.CANNOT_USE_LOCAL_RUN_ON_REMOTE_OBJECT)
    def local_run(
        self,
        spark: pyspark_sql.SparkSession,
        start_time: datetime.datetime,
        end_time: datetime.datetime,
        aggregation_level: Optional[str] = None,
        **mock_sources: Union[pandas.DataFrame, pyspark_dataframe.DataFrame],
    ) -> tecton_dataframe.TectonDataFrame:
        """TODO(jake): Port over docs."""

        # Convert pandas dataframes to pyspark dataframes so that we can use the pyspark schemas for mock schema
        # derivation.
        pyspark_mock_sources = {}
        for input_name, mock_data in mock_sources.items():
            if isinstance(mock_data, pyspark_dataframe.DataFrame):
                pyspark_mock_sources[input_name] = mock_data
            elif isinstance(mock_data, pandas.DataFrame):
                pyspark_mock_sources[input_name] = spark.createDataFrame(mock_data)
            else:
                raise TypeError(f"Unexpected mock source type for kwarg {input_name}: {type(mock_data)}")

        feature_definition = self._create_unvalidated_feature_definition(pyspark_mock_sources)

        return run_api.run_batch(
            feature_definition,
            start_time,
            end_time,
            pyspark_mock_sources,
            feature_definition_wrapper.FrameworkVersion.FWV5,
            aggregate_tiles=None,
            aggregation_level=aggregation_level,
            spark=spark,
        )

    @utils.requires_local_object
    def _create_unvalidated_feature_definition(
        self, mock_sources: Dict[str, pyspark_dataframe.DataFrame]
    ) -> feature_definition_wrapper.FeatureDefinitionWrapper:
        """Create an unvalidated feature definition. Used for user unit testing, where backend validation is unavailable."""
        input_name_to_ds_ids = pipeline_helper.get_all_input_ds_id_map(self._args.pipeline.root)

        if set(input_name_to_ds_ids.keys()) != set(mock_sources.keys()):
            raise errors.FV_INVALID_MOCK_SOURCES(mock_sources.keys(), input_name_to_ds_ids.keys())

        # It's possible to have the same data source included twice in mock_sources under two different input names, but
        # we only need to generate an unvalidated spec once for data source. (Putting two conflicting specs with the
        # same id in the fco container will lead to erros.)
        ds_id_to_mock_df = {}
        for input_name, ds_id in input_name_to_ds_ids.items():
            mock_df = mock_sources[input_name]
            ds_id_to_mock_df[ds_id] = mock_df

        data_source_specs = []
        for source in self.sources:
            mock_df = ds_id_to_mock_df[source.info.id]
            data_source_specs.append(source._create_unvalidated_spec(mock_df))

        transformation_specs = [transformation._create_unvalidated_spec() for transformation in self.transformations]
        entity_specs = [entity._create_unvalidated_spec() for entity in self.entities]

        view_schema = spark_api.derive_view_schema_for_feature_view(self._args, transformation_specs, data_source_specs)
        supplement = specs.FeatureViewSpecArgsSupplement(
            view_schema=view_schema,
            materialization_schema=view_schema,
        )

        fv_spec = specs.create_feature_view_spec_from_args_proto(self._args, supplement)

        fco_container_specs = transformation_specs + data_source_specs + entity_specs + [fv_spec]
        fco_container_ = fco_container.FcoContainer.from_specs(specs=fco_container_specs, root_ids=[fv_spec.id])
        return feature_definition_wrapper.FeatureDefinitionWrapper(fv_spec, fco_container_)

    @sdk_decorators.sdk_public_method
    @utils.requires_remote_object
    def get_online_features(
        self,
        join_keys: Mapping[str, Union[int, np.int_, str, bytes]],
        include_join_keys_in_response: bool = False,
    ) -> tecton_dataframe.FeatureVector:
        """TODO(samantha): Port over docs."""
        if not self._feature_definition.writes_to_online_store:
            raise errors.UNSUPPORTED_OPERATION("get_online_features", "online=True is not set for this FeatureView.")

        return query_helper._QueryHelper(self.info.workspace, feature_view_name=self.info.name).get_feature_vector(
            join_keys,
            include_join_keys_in_response,
            request_context_map={},
            request_context_schema=request_context.RequestContext({}),
        )

    @property
    @sdk_decorators.sdk_public_method
    def feature_start_time(self) -> Optional[datetime.datetime]:
        if self._args is not None:
            return (
                self._args.materialized_feature_view_args.feature_start_time.ToDatetime()
                if self._args.materialized_feature_view_args.HasField("feature_start_time")
                else None
            )
        else:
            return self._spec.feature_start_time

    @property
    @sdk_decorators.sdk_public_method
    def batch_trigger(self) -> declarative_feature_view.BatchTriggerType:
        if self._args is not None:
            batch_trigger = specs.get_batch_trigger_from_feature_view_args(self._args)
        else:
            batch_trigger = self._spec.batch_trigger

        return declarative_feature_view.BatchTriggerType(batch_trigger)

    @utils.requires_validation
    @sdk_decorators.sdk_public_method
    def get_timestamp_field(self) -> str:
        return self._feature_definition.fv_spec.timestamp_field

    @property
    @sdk_decorators.sdk_public_method
    def batch_schedule(self) -> Optional[datetime.timedelta]:
        if self._args is not None:
            return specs.get_batch_schedule_from_feature_view_args(self._args)
        else:
            return self._spec.batch_schedule

    @sdk_decorators.sdk_public_method
    @utils.requires_remote_object
    def delete_keys(
        self,
        keys: Union[pyspark_dataframe.DataFrame, pandas.DataFrame],
        online: bool = True,
        offline: bool = True,
    ) -> None:
        """Deletes any materialized data that matches the specified join keys from the FeatureView.

        This method kicks off a job to delete the data in the offline and online stores.
        If a FeatureView has multiple entities, the full set of join keys must be specified.
        Only supports Delta offline store and Dynamo online store.
        (offline_store=DeltaConfig() and online_store left as default)
        Maximum 500,000 keys can be deleted per request.

        :param keys: The Dataframe to be deleted. Must conform to the FeatureView join keys.
        :param online: (Optional, default=True) Whether or not to delete from the online store.
        :param offline: (Optional, default=True) Whether or not to delete from the offline store.
        :return: None if deletion job was created successfully.
        """
        is_live_workspace = internal_utils.is_live_workspace(self.info.workspace)
        if not is_live_workspace:
            raise errors.UNSUPPORTED_OPERATION_IN_DEVELOPMENT_WORKSPACE("delete_keys")

        return delete_keys_api.delete_keys(online, offline, keys, self._feature_definition)

    @sdk_decorators.sdk_public_method
    @utils.requires_remote_object
    def materialization_status(self, verbose=False, limit=1000, sort_columns=None, errors_only=False):
        """Displays materialization information for the FeatureView, which may include past jobs, scheduled jobs,
        and job failures.

        This method returns different information depending on the type of FeatureView.
        :param verbose: If set to true, method will display additional low level materialization information,
            useful for debugging.
        :param limit: Maximum number of jobs to return.
        :param sort_columns: A comma-separated list of column names by which to sort the rows.
        :param: errors_only: If set to true, method will only return jobs that failed with an error.
        """
        return materialization_api.get_materialization_status_for_display(
            self._spec.id_proto, verbose, limit, sort_columns, errors_only
        )

    @sdk_decorators.sdk_public_method
    @sdk_decorators.documented_by(materialization_api.trigger_materialization_job)
    @utils.requires_remote_object
    def trigger_materialization_job(
        self,
        start_time: datetime,
        end_time: datetime,
        online: bool,
        offline: bool,
        use_tecton_managed_retries: bool = True,
        overwrite: bool = False,
    ) -> str:
        if self.batch_trigger != BatchTriggerType.MANUAL:
            raise errors.FV_NEEDS_TO_BE_BATCH_TRIGGER_MANUAL(self.name)

        return materialization_api.trigger_materialization_job(
            self.name, self.workspace, start_time, end_time, online, offline, use_tecton_managed_retries, overwrite
        )

    @sdk_decorators.sdk_public_method
    @sdk_decorators.documented_by(materialization_api.wait_for_materialization_job)
    @utils.requires_remote_object
    def wait_for_materialization_job(
        self,
        job_id: str,
        timeout: Optional[datetime.timedelta] = None,
    ) -> materialization_api.MaterializationJobData:
        return materialization_api.wait_for_materialization_job(self.name, self.workspace, job_id, timeout)

    @sdk_decorators.sdk_public_method
    @utils.requires_remote_object
    def deletion_status(self, verbose=False, limit=1000, sort_columns=None, errors_only=False):
        """Displays information for deletion jobs created with the delete_keys() method,which may include past jobs,
        scheduled jobs, and job failures.

        :param verbose: If set to true, method will display additional low level deletion information,
            useful for debugging.
        :param limit: Maximum number of jobs to return.
        :param sort_columns: A comma-separated list of column names by which to sort the rows.
        :param: errors_only: If set to true, method will only return jobs that failed with an error.
        """
        return materialization_api.get_deletion_status_for_display(
            self._spec.id_proto, verbose, limit, sort_columns, errors_only
        )


@attrs.define(eq=False)
class BatchFeatureView(MaterializedFeatureView):
    """Tecton class for BatchFeatureViews.

    TODO(samantha): add more info for public docs.
    """

    def __init__(
        self,
        *,
        name: str,
        description: Optional[str] = None,
        owner: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None,
        prevent_destroy: bool = False,
        feature_view_function: Callable,
        sources: Sequence[Union[unified_data_source.BatchSource, filtered_source.FilteredSource]],
        entities: Sequence[unified_entity.Entity],
        mode: str,
        aggregation_interval: Optional[datetime.timedelta] = None,
        aggregations: Optional[Sequence[declarative_feature_view.Aggregation]] = None,
        online: bool = False,
        offline: bool = False,
        ttl: Optional[datetime.timedelta] = None,
        feature_start_time: Optional[datetime.datetime] = None,
        batch_trigger: declarative_feature_view.BatchTriggerType = declarative_feature_view.BatchTriggerType.SCHEDULED,
        batch_schedule: Optional[datetime.timedelta] = None,
        online_serving_index: Optional[Sequence[str]] = None,
        batch_compute: Optional[
            Union[feature_configs.DatabricksClusterConfig, feature_configs.EMRClusterConfig]
        ] = None,
        offline_store: Optional[
            Union[feature_configs.ParquetConfig, feature_configs.DeltaConfig]
        ] = feature_configs.ParquetConfig(),
        online_store: Optional[Union[feature_configs.DynamoConfig, feature_configs.RedisConfig]] = None,
        monitor_freshness: bool = False,
        expected_feature_freshness: Optional[datetime.timedelta] = None,
        alert_email: Optional[str] = None,
        timestamp_field: Optional[str] = None,
        max_batch_aggregation_interval: Optional[datetime.timedelta] = None,
        incremental_backfills: bool = False,
    ):
        from tecton.cli import common as cli_common

        if mode == declarative_feature_view.PIPELINE_MODE:
            pipeline_function = feature_view_function
        else:
            # Separate out the Transformation and manually construct a simple pipeline function.
            # We infer owner/family/tags but not a description.
            inferred_transform = unified_transformation.transformation(mode, name, description, owner, tags=tags)(
                feature_view_function
            )

            def pipeline_function(**kwargs):
                return inferred_transform(**kwargs)

        pipeline_root = _build_pipeline(name, feature_view_function, pipeline_function, sources)

        # Batch Feature Views requiring a stream_processing_mode is a legacy of when stream_processing_mode was
        # called aggregation_mode. Changing this would break `tecton plan` for customers without some backend
        # handling.
        stream_processing_mode = declarative_feature_view.StreamProcessingMode.TIME_INTERVAL if aggregations else None

        args = declarative_feature_view.build_materialized_feature_view_args(
            feature_view_type=feature_view__args_pb2.FeatureViewType.FEATURE_VIEW_TYPE_FWV5_FEATURE_VIEW,
            name=name,
            prevent_destroy=prevent_destroy,
            pipeline=pipeline_pb2.Pipeline(root=pipeline_root.node_proto),
            entities=entities,
            online=online,
            offline=offline,
            offline_store=offline_store,
            online_store=online_store,
            aggregation_interval=aggregation_interval,
            stream_processing_mode=stream_processing_mode,
            aggregations=aggregations,
            ttl=ttl,
            feature_start_time=feature_start_time,
            batch_trigger=batch_trigger,
            batch_schedule=batch_schedule,
            online_serving_index=online_serving_index,
            batch_compute=batch_compute,
            stream_compute=None,
            monitor_freshness=monitor_freshness,
            expected_feature_freshness=expected_feature_freshness,
            alert_email=alert_email,
            description=description,
            owner=owner,
            tags=tags,
            timestamp_field=timestamp_field,
            data_source_type=data_source_type_pb2.DataSourceType.BATCH,
            max_batch_aggregation_interval=max_batch_aggregation_interval,
            output_stream=None,
            incremental_backfills=incremental_backfills,
        )

        info = unified_common.TectonObjectInfo.from_args_proto(args.info, args.feature_view_id)

        data_sources = tuple(
            source.source if isinstance(source, filtered_source.FilteredSource) else source for source in sources
        )

        source_info = cli_common.construct_fco_source_info(args.feature_view_id)
        self.__attrs_init__(
            info=info,
            feature_definition=None,
            args=args,
            source_info=source_info,
            sources=data_sources,
            entities=tuple(entities),
            transformations=tuple(pipeline_root.transformations),
            args_supplement=None,
        )
        internal_fco.Fco._register(self)


@typechecked
def batch_feature_view(
    *,
    name: Optional[str] = None,
    description: Optional[str] = None,
    owner: Optional[str] = None,
    tags: Optional[Dict[str, str]] = None,
    prevent_destroy: bool = False,
    mode: str,
    sources: Sequence[Union[unified_data_source.BatchSource, filtered_source.FilteredSource]],
    entities: Sequence[unified_entity.Entity],
    aggregation_interval: Optional[datetime.timedelta] = None,
    aggregations: Optional[Sequence[declarative_feature_view.Aggregation]] = None,
    online: bool = False,
    offline: bool = False,
    ttl: Optional[datetime.timedelta] = None,
    feature_start_time: Optional[datetime.datetime] = None,
    batch_trigger: declarative_feature_view.BatchTriggerType = declarative_feature_view.BatchTriggerType.SCHEDULED,
    batch_schedule: Optional[datetime.timedelta] = None,
    online_serving_index: Optional[Sequence[str]] = None,
    batch_compute: Optional[Union[feature_configs.DatabricksClusterConfig, feature_configs.EMRClusterConfig]] = None,
    offline_store: Optional[
        Union[feature_configs.ParquetConfig, feature_configs.DeltaConfig]
    ] = feature_configs.ParquetConfig(),
    online_store: Optional[Union[feature_configs.DynamoConfig, feature_configs.RedisConfig]] = None,
    monitor_freshness: bool = False,
    expected_feature_freshness: Optional[datetime.timedelta] = None,
    alert_email: Optional[str] = None,
    timestamp_field: Optional[str] = None,
    max_batch_aggregation_interval: Optional[datetime.timedelta] = None,
    incremental_backfills: bool = False,
):
    """TODO(jake): Port over docs. Deferring to avoid skew while in development."""

    def decorator(feature_view_function):
        return BatchFeatureView(
            name=name or feature_view_function.__name__,
            description=description,
            owner=owner,
            tags=tags,
            prevent_destroy=prevent_destroy,
            feature_view_function=feature_view_function,
            mode=mode,
            sources=sources,
            entities=entities,
            aggregation_interval=aggregation_interval,
            aggregations=aggregations,
            online=online,
            offline=offline,
            ttl=ttl,
            feature_start_time=feature_start_time,
            batch_trigger=batch_trigger,
            batch_schedule=batch_schedule,
            online_serving_index=online_serving_index,
            batch_compute=batch_compute,
            offline_store=offline_store,
            online_store=online_store,
            monitor_freshness=monitor_freshness,
            expected_feature_freshness=expected_feature_freshness,
            alert_email=alert_email,
            timestamp_field=timestamp_field,
            max_batch_aggregation_interval=max_batch_aggregation_interval,
            incremental_backfills=incremental_backfills,
        )

    return decorator


@attrs.define(eq=False)
class StreamFeatureView(MaterializedFeatureView):
    """Tecton class for StreamFeatureViews.

    TODO(samantha): add more info for public docs.
    """

    def __init__(
        self,
        *,
        name: str,
        description: Optional[str] = None,
        owner: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None,
        prevent_destroy: bool = False,
        feature_view_function: Optional[Callable] = None,
        source: Union[unified_data_source.StreamSource, unified_data_source.PushSource, filtered_source.FilteredSource],
        entities: Sequence[unified_entity.Entity],
        mode: Optional[str] = None,
        aggregation_interval: Optional[datetime.timedelta] = None,
        aggregations: Optional[Sequence[declarative_feature_view.Aggregation]] = None,
        stream_processing_mode: Optional[declarative_feature_view.StreamProcessingMode] = None,
        online: bool = False,
        offline: bool = False,
        ttl: Optional[datetime.timedelta] = None,
        feature_start_time: Optional[datetime.datetime] = None,
        batch_trigger: declarative_feature_view.BatchTriggerType = None,
        batch_schedule: Optional[datetime.timedelta] = None,
        online_serving_index: Optional[Sequence[str]] = None,
        batch_compute: Optional[
            Union[feature_configs.DatabricksClusterConfig, feature_configs.EMRClusterConfig]
        ] = None,
        stream_compute: Optional[
            Union[feature_configs.DatabricksClusterConfig, feature_configs.EMRClusterConfig]
        ] = None,
        offline_store: Optional[
            Union[feature_configs.ParquetConfig, feature_configs.DeltaConfig]
        ] = feature_configs.ParquetConfig(),
        online_store: Optional[Union[feature_configs.DynamoConfig, feature_configs.RedisConfig]] = None,
        monitor_freshness: bool = False,
        expected_feature_freshness: Optional[datetime.timedelta] = None,
        alert_email: Optional[str] = None,
        timestamp_field: Optional[str] = None,
        max_batch_aggregation_interval: Optional[datetime.timedelta] = None,
        output_stream: Optional[declarative_base.OutputStream] = None,
    ):
        from tecton.cli import common as cli_common

        data_source = source.source if isinstance(source, filtered_source.FilteredSource) else source
        has_push_source = isinstance(data_source, unified_data_source.PushSource)

        if has_push_source:
            # Stream Feature Views with Push Sources do not have transformations, so the entire pipeline is the source.
            pipeline_root = declarative_feature_view.source_to_pipeline_node(source=source, input_name=data_source.name)
            stream_processing_mode_ = declarative_feature_view.StreamProcessingMode.CONTINUOUS
            data_source_type = data_source.data_source_type
        else:
            if mode == declarative_feature_view.PIPELINE_MODE:
                pipeline_function = feature_view_function
            else:
                # Separate out the Transformation and manually construct a simple pipeline function.
                # We infer owner/family/tags but not a description.
                inferred_transform = unified_transformation.transformation(mode, name, description, owner, tags=tags)(
                    feature_view_function
                )

                def pipeline_function(**kwargs):
                    return inferred_transform(**kwargs)

            if aggregations:
                stream_processing_mode_ = (
                    stream_processing_mode or declarative_feature_view.StreamProcessingMode.TIME_INTERVAL
                )
            else:
                stream_processing_mode_ = stream_processing_mode

            pipeline_root = _build_pipeline(
                name,
                feature_view_function,
                pipeline_function,
                [source],
            )
            data_source_type = data_source_type_pb2.DataSourceType.STREAM_WITH_BATCH

        default_batch_trigger = (
            declarative_feature_view.BatchTriggerType.NO_BATCH_MATERIALIZATION
            if data_source_type == data_source_type_pb2.DataSourceType.PUSH_NO_BATCH
            else declarative_feature_view.BatchTriggerType.SCHEDULED
        )
        batch_trigger_ = batch_trigger or default_batch_trigger
        args = declarative_feature_view.build_materialized_feature_view_args(
            feature_view_type=feature_view__args_pb2.FeatureViewType.FEATURE_VIEW_TYPE_FWV5_FEATURE_VIEW,
            name=name,
            prevent_destroy=prevent_destroy,
            pipeline=pipeline_pb2.Pipeline(root=pipeline_root.node_proto),
            entities=entities,
            online=online,
            offline=offline,
            offline_store=offline_store,
            online_store=online_store,
            aggregation_interval=aggregation_interval,
            stream_processing_mode=stream_processing_mode_,
            aggregations=aggregations,
            ttl=ttl,
            feature_start_time=feature_start_time,
            batch_trigger=batch_trigger_,
            batch_schedule=batch_schedule,
            online_serving_index=online_serving_index,
            batch_compute=batch_compute,
            stream_compute=stream_compute,
            monitor_freshness=monitor_freshness,
            expected_feature_freshness=expected_feature_freshness,
            alert_email=alert_email,
            description=description,
            owner=owner,
            tags=tags,
            timestamp_field=timestamp_field,
            data_source_type=data_source_type,
            max_batch_aggregation_interval=max_batch_aggregation_interval,
            output_stream=output_stream,
            incremental_backfills=False,
        )

        info = unified_common.TectonObjectInfo.from_args_proto(args.info, args.feature_view_id)

        data_sources = (source.source if isinstance(source, filtered_source.FilteredSource) else source,)

        source_info = cli_common.construct_fco_source_info(args.feature_view_id)
        self.__attrs_init__(
            info=info,
            feature_definition=None,
            args=args,
            source_info=source_info,
            sources=data_sources,
            entities=tuple(entities),
            transformations=tuple(pipeline_root.transformations),
            args_supplement=None,
        )
        internal_fco.Fco._register(self)

    @sdk_decorators.sdk_public_method
    @utils.requires_validation
    def run_stream(self, output_temp_table: str) -> streaming.StreamingQuery:
        """TODO(samantha): Port over docs."""
        if self._spec.data_source_type != data_source_type_pb2.DataSourceType.STREAM_WITH_BATCH:
            raise errors.FEATURE_VIEW_HAS_NO_STREAM_SOURCE(self.name)
        return run_api.run_stream(self._feature_definition, output_temp_table)


@typechecked
def stream_feature_view(
    *,
    name: Optional[str] = None,
    description: Optional[str] = None,
    owner: Optional[str] = None,
    tags: Optional[Dict[str, str]] = None,
    prevent_destroy: bool = False,
    source: Union[unified_data_source.StreamSource, filtered_source.FilteredSource],
    entities: Sequence[unified_entity.Entity],
    mode: str,
    aggregation_interval: Optional[datetime.timedelta] = None,
    aggregations: Optional[Sequence[declarative_feature_view.Aggregation]] = None,
    stream_processing_mode: Optional[declarative_feature_view.StreamProcessingMode] = None,
    online: bool = False,
    offline: bool = False,
    ttl: Optional[datetime.timedelta] = None,
    feature_start_time: Optional[datetime.datetime] = None,
    batch_trigger: declarative_feature_view.BatchTriggerType = declarative_feature_view.BatchTriggerType.SCHEDULED,
    batch_schedule: Optional[datetime.timedelta] = None,
    online_serving_index: Optional[Sequence[str]] = None,
    batch_compute: Optional[Union[feature_configs.DatabricksClusterConfig, feature_configs.EMRClusterConfig]] = None,
    stream_compute: Optional[Union[feature_configs.DatabricksClusterConfig, feature_configs.EMRClusterConfig]] = None,
    offline_store: Optional[
        Union[feature_configs.ParquetConfig, feature_configs.DeltaConfig]
    ] = feature_configs.ParquetConfig(),
    online_store: Optional[Union[feature_configs.DynamoConfig, feature_configs.RedisConfig]] = None,
    monitor_freshness: bool = False,
    expected_feature_freshness: Optional[datetime.timedelta] = None,
    alert_email: Optional[str] = None,
    timestamp_field: Optional[str] = None,
    max_batch_aggregation_interval: Optional[datetime.timedelta] = None,
    output_stream: Optional[declarative_base.OutputStream] = None,
):
    """TODO(samantha): Port over docs. Deferring to avoid skew while in development."""

    def decorator(feature_view_function):

        if aggregations:
            stream_processing_mode_ = (
                stream_processing_mode or declarative_feature_view.StreamProcessingMode.TIME_INTERVAL
            )
        else:
            stream_processing_mode_ = stream_processing_mode

        return StreamFeatureView(
            name=name or feature_view_function.__name__,
            description=description,
            owner=owner,
            tags=tags,
            prevent_destroy=prevent_destroy,
            feature_view_function=feature_view_function,
            source=source,
            entities=entities,
            mode=mode,
            aggregation_interval=aggregation_interval,
            aggregations=aggregations,
            stream_processing_mode=stream_processing_mode_,
            online=online,
            offline=offline,
            ttl=ttl,
            feature_start_time=feature_start_time,
            batch_trigger=batch_trigger,
            batch_schedule=batch_schedule,
            online_serving_index=online_serving_index,
            batch_compute=batch_compute,
            stream_compute=stream_compute,
            offline_store=offline_store,
            online_store=online_store,
            monitor_freshness=monitor_freshness,
            expected_feature_freshness=expected_feature_freshness,
            alert_email=alert_email,
            timestamp_field=timestamp_field,
            max_batch_aggregation_interval=max_batch_aggregation_interval,
            output_stream=output_stream,
        )

    return decorator


@attrs.define(eq=False)
class FeatureTable(FeatureView):
    """A Tecton Feature Table.

    Attributes:
        entities: The Entities for this Feature View.
    """

    entities: Tuple[unified_entity.Entity, ...] = attrs.field(
        repr=utils.short_tecton_objects_repr, on_setattr=attrs.setters.frozen
    )

    @typechecked
    def __init__(
        self,
        *,
        name: str,
        description: Optional[str] = None,
        owner: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None,
        prevent_destroy: bool = False,
        entities: List[unified_entity.Entity],
        schema: List[types.Field],
        ttl: Optional[datetime.timedelta] = None,
        online: bool = False,
        offline: bool = False,
        offline_store: feature_configs.DeltaConfig = feature_configs.DeltaConfig(),
        online_store: Optional[Union[feature_configs.DynamoConfig, feature_configs.RedisConfig]] = None,
        batch_compute: Optional[
            Union[feature_configs.DatabricksClusterConfig, feature_configs.EMRClusterConfig]
        ] = None,
        online_serving_index: Optional[List[str]] = None,
    ):
        """Instantiate a new FeatureTable.

        :param name: Unique, human friendly name that identifies the FeatureTable.
        :param description: A human readable description.
        :param owner: Owner name (typically the email of the primary maintainer).
        :param tags: Tags associated with this Tecton Object (key-value pairs of arbitrary metadata).
        :param prevent_destroy: If True, this Tecton object will be blocked from being deleted or re-created (i.e. a
            destructive update) during tecton plan/apply. To remove or update this object, `prevent_destroy` must be
            first set to False via a separate tecton apply. `prevent_destroy` can be used to prevent accidental changes
            such as inadvertantly deleting a Feature Service used in production or recreating a Feature View that
            triggers expensive rematerialization jobs. `prevent_destroy` also blocks changes to dependent Tecton objects
            that would trigger a recreate of the tagged object, e.g. if `prevent_destroy` is set on a Feature Service,
            that will also prevent deletions or re-creates of Feature Views used in that service. `prevent_destroy` is
            only enforced in live (i.e. non-dev) workspaces.
        :param entities: A list of Entity objects, used to organize features.
        :param schema: A schema for the FeatureTable. Supported types are: Int64, Float64, String, Bool and Array with Int64, Float32, Float64 and String typed elements. Additionally you must have exactly one Timestamp typed column for the feature timestamp.
        :param ttl: The TTL (or "look back window") for features defined by this feature table. This parameter determines how long features will live in the online store and how far to  "look back" relative to a training example's timestamp when generating offline training sets. Shorter TTLs improve performance and reduce costs.
        :param online: Enable writing to online feature store. (Default: False)
        :param offline: Enable writing to offline feature store. (Default: False)
        :param offline_store: Configuration for how data is written to the offline feature store.
        :param online_store: Configuration for how data is written to the online feature store.
        :param batch_compute: Batch materialization cluster configuration. Should be one of:
            [``EMRClusterConfig``, ``DatabricksClusterConfig``]
        :param online_serving_index: (Advanced) Defines the set of join keys that will be indexed and queryable during online serving.
            Defaults to the complete set of join keys. Up to one join key may be omitted. If one key is omitted, online requests to a Feature Service will
            return all feature vectors that match the specified join keys.
        :returns: A Feature Table

        An example declaration of a FeatureTable

        .. code-block:: python

            from tecton import Entity, FeatureTable
            from tecton.types import Field, String, Timestamp, Int64
            import datetime

            # Declare your user Entity instance here or import it if defined elsewhere in
            # your Tecton repo.

            user = ...

            schema = [
                Field('user_id', String),
                Field('timestamp', Timestamp),
                Field('user_login_count_7d', Int64),
                Field('user_login_count_30d', Int64)
            ]

            user_login_counts = FeatureTable(
                name='user_login_counts',
                entities=[user],
                schema=schema,
                online=True,
                offline=True,
                ttl=datetime.timedelta(days=30)
            )
        """
        from tecton.cli import common as cli_common

        if isinstance(schema, list):
            wrapper = type_utils.to_spark_schema_wrapper(schema)
        else:
            wrapper = spark_schema_wrapper.SparkSchemaWrapper(schema)

        if batch_compute:
            batch_compute_proto = batch_compute._to_cluster_proto()
        else:
            batch_compute_proto = feature_view__args_pb2.ClusterConfig(
                implicit_config=feature_view__args_pb2.DefaultClusterConfig(**feature_configs.DEFAULT_SPARK_VERSIONS)
            )

        feature_table_args = feature_view__args_pb2.FeatureTableArgs(
            schema=wrapper.to_proto(),
            serving_ttl=time_utils.timedelta_to_proto(ttl),
            batch_compute=batch_compute_proto,
            offline_store=offline_store._to_proto(),
            online_store=online_store._to_proto() if online_store else None,
        )

        # If unspecified, online_serving_index defaults to the join_keys of the Feature Table.
        join_keys = []
        for entity in entities:
            join_keys.extend(entity.join_keys)

        args = feature_view__args_pb2.FeatureViewArgs(
            feature_table_args=feature_table_args,
            feature_view_id=id_helper.IdHelper.generate_id(),
            info=basic_info_pb2.BasicInfo(name=name, description=description, tags=tags, owner=owner),
            prevent_destroy=prevent_destroy,
            feature_view_type=feature_view__args_pb2.FeatureViewType.FEATURE_VIEW_TYPE_FEATURE_TABLE,
            version=feature_definition_wrapper.FrameworkVersion.FWV5.value,
            entities=[
                feature_view__args_pb2.EntityKeyOverride(entity_id=entity.info._id_proto, join_keys=entity.join_keys)
                for entity in entities
            ],
            online_enabled=online,
            offline_enabled=offline,
            online_serving_index=online_serving_index,
        )

        info = unified_common.TectonObjectInfo.from_args_proto(args.info, args.feature_view_id)
        source_info = cli_common.construct_fco_source_info(args.feature_view_id)
        self.__attrs_init__(
            info=info,
            feature_definition=None,
            args=args,
            source_info=source_info,
            entities=tuple(entities),
            args_supplement=None,
        )
        internal_fco.Fco._register(self)

    @classmethod
    @typechecked
    def _from_spec(cls, spec: specs.FeatureTableSpec, fco_container_: fco_container.FcoContainer) -> "FeatureTable":
        """Create a FeatureTable from directly from a spec. Specs are assumed valid and will not be re-validated."""
        feature_definition = feature_definition_wrapper.FeatureDefinitionWrapper(spec, fco_container_)
        info = unified_common.TectonObjectInfo.from_spec(spec)

        entities = []
        for entity_spec in feature_definition.entities:
            entities.append(unified_entity.Entity._from_spec(entity_spec))

        obj = cls.__new__(cls)  # Instantiate the object. Does not call init.
        obj.__attrs_init__(
            info=info,
            feature_definition=feature_definition,
            args=None,
            source_info=None,
            entities=tuple(entities),
            args_supplement=None,
        )

        return obj

    def _get_dependent_objects(self, include_indirect_dependencies: bool) -> List[unified_common.BaseTectonObject]:
        return list(self.entities)

    def _derive_schemas(self) -> None:
        view_schema = spark_api.spark_schema_to_tecton_schema(self._args.feature_table_args.schema)

        # For feature tables, materialization and view schema are the same.
        self._args_supplement = specs.FeatureViewSpecArgsSupplement(
            view_schema=view_schema,
            materialization_schema=view_schema,
        )

    @utils.requires_validation
    def _check_can_query_from_source(self, from_source: Optional[bool]):
        if self._is_local_object:
            raise errors.FD_GET_MATERIALIZED_FEATURES_FROM_LOCAL_OBJECT(self.name, "Feature Table")

        if not self._feature_definition.materialization_enabled:
            raise errors.FEATURE_TABLE_GET_MATERIALIZED_FEATURES_FROM_DEVELOPMENT_WORKSPACE(
                self.info.name, self.info.workspace
            )

        if from_source:
            raise errors.FROM_SOURCE_WITH_FT

        if not self._feature_definition.writes_to_offline_store:
            raise errors.FEATURE_TABLE_GET_MATERIALIZED_FEATURES_OFFLINE_FALSE(self.info.name)

    @sdk_decorators.sdk_public_method
    @utils.requires_remote_object(error_message=errors.INVALID_USAGE_FOR_LOCAL_FEATURE_TABLE_OBJECT)
    def get_historical_features(
        self,
        spine: Optional[Union[pyspark_dataframe.DataFrame, pandas.DataFrame, tecton_dataframe.TectonDataFrame]] = None,
        timestamp_key: Optional[str] = None,
        entities: Optional[
            Union[pyspark_dataframe.DataFrame, pandas.DataFrame, tecton_dataframe.TectonDataFrame]
        ] = None,
        start_time: Optional[datetime.datetime] = None,
        end_time: Optional[datetime.datetime] = None,
        save: bool = False,
        save_as: Optional[str] = None,
    ) -> tecton_dataframe.TectonDataFrame:
        """TODO(samantha): port over docs"""

        self._check_can_query_from_source(from_source=None)

        if spine is None and timestamp_key is not None:
            raise errors.GET_HISTORICAL_FEATURES_WRONG_PARAMS(["timestamp_key"], "the spine parameter is not provided")

        if spine is not None and (start_time is not None or end_time is not None or entities is not None):
            raise errors.GET_HISTORICAL_FEATURES_WRONG_PARAMS(
                ["start_time", "end_time", "entities"], "the spine parameter is provided"
            )

        if conf.get_bool("ALPHA_ATHENA_COMPUTE_ENABLED"):
            return athena_api.get_historical_features(
                spine=spine,
                timestamp_key=timestamp_key,
                start_time=start_time,
                end_time=end_time,
                entities=entities,
                from_source=False,
                save=save,
                save_as=save_as,
                feature_set_config=self._construct_feature_set_config(),
            )

        return spark_api.get_historical_features_for_feature_definition(
            feature_definition=self._feature_definition,
            spine=spine,
            timestamp_key=timestamp_key,
            start_time=start_time,
            end_time=end_time,
            entities=entities,
            from_source=False,
            save=save,
            save_as=save_as,
        )

    @sdk_decorators.sdk_public_method
    @utils.requires_remote_object
    def get_online_features(
        self,
        join_keys: Mapping[str, Union[int, np.int_, str, bytes]],
        include_join_keys_in_response: bool = False,
    ) -> tecton_dataframe.FeatureVector:
        """TODO(samantha): port over docs."""
        if not self._feature_definition.materialization_enabled:
            raise errors.FEATURE_TABLE_GET_ONLINE_FEATURES_FROM_DEVELOPMENT_WORKSPACE(
                self.info.name, self.info.workspace
            )

        if not self._feature_definition.writes_to_online_store:
            raise errors.UNSUPPORTED_OPERATION("get_online_features", "online=True was not set for this Feature Table.")

        return query_helper._QueryHelper(self.info.workspace, feature_view_name=self.info.name).get_feature_vector(
            join_keys,
            include_join_keys_in_response,
            request_context_map={},
            request_context_schema=request_context.RequestContext({}),
        )

    @sdk_decorators.sdk_public_method
    @utils.requires_remote_object
    def ingest(self, df: Union[pyspark_dataframe.DataFrame, pandas.DataFrame]):
        """TODO(samantha): port over docs."""

        if not self._feature_definition.materialization_enabled:
            raise errors.UNSUPPORTED_OPERATION_IN_DEVELOPMENT_WORKSPACE("ingest")

        get_upload_info_request = metadata_service_pb2.GetNewIngestDataframeInfoRequest(
            feature_definition_id=self._spec.id_proto
        )
        upload_info_response = metadata_service.instance().GetNewIngestDataframeInfo(get_upload_info_request)

        df_path = upload_info_response.df_path
        upload_url = upload_info_response.signed_url_for_df_upload
        spark_api.write_dataframe_to_path_or_url(df, df_path, upload_url, self._feature_definition.view_schema)

        ingest_request = metadata_service_pb2.IngestDataframeRequest(
            workspace=self.info.workspace, feature_definition_id=self._spec.id_proto, df_path=df_path
        )
        response = metadata_service.instance().IngestDataframe(ingest_request)

    @utils.requires_validation
    @sdk_decorators.sdk_public_method
    def get_timestamp_field(self) -> str:
        return self._feature_definition.fv_spec.timestamp_field

    @sdk_decorators.sdk_public_method
    @utils.requires_remote_object
    def delete_keys(
        self,
        keys: Union[pyspark_dataframe.DataFrame, pandas.DataFrame],
        online: bool = True,
        offline: bool = True,
    ) -> None:
        """Deletes any materialized data that matches the specified join keys from the FeatureTable.

        This method kicks off a job to delete the data in the offline and online stores.
        If a FeatureTable has multiple entities, the full set of join keys must be specified.
        Only supports Dynamo online store.
        Maximum 500,000 keys can be deleted per request.

        :param keys: The Dataframe to be deleted. Must conform to the FeatureTable join keys.
        :param online: (Optional, default=True) Whether or not to delete from the online store.
        :param offline: (Optional, default=True) Whether or not to delete from the offline store.
        :return: None if deletion job was created successfully.
        """
        is_live_workspace = internal_utils.is_live_workspace(self.info.workspace)
        if not is_live_workspace:
            raise errors.UNSUPPORTED_OPERATION_IN_DEVELOPMENT_WORKSPACE("delete_keys")

        return delete_keys_api.delete_keys(online, offline, keys, self._feature_definition)

    @sdk_decorators.documented_by(MaterializedFeatureView.materialization_status)
    @utils.requires_remote_object
    def materialization_status(self, verbose=False, limit=1000, sort_columns=None, errors_only=False):
        return materialization_api.get_materialization_status_for_display(
            self._spec.id_proto, verbose, limit, sort_columns, errors_only
        )

    @sdk_decorators.sdk_public_method
    @sdk_decorators.documented_by(MaterializedFeatureView.deletion_status)
    @utils.requires_remote_object
    def deletion_status(self, verbose=False, limit=1000, sort_columns=None, errors_only=False):
        return materialization_api.get_deletion_status_for_display(
            self._spec.id_proto, verbose, limit, sort_columns, errors_only
        )


@attrs.define(eq=False)
class OnDemandFeatureView(FeatureView):
    """A Tecton On-Demand Feature View.

    Attributes:
        sources: The Request Sources and dependent Feature Views for this On Demand Feature View.
        tranformations: The Transformations for this Feature View.
    """

    sources: Tuple[Union[declarative_base.FeatureReference, declarative_data_source.RequestSource], ...] = attrs.field(
        on_setattr=attrs.setters.frozen
    )
    transformations: Tuple[unified_transformation.Transformation, ...] = attrs.field(
        repr=utils.short_tecton_objects_repr, on_setattr=attrs.setters.frozen
    )

    def __init__(
        self,
        *,
        name: str,
        description: Optional[str] = None,
        owner: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None,
        prevent_destroy: bool = False,
        mode: str,
        sources: List[Union[declarative_data_source.RequestSource, FeatureView, declarative_base.FeatureReference]],
        schema: List[types.Field],
        feature_view_function: Callable,
    ):
        from tecton.cli import common as cli_common

        if mode == declarative_feature_view.PIPELINE_MODE:
            pipeline_function = feature_view_function
        else:
            # Separate out the Transformation and manually construct a simple pipeline function.
            # We infer owner/family/tags but not a description.
            inferred_transform = unified_transformation.transformation(mode, name, description, owner, tags=tags)(
                feature_view_function
            )

            def pipeline_function(**kwargs):
                return inferred_transform(**kwargs)

        pipeline_root = declarative_feature_view.build_pipeline_for_odfv(
            name, feature_view_function, pipeline_function, sources
        )

        spark_schema_wrapper = type_utils.to_spark_schema_wrapper(schema)

        args = feature_view__args_pb2.FeatureViewArgs(
            feature_view_id=id_helper.IdHelper.generate_id(),
            info=basic_info_pb2.BasicInfo(name=name, description=description, tags=tags, owner=owner),
            prevent_destroy=prevent_destroy,
            version=feature_definition_wrapper.FrameworkVersion.FWV5.value,
            pipeline=pipeline_pb2.Pipeline(root=pipeline_root.node_proto),
            feature_view_type=feature_view__args_pb2.FeatureViewType.FEATURE_VIEW_TYPE_ON_DEMAND,
            on_demand_args=feature_view__args_pb2.OnDemandArgs(schema=spark_schema_wrapper.to_proto()),
        )

        info = unified_common.TectonObjectInfo.from_args_proto(args.info, args.feature_view_id)
        source_info = cli_common.construct_fco_source_info(args.feature_view_id)

        references_and_request_sources = []
        for source in sources:
            if isinstance(source, FeatureView):
                references_and_request_sources.append(declarative_base.FeatureReference(feature_definition=source))
            else:
                references_and_request_sources.append(source)

        self.__attrs_init__(
            info=info,
            feature_definition=None,
            args=args,
            source_info=source_info,
            sources=tuple(references_and_request_sources),
            transformations=tuple(pipeline_root.transformations),
            args_supplement=None,
        )

        internal_fco.Fco._register(self)

    @classmethod
    @typechecked
    def _from_spec(
        cls, spec: specs.OnDemandFeatureViewSpec, fco_container_: fco_container.FcoContainer
    ) -> "FeatureView":
        """Create a FeatureView from directly from a spec. Specs are assumed valid and will not be re-validated."""
        feature_definition = feature_definition_wrapper.FeatureDefinitionWrapper(spec, fco_container_)
        info = unified_common.TectonObjectInfo.from_spec(spec)

        transformations = []
        for transformation_spec in feature_definition.transformations:
            transformations.append(unified_transformation.Transformation._from_spec(transformation_spec))

        obj = cls.__new__(cls)  # Instantiate the object. Does not call init.
        obj.__attrs_init__(
            info=info,
            feature_definition=feature_definition,
            args=None,
            source_info=None,
            sources=_build_odfv_sources_from_spec(spec, fco_container_),
            transformations=tuple(transformations),
            args_supplement=None,
        )

        return obj

    def _get_dependent_objects(self, include_indirect_dependencies: bool) -> List[unified_common.BaseTectonObject]:
        dependent_objects = list(self.transformations)
        for fv in self._get_dependent_feature_views():
            if include_indirect_dependencies:
                dependent_objects.extend(fv._get_dependent_objects(include_indirect_dependencies=True) + [fv])
            else:
                dependent_objects.append(fv)

        # Dedupe by ID.
        return list({fco_obj.id: fco_obj for fco_obj in dependent_objects}.values())

    def _get_dependent_feature_views(self) -> List[FeatureView]:
        return [
            source.feature_definition
            for source in self.sources
            if isinstance(source, declarative_base.FeatureReference)
        ]

    def _derive_schemas(self) -> None:
        view_schema = spark_api.spark_schema_to_tecton_schema(self._args.on_demand_args.schema)

        self._args_supplement = specs.FeatureViewSpecArgsSupplement(
            view_schema=view_schema,
            materialization_schema=view_schema,
        )

    @utils.requires_validation
    def _check_can_query_from_source(self, from_source: Optional[bool]):
        for fv in self._get_dependent_feature_views():
            fv._check_can_query_from_source(from_source)

    @sdk_decorators.sdk_public_method
    @utils.requires_validation
    def run(
        self, **mock_inputs: Union[Dict[str, Any], pandas.DataFrame, pyspark_dataframe.DataFrame]
    ) -> Union[Dict[str, Any], tecton_dataframe.TectonDataFrame]:
        """TODO(samantha): port over docs."""
        # Snowflake compute uses the same code for run_ondemand as Spark.
        return run_api.run_ondemand(self._feature_definition, self.info.name, mock_inputs)

    @sdk_decorators.sdk_public_method
    @utils.requires_local_object(error_message=errors.CANNOT_USE_LOCAL_RUN_ON_REMOTE_OBJECT)
    def local_run(
        self, **mock_sources: Union[Dict[str, Any], pandas.DataFrame]
    ) -> Union[Dict[str, Any], pandas.DataFrame]:
        """Run the OnDemandFeatureView using mock sources.

        :param mock_sources: Required. Keyword args with the same expected keys
            as the OnDemandFeatureView's inputs parameters.
            For the "python" mode, each input must be a Dictionary representing a single row.
            For the "pandas" mode, each input must be a DataFrame with all of them containing the
            same number of rows and matching row ordering.

        Example:
            .. code-block:: python

                @on_demand_feature_view(
                    sources=[transaction_request],
                    mode='python',
                    schema=output_schema,
                )
                def transaction_amount_is_high(transaction_request):
                    return {'transaction_amount_is_high': transaction_request['amount'] > 10000}

                # Test using `run` API.
                result = transaction_amount_is_high.local_run(transaction_request={'amount': 100})

        :return: A `Dict` object for the "python" mode and a `pandas.DataFrame` object for the "pandas" mode".
        """
        run_api.validate_ondemand_mock_inputs_keys(mock_sources, self._args.pipeline)

        transformation_specs = [transformation._create_unvalidated_spec() for transformation in self.transformations]

        return pipeline_helper.run_mock_odfv_pipeline(
            self._args.pipeline, transformation_specs, self.name, mock_sources
        )

    @sdk_decorators.sdk_public_method
    @utils.requires_validation
    def get_historical_features(
        self,
        spine: Union[pyspark_dataframe.DataFrame, pandas.DataFrame, tecton_dataframe.TectonDataFrame, str],
        timestamp_key: Optional[str] = None,
        from_source: Optional[bool] = None,
        save: bool = False,
        save_as: Optional[str] = None,
    ) -> tecton_dataframe.TectonDataFrame:
        """TODO(samantha): port over docs."""

        self._check_can_query_from_source(from_source)

        if conf.get_bool("ALPHA_SNOWFLAKE_COMPUTE_ENABLED"):
            return snowflake_api.get_historical_features(
                spine=spine,
                timestamp_key=timestamp_key,
                from_source=from_source,
                save=save,
                save_as=save_as,
                feature_set_config=feature_set_config.FeatureSetConfig.from_feature_definition(
                    self._feature_definition
                ),
                append_prefix=False,
            )

        if conf.get_bool("ALPHA_ATHENA_COMPUTE_ENABLED"):
            if not self._feature_definition.materialization_enabled:
                raise errors.ATHENA_COMPUTE_ONLY_SUPPORTED_IN_LIVE_WORKSPACE

            return athena_api.get_historical_features(
                spine=spine,
                timestamp_key=timestamp_key,
                from_source=from_source,
                save=save,
                save_as=save_as,
                feature_set_config=feature_set_config,
            )

        return spark_api.get_historical_features_for_feature_definition(
            feature_definition=self._feature_definition,
            spine=spine,
            timestamp_key=timestamp_key,
            start_time=None,
            end_time=None,
            entities=None,
            from_source=from_source,
            save=save,
            save_as=save_as,
        )

    @sdk_decorators.sdk_public_method
    @utils.requires_remote_object
    def get_online_features(
        self,
        join_keys: Optional[Mapping[str, Union[int, np.int_, str, bytes]]] = None,
        include_join_keys_in_response: bool = False,
        request_data: Optional[Mapping[str, Union[int, np.int_, str, bytes, float]]] = None,
    ) -> tecton_dataframe.FeatureVector:
        """TODO(samantha): port over docs."""
        # Default to empty dicts.
        join_keys = join_keys or {}
        request_data = request_data or {}

        if not join_keys and not request_data:
            raise errors.GET_ONLINE_FEATURES_REQUIRED_ARGS

        if not join_keys and self._get_dependent_feature_views():
            raise errors.GET_ONLINE_FEATURES_ODFV_JOIN_KEYS

        request_context = self._request_context
        required_request_context_keys = list(request_context.schema.keys())
        if len(required_request_context_keys) > 0 and request_data is None:
            raise errors.GET_ONLINE_FEATURES_FV_NO_REQUEST_DATA(required_request_context_keys)
        internal_utils.validate_request_data(request_data, required_request_context_keys)

        return query_helper._QueryHelper(self.workspace, feature_view_name=self.name).get_feature_vector(
            join_keys,
            include_join_keys_in_response,
            request_data,
            request_context,
        )

    @property
    @utils.requires_validation
    def _request_context(self) -> request_context.RequestContext:
        rc = pipeline_common.find_request_context(self._feature_definition.pipeline.root)
        return request_context.RequestContext({}) if rc is None else request_context.RequestContext.from_proto(rc)


@typechecked
def on_demand_feature_view(
    *,
    name: Optional[str] = None,
    description: Optional[str] = None,
    owner: Optional[str] = None,
    tags: Optional[Dict[str, str]] = None,
    prevent_destroy: bool = False,
    mode: str,
    sources: List[Union[declarative_data_source.RequestSource, FeatureView, declarative_base.FeatureReference]],
    schema: List[types.Field],
):
    """TODO(samantha): port over docs."""

    def decorator(feature_view_function):
        return OnDemandFeatureView(
            name=name or feature_view_function.__name__,
            description=description,
            owner=owner,
            tags=tags,
            prevent_destroy=prevent_destroy,
            mode=mode,
            sources=sources,
            schema=schema,
            feature_view_function=feature_view_function,
        )

    return decorator


@typechecked
def _build_pipeline(
    fv_name: str,
    feature_view_function: Callable,
    pipeline_function: Callable[..., declarative_transformation.PipelineNodeWrapper],
    sources: Sequence[Union[unified_data_source.DataSource, filtered_source.FilteredSource]],
) -> declarative_transformation.PipelineNodeWrapper:
    fn_params = declarative_feature_view.get_source_input_params(feature_view_function)
    params_to_sources = dict(zip(fn_params, sources))
    pipeline_root = declarative_feature_view.transformation_to_pipeline_node(pipeline_function, params_to_sources)
    # we bind to user_function since pipeline_function may be artificially created and just accept **kwargs
    declarative_feature_view.test_binding_user_function(feature_view_function, params_to_sources)

    pipeline_common.transformation_type_checker(
        fv_name,
        pipeline_root.node_proto,
        "pipeline",
        ["pipeline", "spark_sql", "pyspark", "snowflake_sql", "athena", "snowpark"],
    )

    return pipeline_root


def feature_view_from_spec(feature_view_spec: specs.FeatureViewSpec, fco_container_: fco_container.FcoContainer):
    # TODO(samantha): Combine with get_feature_view_by_type when we kill the interactive code.
    if isinstance(feature_view_spec, specs.OnDemandFeatureViewSpec):
        return OnDemandFeatureView._from_spec(feature_view_spec, fco_container_)
    elif isinstance(feature_view_spec, specs.FeatureTableSpec):
        return FeatureTable._from_spec(feature_view_spec, fco_container_)
    elif isinstance(feature_view_spec, specs.MaterializedFeatureViewSpec):
        if feature_view_spec.data_source_type == data_source_type_pb2.DataSourceType.BATCH:
            return BatchFeatureView._from_spec(feature_view_spec, fco_container_)
        if feature_view_spec.data_source_type in (
            data_source_type_pb2.DataSourceType.STREAM_WITH_BATCH,
            data_source_type_pb2.DataSourceType.PUSH_WITH_BATCH,
            data_source_type_pb2.DataSourceType.PUSH_NO_BATCH,
        ):
            return StreamFeatureView._from_spec(feature_view_spec, fco_container_)
    raise errors.INTERNAL_ERROR("Missing or unsupported FeatureView type.")


def _build_odfv_sources_from_spec(
    spec: specs.OnDemandFeatureViewSpec, fco_container_: fco_container.FcoContainer
) -> Tuple[Union[declarative_base.FeatureReference, declarative_data_source.RequestSource], ...]:
    sources = []
    request_context = pipeline_common.find_request_context(spec.pipeline.root)
    if request_context is not None:
        request_schema = spark_api.get_request_schema_from_spark_schema(request_context.schema)
        sources.append(declarative_data_source.RequestSource(schema=request_schema))

    feature_view_nodes = pipeline_common.get_all_feature_view_nodes(spec.pipeline)
    for node in feature_view_nodes:
        fv_spec = fco_container_.get_by_id_proto(node.feature_view_node.feature_view_id)
        fv = feature_view_from_spec(fv_spec, fco_container_)
        override_join_keys = {
            colpair.spine_column: colpair.feature_column
            for colpair in node.feature_view_node.feature_view.override_join_keys
        }
        feature_reference = declarative_base.FeatureReference(
            feature_definition=fv,
            namespace=node.feature_view_node.feature_view.namespace,
            features=node.feature_view_node.feature_view.features,
            override_join_keys=override_join_keys,
        )
        sources.append(feature_reference)

    return sources
