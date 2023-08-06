from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import attrs
from typeguard import typechecked

from tecton._internals import display
from tecton._internals import fco as internal_fco
from tecton._internals import metadata_service
from tecton._internals import sdk_decorators
from tecton.declarative import base as declarative_base
from tecton.unified import common as unified_common
from tecton.unified import utils as unified_utils
from tecton.unified import validations_api
from tecton_core import feature_definition_wrapper
from tecton_core import id_helper
from tecton_core import specs
from tecton_proto.args import basic_info_pb2
from tecton_proto.args import entity_pb2 as entity__args_pb2
from tecton_proto.args import fco_args_pb2
from tecton_proto.common import fco_locator_pb2
from tecton_proto.metadataservice import metadata_service_pb2
from tecton_proto.validation import validator_pb2


@attrs.define(eq=False)
class Entity(unified_common.BaseTectonObject, declarative_base.BaseEntity):
    """Tecton class for entities.

    Attributes:
        _spec:  An entity spec, i.e. a dataclass representation of the Tecton object that is used in most functional
            use cases, e.g. constructing queries. Set only after the object has been validated. Remote objects, i.e.
            applied objects fetched from the backend, are assumed valid.
        _args: A Tecton "args" proto. Only set if this object was defined locally, i.e. this object was not applied
            and fetched from the Tecton backend.


    """

    _spec: Optional[specs.EntitySpec] = attrs.field(repr=False)
    _args: Optional[entity__args_pb2.EntityArgs] = attrs.field(repr=False, on_setattr=attrs.setters.frozen)

    @typechecked
    def __init__(
        self,
        *,
        name: str,
        description: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None,
        owner: Optional[str] = None,
        prevent_destroy: bool = False,
        join_keys: Optional[Union[str, List[str]]] = None,
    ):
        """
        Declare a new Entity.

        :param name: Unique name for the new entity.
        :param description: Short description of the new entity.
        :param tags: Tags associated with this Tecton Object (key-value pairs of arbitrary metadata).
        :param owner: Owner name (typically the email of the primary maintainer).
        :param prevent_destroy: If True, this Tecton object will be blocked from being deleted or re-created (i.e. a
            destructive update) during tecton plan/apply. To remove or update this object, `prevent_destroy` must be
            first set to False via a separate tecton apply. `prevent_destroy` can be used to prevent accidental changes
            such as inadvertantly deleting a Feature Service used in production or recreating a Feature View that
            triggers expensive rematerialization jobs. `prevent_destroy` also blocks changes to dependent Tecton objects
            that would trigger a recreate of the tagged object, e.g. if `prevent_destroy` is set on a Feature Service,
            that will also prevent deletions or re-creates of Feature Views used in that service. `prevent_destroy` is
            only enforced in live (i.e. non-dev) workspaces.
        :param join_keys: Names of columns that uniquely identify the entity in FeatureView's SQL statement
            for which features should be aggregated. Defaults to using ``name`` as the entity's join key.

        :raises TectonValidationError: if the input non-parameters are invalid.
        """
        from tecton.cli import common as cli_common

        if not join_keys:
            resolved_join_keys = [name]
        elif isinstance(join_keys, str):
            resolved_join_keys = [join_keys]
        else:
            resolved_join_keys = join_keys

        args = entity__args_pb2.EntityArgs(
            entity_id=id_helper.IdHelper.generate_id(),
            info=basic_info_pb2.BasicInfo(name=name, description=description, tags=tags, owner=owner),
            join_keys=resolved_join_keys,
            version=feature_definition_wrapper.FrameworkVersion.FWV5.value,
            prevent_destroy=prevent_destroy,
        )
        info = unified_common.TectonObjectInfo.from_args_proto(args.info, args.entity_id)
        source_info = cli_common.construct_fco_source_info(args.entity_id)
        self.__attrs_init__(info=info, spec=None, args=args, source_info=source_info)
        internal_fco.Fco._register(self)

    @classmethod
    @typechecked
    def _from_spec(cls, spec: specs.EntitySpec) -> "Entity":
        """Create an Entity from directly from a spec. Specs are assumed valid and will not be re-validated."""
        info = unified_common.TectonObjectInfo.from_spec(spec)
        obj = cls.__new__(cls)  # Instantiate the object. Does not call init.
        obj.__attrs_init__(info=info, spec=spec, args=None, source_info=None)
        return obj

    @unified_utils.requires_local_object
    def _build_args(self) -> fco_args_pb2.FcoArgs:
        return fco_args_pb2.FcoArgs(entity=self._args)

    def _build_fco_validation_args(self) -> validator_pb2.FcoValidationArgs:
        if self.info._is_local_object:
            return validator_pb2.FcoValidationArgs(
                entity=validator_pb2.EntityValidationArgs(
                    args=self._args,
                )
            )
        else:
            return validator_pb2.FcoValidationArgs(entity=self._spec.data_proto.validation_args)

    @property
    def _is_valid(self) -> bool:
        return self._spec is not None

    @property
    def join_keys(self) -> List[str]:
        """Join keys of the entity."""
        if self._spec is None:
            return list(self._args.join_keys)
        return list(self._spec.join_keys)

    def _validate(self, indentation_level: int = 0) -> None:
        if self._is_valid:
            return

        validations_api.run_backend_validation_and_assert_valid(
            self,
            validator_pb2.ValidationRequest(validation_args=[self._build_fco_validation_args()]),
            indentation_level,
        )

        self._spec = specs.EntitySpec.from_args_proto(self._args)

    @sdk_decorators.sdk_public_method
    @unified_utils.requires_remote_object
    def summary(self) -> display.Displayable:
        """Displays a human readable summary of this Feature View."""
        request = metadata_service_pb2.GetEntitySummaryRequest(
            fco_locator=fco_locator_pb2.FcoLocator(id=self._spec.id_proto, workspace=self._spec.workspace)
        )
        response = metadata_service.instance().GetEntitySummary(request)
        return display.Displayable.from_fco_summary(response.fco_summary)

    @unified_utils.requires_local_object
    def _create_unvalidated_spec(self) -> specs.EntitySpec:
        """Create an unvalidated spec. Used for user unit testing, where backend validation is unavailable."""
        return specs.EntitySpec.from_args_proto(self._args)
