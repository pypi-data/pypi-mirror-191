from typing import TYPE_CHECKING, List, Type, Union

import numpy as np
import pytest
from pydantic import BaseModel, Field
from pydantic.config import BaseConfig
from pydantic.fields import ModelField

from scidantic.array._base import (
    Bool,
    Complex,
    Complex64,
    Complex128,
    Float,
    Float16,
    Float32,
    Float64,
    Int,
    Int8,
    Int16,
    Int32,
    Int64,
    UInt,
    UInt8,
    UInt16,
    UInt32,
    UInt64,
)
from scidantic.array._numpy import NumpyArray, StrictNumpyArray

if TYPE_CHECKING:
    from scidantic.array._base import _DTypeBase


@pytest.mark.parametrize(
    "value",
    [
        [1, 2, 3],
        np.array([1, 2, 3], dtype=np.float64),
    ],
)
def test_numpyarray_validate(value: Union[List[int], np.ndarray]) -> None:
    """Test `scidantic.array._numpy.NumpyArray.validate` method."""
    field = ModelField(
        name="test",
        type_=NumpyArray[Float64],
        class_validators={},
        model_config=BaseConfig(),
        field_info=Field(..., shape=(3,)),
    )
    np.allclose(NumpyArray.validate(v=value, field=field), value)


def test_numpyarray_validate_raise_typeerror_when_wrong_dtype() -> None:
    """Test `scidantic.array._numpy.NumpyArray.validate` method raises `TypeError` when
    the array dtype is not the expected one."""
    with pytest.raises(
        TypeError,
        match="Expected array of dtype `float64`, but got array of dtype `int64`",
    ):
        NumpyArray.validate(
            v=np.array([1, 2, 3], dtype=np.int64),
            field=ModelField(
                name="test",
                type_=NumpyArray[Float64],
                class_validators={},
                model_config=BaseConfig(),
                field_info=Field(..., shape=(3,)),
            ),
        )


def test_strictnumpyarray_validate_raise_typeerror_when_v_not_numpy_array() -> None:
    """Test `scidantic.array._numpy.NumpyArray.validate` method raises `TypeError` when
    the `v` argument is not a `numpy.ndarray`."""
    with pytest.raises(
        TypeError,
        match=(
            r"Expected `np.ndarray`, but got `list`. If you want scidantic to"
            r" transform the list to an array, use `NumpyArray\[...\]` instead of"
            r" `StrictNumpyArray\[...\] as attribute type."
        ),
    ):
        StrictNumpyArray.validate(
            [1, 2, 3],
            field=ModelField(
                name="test",
                type_=StrictNumpyArray[Float64],
                class_validators={},
                model_config=BaseConfig(),
                field_info=Field(..., shape=(3,)),
            ),
        )


def test_numpyarray_validate_raise_typeerror_when_not_c_contiguous() -> None:
    """Test `scidantic.array._numpy.NumpyArray.validate` method raises `TypeError` when
    the array is not C-contiguous."""
    with pytest.raises(
        TypeError,
        match=(
            r"Expected array to be C-contiguous, but got array that is not"
            r" C-contiguous."
        ),
    ):
        NumpyArray.validate(
            v=np.array([[1, 2, 3], [4, 5, 6]], dtype=np.float64).T,
            field=ModelField(
                name="test",
                type_=NumpyArray[Float64],
                class_validators={},
                model_config=BaseConfig(),
                field_info=Field(..., c_contiguous=True),
            ),
        )


def test_numpyarray_validate_raise_typeerror_when_not_f_contiguous() -> None:
    """Test `scidantic.array._numpy.NumpyArray.validate` method raises `TypeError` when
    the array is not F-contiguous."""
    with pytest.raises(
        TypeError,
        match=(
            r"Expected array to be F-contiguous, but got array that is not"
            r" F-contiguous."
        ),
    ):
        NumpyArray.validate(
            v=np.array([[1, 2, 3], [4, 5, 6]], dtype=np.float64),
            field=ModelField(
                name="test",
                type_=NumpyArray[Float64],
                class_validators={},
                model_config=BaseConfig(),
                field_info=Field(..., f_contiguous=True),
            ),
        )


@pytest.mark.parametrize(
    "value, dtype, numpy_dtype",
    [
        ([True, True, False], Bool, np.bool_),
        ([1 + 1j, 2 + 2j, 3 + 3j], Complex, np.complex_),
        ([1 + 1j, 2 + 2j, 3 + 3j], Complex64, np.complex64),
        ([1 + 1j, 2 + 2j, 3 + 3j], Complex128, np.complex128),
        ([1.0, 2.0, 3.0], Float, np.float_),
        ([1.0, 2.0, 3.0], Float16, np.float16),
        ([1.0, 2.0, 3.0], Float32, np.float32),
        ([1.0, 2.0, 3.0], Float64, np.float64),
        ([1, 2, 3], Int, np.int_),
        ([1, 2, 3], Int8, np.int8),
        ([1, 2, 3], Int16, np.int16),
        ([1, 2, 3], Int32, np.int32),
        ([1, 2, 3], Int64, np.int64),
        ([1, 2, 3], UInt, np.uint),
        ([1, 2, 3], UInt8, np.uint8),
        ([1, 2, 3], UInt16, np.uint16),
        ([1, 2, 3], UInt32, np.uint32),
        ([1, 2, 3], UInt64, np.uint64),
    ],
)
def test_numpyarray(
    value: List[int], dtype: Type["_DTypeBase"], numpy_dtype: Type[np.number]
) -> None:
    """Test `scidantic.array._numpy.NumpyArray` field type."""

    class Model(BaseModel):
        array: NumpyArray[dtype] = Field(..., shape=(3,))

    model = Model(array=value)
    assert model.array.dtype == numpy_dtype


@pytest.mark.parametrize(
    "value, dtype, numpy_dtype",
    [
        (np.array([True, True, False], dtype=np.bool_), Bool, np.bool_),
        (np.array([1 + 1j, 2 + 2j, 3 + 3j], dtype=np.complex_), Complex, np.complex_),
        (
            np.array([1 + 1j, 2 + 2j, 3 + 3j], dtype=np.complex64),
            Complex64,
            np.complex64,
        ),
        (
            np.array([1 + 1j, 2 + 2j, 3 + 3j], dtype=np.complex128),
            Complex128,
            np.complex128,
        ),
        (np.array([1.0, 2.0, 3.0], dtype=np.float_), Float, np.float_),
        (np.array([1.0, 2.0, 3.0], dtype=np.float16), Float16, np.float16),
        (np.array([1.0, 2.0, 3.0], dtype=np.float32), Float32, np.float32),
        (np.array([1.0, 2.0, 3.0], dtype=np.float64), Float64, np.float64),
        (np.array([1, 2, 3], dtype=np.int_), Int, np.int_),
        (np.array([1, 2, 3], dtype=np.int8), Int8, np.int8),
        (np.array([1, 2, 3], dtype=np.int16), Int16, np.int16),
        (np.array([1, 2, 3], dtype=np.int32), Int32, np.int32),
        (np.array([1, 2, 3], dtype=np.int64), Int64, np.int64),
        (np.array([1, 2, 3], dtype=np.uint), UInt, np.uint),
        (np.array([1, 2, 3], dtype=np.uint8), UInt8, np.uint8),
        (np.array([1, 2, 3], dtype=np.uint16), UInt16, np.uint16),
        (np.array([1, 2, 3], dtype=np.uint32), UInt32, np.uint32),
        (np.array([1, 2, 3], dtype=np.uint64), UInt64, np.uint64),
    ],
)
def test_strictnumpyarray(
    value: List[int], dtype: Type["_DTypeBase"], numpy_dtype: Type[np.number]
) -> None:
    """Test `scidantic.array._numpy.StrictNumpyArray` field type."""

    class Model(BaseModel):
        array: StrictNumpyArray[dtype] = Field(..., shape=(3,))

    model = Model(array=value)
    assert model.array.dtype == numpy_dtype
