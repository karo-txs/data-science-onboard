from typing import _GenericAlias, get_args, Any, Type
from dataclasses import fields, is_dataclass
import copy


class TypeDict(dict):
    """Provides a custom dict with original type."""

    def __init__(self, _type: Type, *args, **kwargs):
        """Constructor.

        Args:
            _type (type): An original type for dict object.
        """
        super(TypeDict, self).__init__(*args, **kwargs)

        if not isinstance(_type, type):
            raise TypeError("t must be a type")

        self._type = _type

    @property
    def type(self) -> Type:
        """Gets the original type for dict object.

        Returns:
            Type: An original type for dict object.
        """
        return self._type


def __from_dict_to_type_dict(base_type: Type, obj: Any) -> TypeDict:
    """Function to converts dict objects in TypeDict based on dataclasses.

    Args:
        base_type (Type): A dataclass instance.
        obj (Any): A dataclass instance.

    Returns:
        TypeDict: A TypeDict object.
    """

    if is_dataclass(base_type):
        result = {}
        for name, data in obj.items():
            field = base_type.__dataclass_fields__.get(name)
            result[name] = __from_dict_to_type_dict(field.type, data)
        return TypeDict(base_type, result)

    elif isinstance(base_type, _GenericAlias):
        _types = get_args(base_type)

        if len(_types) > 0:
            for _type in _types:
                if isinstance(obj, (list, tuple)):
                    return type(obj)(__from_dict_to_type_dict(_type, v) for v in obj)

    elif isinstance(obj, (list, tuple)):
        return type(obj)(__from_dict_to_type_dict(type(v), v) for v in obj)

    elif isinstance(obj, dict):
        return type(obj)(
            (k, __from_dict_to_type_dict(type(v), v)) for k, v in obj.items()
        )
    else:
        return copy.deepcopy(obj)


def __todict_inner(obj: Any) -> Any:
    """Converts a dataclass instance in a dict object.

    Args:
        obj (Any): A dataclass instance.

    Returns:
        Any: An object.
    """
    if is_dataclass_instance(obj):
        result = []
        for f in fields(obj):
            value = __todict_inner(getattr(obj, f.name))
            result.append((f.name, value))
        return TypeDict(type(obj), result)

    elif isinstance(obj, tuple) and hasattr(obj, "_fields"):
        return type(obj)(*[__todict_inner(v) for v in obj])
    elif isinstance(obj, (list, tuple)):
        return type(obj)(__todict_inner(v) for v in obj)
    elif isinstance(obj, dict):
        return type(obj)((__todict_inner(k), __todict_inner(v)) for k, v in obj.items())
    else:
        return copy.deepcopy(obj)


def __fromdict_inner(obj: Any) -> Any:
    """Converts an object in an arbitrary object (normally, a dataclass).

    Args:
        obj (Any): An object.

    Returns:
        Any: An arbitrary object.
    """
    # reconstruct the dataclass using the type tag
    if is_dataclass_dict(obj):
        result = {}
        for name, data in obj.items():
            result[name] = __fromdict_inner(data)
        return obj.type(**result)

    # exactly the same as before (without the tuple clause)
    elif isinstance(obj, (list, tuple)):
        return type(obj)(__fromdict_inner(v) for v in obj)
    elif isinstance(obj, dict):
        return type(obj)(
            (__fromdict_inner(k), __fromdict_inner(v)) for k, v in obj.items()
        )
    else:
        return copy.deepcopy(obj)


def from_dict_to_type_dict(base_type: Any, _dict: dict) -> TypeDict:
    """Converts a dict object in a TypeDict object.

    Args:
        base_type (Any): A dataclass.
        _dict (dict): A dict object.

    Returns:
        TypeDict: A TypeDict object.
    """
    if is_dataclass(base_type):
        result = {}
        for name, data in _dict.items():
            field = base_type.__dataclass_fields__.get(name)
            result[name] = from_dict_to_type_dict(field.type, data)
        return TypeDict(base_type, _dict)


# copy of the internal function _is_dataclass_instance
def is_dataclass_instance(obj: Any) -> bool:
    """Checks if the object is a dataclass instance.

    Args:
        obj (Any): An arbitrary object.

    Returns:
        bool: True if obj is dataclass, otherwise False.
    """
    return is_dataclass(obj)


# the adapted version of asdict
def to_dict(obj: Any) -> dict:
    """Converts a dataclass instance in a dict.

    Args:
        obj (Any): A dataclass instance.

    Returns:
        dict: A dict object.
    """
    if obj is None:
        return {}

    if not is_dataclass_instance(obj):
        raise TypeError("to_dict() should be called on dataclass instances")
    return __todict_inner(obj)


def is_dataclass_dict(obj: Any) -> bool:
    """Checks if the object is an instance of the TypeDict.

    Args:
        obj (Any): A object.

    Returns:
        bool: True if obj is TypeDict, otherwise False.
    """
    return isinstance(obj, TypeDict)


def from_dict(_class: Type, _dict: dict) -> Any:
    """Converts a dict in a dataclass instance.

    Args:
        _class (Type): A dataclass class.
        _dict (dict): A dict object.

    Returns:
        Any: An dataclass instance.
    """
    return __fromdict_inner(__from_dict_to_type_dict(_class, _dict))
