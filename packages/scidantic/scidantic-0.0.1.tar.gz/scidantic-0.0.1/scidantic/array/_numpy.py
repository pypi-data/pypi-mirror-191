from typing import TYPE_CHECKING, Any, Dict, List, Union

import numpy as np

from scidantic.array._base import DType, _ArrayBase

if TYPE_CHECKING:
    from pydantic.fields import ModelField

    _NumpyNDArrayType = np.ndarray[Any, Any]
else:
    _NumpyNDArrayType = np.ndarray


_NUMPY_DTYPE_KIND_TO_SCIDANTIC = {
    "b": "bool",
    "c": "complex",
    "f": "float",
    "i": "int",
    "u": "uint",
}

_SCIDANTIC_TO_NUMPY_DTYPE: Dict[str, Dict[int, Any]] = {
    "bool": {
        8: np.bool_,
    },
    "complex": {
        64: np.complex64,
        128: np.complex128,
    },
    "float": {
        16: np.float16,
        32: np.float32,
        64: np.float64,
    },
    "int": {
        8: np.int8,
        16: np.int16,
        32: np.int32,
        64: np.int64,
    },
    "uint": {
        8: np.uint8,
        16: np.uint16,
        32: np.uint32,
        64: np.uint64,
    },
}


class NumpyArray(_ArrayBase[DType, _NumpyNDArrayType], _NumpyNDArrayType):
    transform_list_to_array = True

    @classmethod
    def validate(
        cls,
        v: Union[List[Union[int, float, bool]], _NumpyNDArrayType],
        field: "ModelField",
    ) -> _NumpyNDArrayType:
        if not isinstance(v, np.ndarray) and not cls.transform_list_to_array:
            raise TypeError(
                "Expected `np.ndarray`, but got `list`. If you want scidantic to"
                " transform the list to an array, use `NumpyArray[...]` instead of"
                " `StrictNumpyArray[...] as attribute type."
            )

        subfield_type = cls._get_array_type(field)

        if isinstance(v, list):
            dtype = _SCIDANTIC_TO_NUMPY_DTYPE[subfield_type._type][subfield_type._bits]
            v = np.array(v, dtype=dtype)
            return super().validate(v, field)

        c_contiguous = field.field_info.extra.get("c_contiguous", False)
        if c_contiguous and not v.flags.c_contiguous:
            raise TypeError(
                "Expected array to be C-contiguous, but got array that is not"
                " C-contiguous."
            )

        f_contiguous = field.field_info.extra.get("f_contiguous", False)
        if f_contiguous and not v.flags.f_contiguous:
            raise TypeError(
                "Expected array to be F-contiguous, but got array that is not"
                " F-contiguous."
            )

        v_bits = v.dtype.itemsize * 8
        v_type = _NUMPY_DTYPE_KIND_TO_SCIDANTIC[v.dtype.kind]
        # The array generic type used is `Float`, `Integer`, etc, so `_bits` is
        # `None`. Defaulting to 64 bits.
        if v_bits != subfield_type._bits or v_type != subfield_type._type:
            raise TypeError(
                "Expected array of dtype"
                f" `{subfield_type._type}{subfield_type._bits}`, but got array of"
                f" dtype `{v_type}{v_bits}`"
            )

        return super().validate(v, field)


class StrictNumpyArray(NumpyArray[DType]):
    transform_list_to_array = False
