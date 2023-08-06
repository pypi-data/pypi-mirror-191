from functools import wraps
from typing import Callable
from typing import Optional
from typing import Tuple

from tecton import conf
from tecton._internals import errors
from tecton.unified import common
from tecton.unified import validations_api


# TODO(jake): Need to distinguish between two cases.
# 1) requires_validation on a public method. Should trigger automatic validation.
# 2) requires_validation on a private method as an assertion and documentation.
def requires_validation(func):
    """Check if the object has been validated, if not validate the object."""

    @wraps(func)
    def wrapper(fco_object: common.BaseTectonObject, *args, **kwargs):
        if fco_object._is_valid:
            return func(fco_object, *args, **kwargs)

        if conf.get_or_none("TECTON_VALIDATION_MODE") == validations_api.ValidationMode.AUTOMATIC:
            fco_object.validate()
        else:
            raise errors.TECTON_OBJECT_REQUIRES_VALIDATION(func.__name__, type(fco_object).__name__, fco_object.name)

        return func(fco_object, *args, **kwargs)

    return wrapper


def requires_remote_object(
    original_function: Optional[Callable] = None,
    *,
    error_message: Callable[[str], Exception] = errors.INVALID_USAGE_FOR_LOCAL_TECTON_OBJECT,
):
    """Assert this function is being called on a remote Tecton object, aka an object applied and fetched from the backend, and raise error otherwise.

    :param: error_message: error message to raise if the Tecton object is locally defined. The error_message param must contain a function that takes
    in the target function's name as a param and returns an Exception.
    """

    def inner_decorater(target):
        @wraps(target)
        def wrapper(fco_object: common.BaseTectonObject, *args, **kwargs):
            if fco_object.info._is_local_object:
                raise error_message(target.__name__)
            return target(fco_object, *args, **kwargs)

        return wrapper

    if original_function:
        return inner_decorater(original_function)

    return inner_decorater


def requires_local_object(
    original_function: Optional[Callable] = None,
    *,
    error_message: Callable[[str], Exception] = errors.INVALID_USAGE_FOR_REMOTE_TECTON_OBJECT,
):
    """Assert this function is being called on a local Tecton object, aka an object created locally (as opposed to being fetched from the backend).

    :param: error_message: error message to raise if the Tecton object is not locally defined. The error_message param must contain a function that takes
    in the target function's name as a param and returns an Exception.
    """

    def inner_decorater(target):
        @wraps(target)
        def wrapper(fco_object: common.BaseTectonObject, *args, **kwargs):
            if not fco_object.info._is_local_object:
                raise error_message(target.__name__)
            return target(fco_object, *args, **kwargs)

        return wrapper

    if original_function:
        return inner_decorater(original_function)

    return inner_decorater


def short_tecton_objects_repr(tecton_objects: Tuple[common.BaseTectonObject]) -> str:
    """Returns a shortened printable representation for a tuple of Tecton objects. Used for printing summaries."""
    short_strings = tuple(short_tecton_object_repr(obj) for obj in tecton_objects)
    return repr(short_strings)


def short_tecton_object_repr(tecton_object: common.BaseTectonObject) -> str:
    """Returns a shortened printable representation for a Tecton object. Used for printing summaries."""
    return f"{type(tecton_object).__name__}('{tecton_object.info.name}')"
