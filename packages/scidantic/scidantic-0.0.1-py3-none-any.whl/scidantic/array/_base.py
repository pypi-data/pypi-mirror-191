from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Generic,
    Protocol,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
)

if TYPE_CHECKING:
    from pydantic.fields import ModelField
    from pydantic.typing import CallableGenerator


class _DTypeBase:
    _type: str
    _bits: int

    @classmethod
    def __get_validators__(cls) -> "CallableGenerator":
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema: Dict[str, Any]) -> None:
        field_schema.update(type=cls._type, bits=cls._bits)

    @classmethod
    def validate(cls, v: "_DTypeBase", field: "ModelField") -> "_DTypeBase":
        return v


def _get_arch_bits() -> int:
    """Get the number of bits of the current architecture.

    Returns:
        The number of bits of the current architecture.
    """
    import struct

    return struct.calcsize("P") * 8


_ARCH_BITS = _get_arch_bits()


def _make_dtype(
    name: str, _type: str, bits: Union[int, None] = None
) -> Type[_DTypeBase]:
    """Make a new `_DTypeBase` subclass with the given name, type, and bits.

    Args:
        name: The name of the new class.
        _type: The type of the new class.
        bits: The number of bits of the new class.

    Returns:
        The new class.
    """
    return type(name, (_DTypeBase,), {"_type": _type, "_bits": bits})


Bool = _make_dtype("Bool", "bool", 8)
Complex = _make_dtype("Complex", "complex", 128)
Complex64 = _make_dtype("Complex64", "complex", 64)
Complex128 = _make_dtype("Complex128", "complex", 128)
Float = _make_dtype("Float", "float", _ARCH_BITS)
Float16 = _make_dtype("Float16", "float", 16)
Float32 = _make_dtype("Float32", "float", 32)
Float64 = _make_dtype("Float64", "float", 64)
Int = _make_dtype("Int", "int", _ARCH_BITS)
Int8 = _make_dtype("Int8", "int", 8)
Int16 = _make_dtype("Int16", "int", 16)
Int32 = _make_dtype("Int32", "int", 32)
Int64 = _make_dtype("Int64", "int", 64)
UInt = _make_dtype("UInt", "uint", _ARCH_BITS)
UInt8 = _make_dtype("UInt8", "uint", 8)
UInt16 = _make_dtype("UInt16", "uint", 16)
UInt32 = _make_dtype("UInt32", "uint", 32)
UInt64 = _make_dtype("UInt64", "uint", 64)


class _ArrayType(Protocol):
    @property
    def shape(self) -> Tuple[int, ...]:
        raise NotImplementedError


DType = TypeVar("DType", bound=_DTypeBase)
ArrayType = TypeVar("ArrayType", bound=_ArrayType)


class _ArrayBase(Generic[DType, ArrayType]):
    @classmethod
    def __get_validators__(cls) -> "CallableGenerator":
        yield cls.validate

    @classmethod
    def validate(cls, v: ArrayType, field: "ModelField") -> ArrayType:
        shape: Union[Tuple[int, ...], None] = field.field_info.extra.get("shape")
        if shape:
            if not isinstance(shape, (list, tuple)):
                raise TypeError(
                    "shape argument was provided using Field, but its value is not a"
                    f" list or tuple: {shape} (`{type(shape).__name__}`)"
                )

            if v.shape != shape:
                raise ValueError(
                    f"field '{field.name}' must be an array with shape {shape},"
                    f" but got {v.shape}"
                )

        return v

    @classmethod
    def __modify_schema__(cls, field_schema: Dict[str, Any]) -> None:
        field_schema.update(type="array")

    @staticmethod
    def _get_array_type(field: "ModelField") -> Type[_DTypeBase]:
        if not field.sub_fields:
            raise TypeError(
                f"field '{field.name}' must be an array with a single type,"
                " but got no type"
            )

        if not issubclass(field.sub_fields[0].type_, _DTypeBase):
            raise TypeError(
                f"field '{field.name}' must be an array with a type, imported from"
                " `scidantic.array`, like `UInt`, but got"
                f" `{field.sub_fields[0].type_.__name__}`"
            )

        return cast(Type[_DTypeBase], field.sub_fields[0].type_)
