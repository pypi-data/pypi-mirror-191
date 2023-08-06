from enum import Enum
from typing import List
from typing import Sequence
from typing import Tuple

from colorama import Fore
from typeguard import typechecked

from tecton import version as tecton_version
from tecton._internals import metadata_service
from tecton.unified import common as unified_common
from tecton_core import conf
from tecton_core import errors
from tecton_core import id_helper
from tecton_proto.args import fco_args_pb2
from tecton_proto.args import repo_metadata_pb2
from tecton_proto.data import state_update_pb2
from tecton_proto.metadataservice import metadata_service_pb2
from tecton_proto.validation import validator_pb2


class ValidationMode(str, Enum):
    EXPLICIT = "explicit"
    AUTOMATIC = "auto"


_INDENTATION_SIZE = 4


def set_validation_mode(mode: ValidationMode):
    """Convenience utility to set the Tecton object validation mode for the lifetime of the Python process.

    Must be either "explicit" (tecton.ValidationMode.EXPLICIT) or "auto" (tecton.ValidationMode.AUTOMATIC). "explicit"
    is the default.

    In "auto" mode, locally defined Tecton objects will automatically trigger validation when needed.

    .. code-block:: python

        import tecton

        tecton.set_validation_mode("auto")

        credit_scores_batch = tecton.BatchSource(
            name='credit_scores_batch',
            batch_config=tecton.HiveConfig(database='demo_fraud', table='credit_scores'),
        )

        df = credit_scores_batch.get_dataframe()  # Will automatically trigger validation.

    In "explicit" mode, locally defined Tecton objects must be validated before they can be used to execute many
    methods.

    .. code-block:: python

        import tecton

        tecton.set_validation_mode("auto")

        credit_scores_batch = tecton.BatchSource(
            name='credit_scores_batch',
            batch_config=tecton.HiveConfig(database='demo_fraud', table='credit_scores'),
        )

        credit_scores_batch.validate()

        df = credit_scores_batch.get_dataframe()


    Note: Tecton objects fetched from the Tecton backend have already been validated during `tecton plan` and do
    not need to be re-validated.
    """
    if mode is None or mode.lower() not in (ValidationMode.AUTOMATIC, ValidationMode.EXPLICIT):
        raise ValueError(f"Mode should be one of 'auto' or 'explicit', got {mode}")
    conf.set("TECTON_VALIDATION_MODE", mode)


def _get_validation_prefix(obj: unified_common.BaseTectonObject, indentation_level: int) -> str:
    indent_prefix = " " * (indentation_level * _INDENTATION_SIZE)
    return f"{indent_prefix}{obj.__class__.__name__} '{obj.name}': "


def print_validation_success(
    obj: unified_common.BaseTectonObject,
    indentation_level: int,
) -> None:
    prefix = _get_validation_prefix(obj, indentation_level)
    print(f"{prefix}Successfully validated.")


def print_validating_dependencies(
    obj: unified_common.BaseTectonObject,
    dependencies: Sequence[unified_common.BaseTectonObject],
    indentation_level: int,
) -> None:
    num_unvalidated_dependencies = len([dep for dep in dependencies if not dep._is_valid])
    if num_unvalidated_dependencies == 0:
        return

    prefix = _get_validation_prefix(obj, indentation_level)
    num_validated_dependencies = len(dependencies) - num_unvalidated_dependencies

    cache_message = f" ({num_validated_dependencies} already validated.)" if num_validated_dependencies > 0 else ""
    dependency_string = "dependency" if num_unvalidated_dependencies == 1 else "dependencies"
    print(f"{prefix}Validating {num_unvalidated_dependencies} unvalidated {dependency_string}." + cache_message)


def print_deriving_schemas(
    obj: unified_common.BaseTectonObject,
    indentation_level: int,
) -> None:
    prefix = _get_validation_prefix(obj, indentation_level)
    print(f"{prefix}Deriving schema.")


# Copy of logic in engine.py - but using unified objects for notebook development.
def _get_declared_fco_args(
    objects: List[unified_common.BaseTectonObject],
) -> Tuple[List[fco_args_pb2.FcoArgs], repo_metadata_pb2.FeatureRepoSourceInfo]:
    all_args = []
    repo_source_info = repo_metadata_pb2.FeatureRepoSourceInfo()

    for fco_obj in objects:
        source_info = fco_obj._source_info
        source_info.fco_id.CopyFrom(id_helper.IdHelper.from_string(fco_obj.info.id))

        repo_source_info.source_info.append(source_info)
        all_args.append(fco_obj._build_args())

    return all_args, repo_source_info


def format_server_errors(obj: unified_common.BaseTectonObject, errors: List[state_update_pb2.ValidationMessage]) -> str:
    error_strings = [f"{obj.__class__.__name__} '{obj.info.name}' failed validation with following errors:"]
    for err in errors:
        err_obj_id = id_helper.IdHelper.to_string(err.fco_refs[0].fco_id)

        if err_obj_id != obj.id:
            raise errors.TectonInternalError(
                f"Backend validation error returned wrong object id: {err_obj_id}. Expected {obj.id}"
            )

        error_strings.append(Fore.RED + err.message + Fore.RESET)

    return "\n".join(error_strings)


@typechecked
def run_backend_validation_and_assert_valid(
    obj: unified_common.BaseTectonObject, validation_request: validator_pb2.ValidationRequest, indentation_level: int
) -> None:
    """Run validation against the Tecton backend.

    Raises an exception if validation fails. Prints message if successful.
    """
    validation_request = metadata_service_pb2.ValidateLocalFcoRequest(
        sdk_version=tecton_version.get_semantic_version() or "",
        validation_request=validation_request,
    )
    response = metadata_service.instance().ValidateLocalFco(validation_request).response_proto
    if response.success:
        print_validation_success(obj, indentation_level)
    else:
        raise errors.TectonValidationError(format_server_errors(obj, response.validation_result.errors))
