from typing import List
from typing import Optional

from tecton._internals import metadata_service
from tecton._internals.display import Displayable
from tecton._internals.sdk_decorators import sdk_public_method
from tecton.fco import Fco
from tecton.interactive import materialization_api
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper
from tecton_core.feature_set_config import FeatureSetConfig
from tecton_core.id_helper import IdHelper
from tecton_core.logger import get_logger
from tecton_core.online_serving_index import OnlineServingIndex
from tecton_core.schema import Schema
from tecton_proto.data.materialization_status_pb2 import MaterializationStatus
from tecton_proto.metadataservice.metadata_service_pb2 import GetFeatureFreshnessRequest
from tecton_proto.metadataservice.metadata_service_pb2 import GetFeatureViewSummaryRequest

logger = get_logger("FeatureDefinition")


class FeatureDefinition(Fco):
    @property
    def _fco_metadata(self):
        return self._proto.fco_metadata

    @property
    def _view_schema(self):
        return Schema(self._proto.schemas.view_schema)

    @property
    def _materialization_schema(self):
        return Schema(self._proto.schemas.materialization_schema)

    @property
    def _id_proto(self):
        return self._proto.feature_view_id

    @property  # type: ignore
    @sdk_public_method
    def id(self) -> str:
        """
        Returns the id of this object
        """
        return IdHelper.to_string(self._id_proto)

    @property
    def join_keys(self) -> List[str]:
        """
        Returns the join key column names
        """
        return list(self._proto.join_keys)

    @property  # type: ignore
    @sdk_public_method
    def online_serving_index(self) -> OnlineServingIndex:
        """
        Returns Defines the set of join keys that will be indexed and queryable during online serving.
        Defaults to the complete join key.
        """
        return OnlineServingIndex.from_proto(self._proto.online_serving_index)

    @property
    def wildcard_join_key(self) -> Optional[str]:
        """
        Returns a wildcard join key column name if it exists;
        Otherwise returns None.
        """
        online_serving_index = self.online_serving_index
        wildcard_keys = [join_key for join_key in self.join_keys if join_key not in online_serving_index.join_keys]
        return wildcard_keys[0] if wildcard_keys else None

    @property  # type: ignore
    @sdk_public_method
    def entity_names(self) -> List[str]:
        """
        Returns the names of entities for this Feature View.
        """
        entity_specs = [self._fco_container.get_by_id_proto(id) for id in self._proto.entity_ids]
        return [entity.name for entity in entity_specs]

    @property
    def data_source_names(self) -> List[str]:
        """
        Returns the names of the data sources for this Feature View.
        """
        fd = FeatureDefinitionWrapper(self._spec, self._fco_container)
        return [ds.name for ds in fd.data_sources]

    @property
    def _timestamp_key(self) -> str:
        raise NotImplementedError

    @property  # type: ignore
    @sdk_public_method
    def features(self) -> List[str]:
        """
        Returns the names of the (output) features.
        """
        join_keys = self.join_keys
        timestamp_key = self._timestamp_key
        return [
            col_name
            for col_name in self._view_schema.column_names()
            if col_name not in join_keys and col_name != timestamp_key
        ]

    @property  # type: ignore
    @sdk_public_method
    def url(self) -> str:
        """
        Returns a link to the Tecton Web UI.
        """
        return self._proto.web_url

    @sdk_public_method
    def summary(self) -> Displayable:
        """
        Returns various information about this feature definition, including the most critical metadata such
        as the name, owner, features, etc.
        """
        request = GetFeatureViewSummaryRequest()
        request.fco_locator.id.CopyFrom(self._id_proto)
        request.fco_locator.workspace = self.workspace

        response = metadata_service.instance().GetFeatureViewSummary(request)

        return Displayable.from_fco_summary(response.fco_summary)

    def _construct_feature_set_config(self) -> FeatureSetConfig:
        feature_defintion = FeatureDefinitionWrapper(self._spec, self._fco_container)
        return FeatureSetConfig.from_feature_definition(feature_defintion)

    def _freshness(self):
        fresh_request = GetFeatureFreshnessRequest()
        fresh_request.fco_locator.id.CopyFrom(self._id_proto)
        fresh_request.fco_locator.workspace = self.workspace
        return metadata_service.instance().GetFeatureFreshness(fresh_request)

    def _get_materialization_status(self) -> MaterializationStatus:
        return materialization_api.get_materialization_status_response(self._id_proto)
