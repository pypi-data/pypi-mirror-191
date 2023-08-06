from datetime import datetime
from typing import Mapping
from typing import Optional
from typing import Union

import numpy as np
import pandas
import pendulum
import pyspark

from tecton import conf
from tecton._internals import errors
from tecton._internals import metadata_service
from tecton._internals import utils
from tecton._internals.sdk_decorators import sdk_public_method
from tecton._internals.utils import validate_join_key_types
from tecton.interactive import athena_api
from tecton.interactive import delete_keys_api
from tecton.interactive import materialization_api
from tecton.interactive import spark_api
from tecton.interactive.data_frame import FeatureVector
from tecton.interactive.data_frame import TectonDataFrame
from tecton.interactive.feature_definition import FeatureDefinition
from tecton.interactive.query_helper import _QueryHelper
from tecton.unified import feature_view as unified_feature_view
from tecton_core import specs
from tecton_core.fco_container import FcoContainer
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper
from tecton_core.feature_definition_wrapper import FrameworkVersion
from tecton_core.logger import get_logger
from tecton_proto.metadataservice.metadata_service_pb2 import GetFeatureViewRequest
from tecton_proto.metadataservice.metadata_service_pb2 import GetNewIngestDataframeInfoRequest
from tecton_proto.metadataservice.metadata_service_pb2 import IngestDataframeRequest

logger = get_logger("FeatureTable")

__all__ = ["FeatureTable", "get_feature_table"]


class FeatureTable(FeatureDefinition):
    """
    FeatureTable class.

    To get a FeatureTable instance, call :py:func:`tecton.get_feature_table`.
    """

    def __init__(self, proto, fco_container):
        """
        :param proto: FT proto
        :param fco_container: Contains all FV dependencies, e.g., Entities, DS-es, Transformations
        """
        self._proto = proto
        self._spec = specs.create_feature_view_spec_from_data_proto(proto)
        assert isinstance(fco_container, FcoContainer), type(fco_container)
        self._fco_container = fco_container

    @classmethod
    def _fco_type_name_singular_snake_case(cls) -> str:
        return "feature_table"

    @classmethod
    def _fco_type_name_plural_snake_case(cls) -> str:
        return "feature_tables"

    def __str__(self):
        return f"FeatureTable|{self.id}"

    def __repr__(self):
        return f"FeatureTable(name='{self.name}')"

    @property
    def _timestamp_key(self) -> str:
        return self._proto.timestamp_key

    @property
    def timestamp_field(self) -> str:
        """
        Returns the timestamp_field of this FeatureView.
        """
        return self._timestamp_key

    @sdk_public_method
    def get_historical_features(
        self,
        spine: Optional[Union[pyspark.sql.dataframe.DataFrame, pandas.DataFrame, TectonDataFrame]] = None,
        timestamp_key: Optional[str] = None,
        entities: Optional[Union[pyspark.sql.dataframe.DataFrame, pandas.DataFrame, TectonDataFrame]] = None,
        start_time: Optional[Union[pendulum.DateTime, datetime]] = None,
        end_time: Optional[Union[pendulum.DateTime, datetime]] = None,
        save: bool = False,
        save_as: Optional[str] = None,
    ) -> TectonDataFrame:
        """
        Returns a Tecton :class:`TectonDataFrame` of historical values for this feature table.
        If no arguments are passed in, all feature values for this feature table will be returned in a TectonDataFrame.
        Note:
        The `timestamp_key` parameter is only applicable when a spine is passed in.
        Parameters `start_time`, `end_time`, and `entities` are only applicable when a spine is not passed in.

        :param spine: The spine to join against, as a dataframe.
            If present, the returned DataFrame will contain rollups for all (join key, temporal key)
            combinations that are required to compute a full frame from the spine.
            To distinguish between spine columns and feature columns, feature columns are labeled as
            `feature_view_name.feature_name` in the returned DataFrame.
            If spine is not specified, it'll return a DataFrame of  feature values in the specified time range.
        :type spine: Union[pyspark.sql.DataFrame, pandas.DataFrame, TectonDataFrame]
        :param timestamp_key: Name of the time column in spine.
            This method will fetch the latest features computed before the specified timestamps in this column.
            If unspecified, will default to the time column of the spine if there is only one present.
        :type timestamp_key: str
        :param entities: A DataFrame that is used to filter down feature values.
            If specified, this DataFrame should only contain join key columns.
        :type entities: Union[pyspark.sql.DataFrame, pandas.DataFrame, TectonDataFrame]
        :param start_time: The interval start time from when we want to retrieve features.
            If no timezone is specified, will default to using UTC.
        :type start_time: Union[pendulum.DateTime, datetime.datetime]
        :param end_time:  The interval end time until when we want to retrieve features.
            If no timezone is specified, will default to using UTC.
        :type end_time: Union[pendulum.DateTime, datetime.datetime]
        :param save: Whether to persist the DataFrame as a Dataset object. Default is False.
        :type save: bool
        :param save_as: name to save the DataFrame as.
                If unspecified and save=True, a name will be generated.
        :type save_as: str

        Examples:
            A FeatureTable :py:mod:`ft` with join key :py:mod:`user_id`.

            1) :py:mod:`ft.get_historical_features(spine)` where :py:mod:`spine=pandas.Dataframe({'user_id': [1,2,3], 'date': [datetime(...), datetime(...), datetime(...)]})`
            Fetch historical features from the offline store for users 1, 2, and 3 for the specified timestamps in the spine.

            2) :py:mod:`ft.get_historical_features(spine, save_as='my_dataset)` where :py:mod:`spine=pandas.Dataframe({'user_id': [1,2,3], 'date': [datetime(...), datetime(...), datetime(...)]})`
            Fetch historical features from the offline store for users 1, 2, and 3 for the specified timestamps in the spine. Save the DataFrame as dataset with the name :py:mod`my_dataset`.

            3) :py:mod:`ft.get_historical_features(spine, timestamp_key='date_1')` where :py:mod:`spine=pandas.Dataframe({'user_id': [1,2,3], 'date_1': [datetime(...), datetime(...), datetime(...)], 'date_2': [datetime(...), datetime(...), datetime(...)]})`
            Fetch historical features from the offline store for users 1, 2, and 3 for the specified timestamps in the 'date_1' column in the spine.

            4) :py:mod:`ft.get_historical_features(start_time=datetime(...), end_time=datetime(...))`
            Fetch all historical features from the offline store in the time range specified by `start_time` and `end_time`.

        :return: A TectonDataFrame with features values.
        """
        feature_set_config = self._construct_feature_set_config()
        feature_definition = FeatureDefinitionWrapper(self._spec, self._fco_container)
        is_dev_workspace = not utils.is_live_workspace(self.workspace)

        if is_dev_workspace:
            raise errors.FEATURE_TABLE_GET_MATERIALIZED_FEATURES_FROM_DEVELOPMENT_WORKSPACE(self.name, self.workspace)

        if not feature_definition.writes_to_offline_store:
            raise errors.FEATURE_TABLE_GET_MATERIALIZED_FEATURES_OFFLINE_FALSE(self.name)

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
                feature_set_config=feature_set_config,
            )

        return spark_api.get_historical_features_for_feature_definition(
            feature_definition=feature_definition,
            spine=spine,
            timestamp_key=timestamp_key,
            start_time=start_time,
            end_time=end_time,
            entities=entities,
            from_source=False,
            save=save,
            save_as=save_as,
        )

    @sdk_public_method
    def get_online_features(
        self,
        join_keys: Mapping[str, Union[int, np.int_, str, bytes]],
        include_join_keys_in_response: bool = False,
    ) -> FeatureVector:
        """
        Returns a single Tecton FeatureVector from the Online Store.

        :param join_keys: Join keys of the enclosed FeatureTable.
        :param include_join_keys_in_response: Whether to include join keys as part of the response FeatureVector.

        Examples:
            A FeatureTable :py:mod:`ft` with join key :py:mod:`user_id`.

            1) :py:mod:`ft.get_online_features(join_keys={'user_id': 1})`
            Fetch the latest features from the online store for user 1.

            2) :py:mod:`ft.get_online_features(join_keys={'user_id': 1}, include_join_keys_in_respone=True)`
            Fetch the latest features from the online store for user 1 and include the join key information (user_id=1) in the returned FeatureVector.

        :return: A FeatureVector of the results.
        """
        if not self._proto.feature_table.online_enabled:
            raise errors.UNSUPPORTED_OPERATION(
                "get_online_features", "online_serving_enabled was not defined for this Feature Table."
            )
        validate_join_key_types(join_keys)

        return _QueryHelper(self._proto.fco_metadata.workspace, feature_view_name=self.name).get_feature_vector(
            join_keys, include_join_keys_in_response, request_context_map=None, request_context_schema=None
        )

    @sdk_public_method
    def ingest(self, df: Union[pyspark.sql.dataframe.DataFrame, pandas.DataFrame]):
        """
        Ingests a Dataframe into the FeatureTable. This method kicks off a materialization
        job to write the data into the offline and online store, depending on the Feature Table configuration.

        :param df: The Dataframe to be ingested. Has to conform to the FeatureTable schema.
        """

        if not utils.is_live_workspace(self.workspace):
            raise errors.UNSUPPORTED_OPERATION_IN_DEVELOPMENT_WORKSPACE("ingest")

        get_upload_info_request = GetNewIngestDataframeInfoRequest()
        get_upload_info_request.feature_definition_id.CopyFrom(self._id_proto)
        upload_info_response = metadata_service.instance().GetNewIngestDataframeInfo(get_upload_info_request)
        df_path = upload_info_response.df_path
        upload_url = upload_info_response.signed_url_for_df_upload

        spark_api.write_dataframe_to_path_or_url(df, df_path, upload_url, self._view_schema)

        ingest_request = IngestDataframeRequest()
        ingest_request.workspace = self.workspace
        ingest_request.feature_definition_id.CopyFrom(self._id_proto)
        ingest_request.df_path = df_path
        response = metadata_service.instance().IngestDataframe(ingest_request)

    @sdk_public_method
    def materialization_status(self, verbose=False, limit=1000, sort_columns=None, errors_only=False):
        """
        Displays materialization information for the FeatureTable, which may include past jobs, scheduled jobs,
        and job failures.

        :param verbose: If set to true, method will display additional low level materialization information,
            useful for debugging.
        :param limit: Maximum number of jobs to return.
        :param sort_columns: A comma-separated list of column names by which to sort the rows.
        :param: errors_only: If set to true, method will only return jobs that failed with an error.
        """
        return materialization_api.get_materialization_status_for_display(
            self._id_proto, verbose, limit, sort_columns, errors_only
        )

    def delete_keys(
        self,
        keys: Union[pyspark.sql.dataframe.DataFrame, pandas.DataFrame],
        online: bool = True,
        offline: bool = True,
    ) -> None:
        """
        Deletes any materialized data that matches the specified join keys from the FeatureTable.
        This method kicks off a job to delete the data in the offline and online stores.
        If a FeatureTable has multiple entities, the full set of join keys must be specified.
        Only supports Dynamo online store.
        Maximum 500,000 keys can be deleted per request.

        :param keys: The Dataframe to be deleted. Must conform to the FeatureTable join keys.
        :param online: (Optional, default=True) Whether or not to delete from the online store.
        :param offline: (Optional, default=True) Whether or not to delete from the offline store.
        :return: None if deletion job was created successfully.
        """
        is_live_workspace = utils.is_live_workspace(self.workspace)
        if not is_live_workspace:
            raise errors.UNSUPPORTED_OPERATION_IN_DEVELOPMENT_WORKSPACE("delete_keys")

        fd = FeatureDefinitionWrapper(self._spec, self._fco_container)
        return delete_keys_api.delete_keys(online, offline, keys, fd)

    def deletion_status(self, verbose=False, limit=1000, sort_columns=None, errors_only=False):
        """
        Displays information for deletion jobs created with the delete_keys() method,
        which may include past jobs, scheduled jobs, and job failures.

        :param verbose: If set to true, method will display additional low level deletion information,
            useful for debugging.
        :param limit: Maximum number of jobs to return.
        :param sort_columns: A comma-separated list of column names by which to sort the rows.
        :param: errors_only: If set to true, method will only return jobs that failed with an error.
        """
        return self._deletion_status(verbose, limit, sort_columns, errors_only)


@sdk_public_method
def get_feature_table(
    ft_reference: str, workspace_name: Optional[str] = None
) -> Union[FeatureTable, unified_feature_view.FeatureTable]:
    """
    Fetch an existing :class:`tecton.interactive.FeatureTable` by name.

    :param ft_reference: Either a name or a hexadecimal feature table ID.
    :returns: :class:`tecton.interactive.FeatureTable`
    """

    if workspace_name == None:
        logger.warning(
            "`tecton.get_feature_table('<name>')` is deprecated. Please use `tecton.get_workspace('<workspace_name>').get_feature_table('<name>')` instead."
        )

    request = GetFeatureViewRequest()
    request.version_specifier = ft_reference
    request.workspace = workspace_name or conf.get_or_none("TECTON_WORKSPACE")
    response = metadata_service.instance().GetFeatureView(request)
    fco_container = FcoContainer.from_proto(response.fco_container)
    feature_table_spec = fco_container.get_single_root()

    if feature_table_spec is None:
        raise errors.FCO_NOT_FOUND(FeatureTable, ft_reference)

    assert isinstance(feature_table_spec, specs.FeatureViewSpec)
    ft_proto = feature_table_spec.data_proto

    if not ft_proto.HasField("feature_table"):
        raise errors.FCO_NOT_FOUND_WRONG_TYPE(FeatureTable, ft_reference, "get_feature_table")

    if ft_proto.fco_metadata.framework_version != FrameworkVersion.FWV5.value:
        raise errors.UNSUPPORTED_FRAMEWORK_VERSION

    if conf.get_bool("UNIFIED_TECTON_OBJECTS_ENABLED"):
        return unified_feature_view.FeatureTable._from_spec(feature_table_spec, fco_container)

    return FeatureTable(ft_proto, fco_container)
