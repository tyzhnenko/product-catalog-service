from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="IntegerAttribute")


@_attrs_define
class IntegerAttribute:
    """
    Attributes:
        name (str): Name of the attribute
        value (int): Integer value
        type_ (Literal['integer'] | Unset):  Default: 'integer'.
    """

    name: str
    value: int
    type_: Literal["integer"] | Unset = "integer"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        value = self.value

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "value": value,
            }
        )
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        value = d.pop("value")

        type_ = cast(Literal["integer"] | Unset, d.pop("type", UNSET))
        if type_ != "integer" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'integer', got '{type_}'")

        integer_attribute = cls(
            name=name,
            value=value,
            type_=type_,
        )

        integer_attribute.additional_properties = d
        return integer_attribute

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
