from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="IntegerRangeAttribute")


@_attrs_define
class IntegerRangeAttribute:
    """
    Attributes:
        name (str): Name of the attribute
        min_value (int): Integer value
        max_value (int): Integer value
        type_ (Literal['integer_range'] | Unset):  Default: 'integer_range'.
    """

    name: str
    min_value: int
    max_value: int
    type_: Literal["integer_range"] | Unset = "integer_range"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        min_value = self.min_value

        max_value = self.max_value

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "min_value": min_value,
                "max_value": max_value,
            }
        )
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        min_value = d.pop("min_value")

        max_value = d.pop("max_value")

        type_ = cast(Literal["integer_range"] | Unset, d.pop("type", UNSET))
        if type_ != "integer_range" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'integer_range', got '{type_}'")

        integer_range_attribute = cls(
            name=name,
            min_value=min_value,
            max_value=max_value,
            type_=type_,
        )

        integer_range_attribute.additional_properties = d
        return integer_range_attribute

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
