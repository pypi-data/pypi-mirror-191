import numpy as np
import pytest
from pydantic import Field
from pydantic.config import BaseConfig
from pydantic.fields import ModelField

from scidantic.array._base import _ArrayBase, _DTypeBase


class DummyDType(_DTypeBase):
    _type = "dummy"
    _bits = 8


def test_dtypebase_modify_schema() -> None:
    """Test `scidantic.array._base._DTypeBase.__modify_schema__` method."""
    field_schema = {}
    DummyDType.__modify_schema__(field_schema=field_schema)
    assert field_schema == {"type": "dummy", "bits": 8}


def test_arraybase_validate() -> None:
    """Test `scidantic.array._base._ArrayBase.validate` method."""
    v = np.array([1, 2, 3])
    field = ModelField(
        name="test",
        type_=_ArrayBase[DummyDType, None],
        class_validators={},
        model_config=BaseConfig(),
        field_info=Field(..., shape=(3,)),
    )
    assert _ArrayBase.validate(v=v, field=field) is v


def test_arraybase_validate_raise_typeerror_when_shape_is_not_list_or_tuple() -> None:
    """Test `scidantic.array._base._ArrayBase.validate` method raises `TypeError`
    when the `shape` argument is not a `list` or `tuple`."""
    with pytest.raises(
        TypeError,
        match=(
            r"shape argument was provided using Field, but its value is not a list or"
            r" tuple: 1 \(`int`\)"
        ),
    ):
        _ArrayBase.validate(
            v=[1, 2, 3],
            field=ModelField(
                name="test",
                type_=_ArrayBase[DummyDType, None],
                class_validators={},
                model_config=BaseConfig(),
                field_info=Field(..., shape=1),
            ),
        )


def test_arraybase_validate_raise_valueerror() -> None:
    """Test `scidantic.array._base._ArrayBase.validate` method raises `ValueError`
    when the `shape` of the array does not match the `shape` argument."""
    with pytest.raises(ValueError):
        _ArrayBase.validate(
            v=np.array([1, 2, 3]),
            field=ModelField(
                name="test",
                type_=_ArrayBase[DummyDType, None],
                class_validators={},
                model_config=BaseConfig(),
                field_info=Field(..., shape=(2, 2)),
            ),
        )


def test_arraybase_modify_schema() -> None:
    """Test `scidantic.array._base._ArrayBase.__modify_schema__` method."""
    field_schema = {}
    _ArrayBase.__modify_schema__(field_schema=field_schema)
    assert field_schema == {"type": "array"}


def test_arraybase_get_array_type() -> None:
    """Test `scidantic.array._base._ArrayBase._get_array_type` method."""
    assert DummyDType == _ArrayBase._get_array_type(
        field=ModelField(
            name="test",
            type_=_ArrayBase[DummyDType, None],
            class_validators={},
            model_config=BaseConfig(),
        )
    )


def test_arraybase_get_array_type_raise_typeerror_when_no_subfield() -> None:
    """Test `scidantic.array._base._ArrayBase._get_array_type` method raises `TypeError`
    when the `ModelField` passed does not have a `sub_fields` attribute."""
    with pytest.raises(
        TypeError,
        match=r"field 'test' must be an array with a single type, but got no type",
    ):
        _ArrayBase._get_array_type(
            field=ModelField(
                name="test",
                type_=_ArrayBase,
                class_validators={},
                model_config=BaseConfig(),
            )
        )


def test_arraybase_get_array_type_raise_typeerror_when_subfield_is_not_dtypebase() -> (
    None
):
    """Test `scidantic.array._base._ArrayBase._get_array_type` method raises `TypeError`
    when the `ModelField` passed first `sub_fields` attribute is not a `_DTypeBase`."""
    with pytest.raises(
        TypeError,
        match=(
            r"field 'test' must be an array with a type, imported from"
            r" `scidantic.array`, like `UInt`, but got `int`"
        ),
    ):
        _ArrayBase._get_array_type(
            field=ModelField(
                name="test",
                type_=_ArrayBase[int, None],
                class_validators={},
                model_config=BaseConfig(),
            )
        )
