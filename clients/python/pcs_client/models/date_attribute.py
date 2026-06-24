from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="DateAttribute")


@_attrs_define
class DateAttribute:
    """
    Attributes:
        name (str): Name of the attribute
        value (datetime.date): Date value in ISO 8601 format
        type_ (Literal['date'] | Unset):  Default: 'date'.
    """

    name: str
    value: datetime.date
    type_: Literal["date"] | Unset = "date"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        value = self.value.isoformat()

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

        value = datetime.date.fromisoformat(d.pop("value"))

        type_ = cast(Literal["date"] | Unset, d.pop("type", UNSET))
        if type_ != "date" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'date', got '{type_}'")

        date_attribute = cls(
            name=name,
            value=value,
            type_=type_,
        )

        date_attribute.additional_properties = d
        return date_attribute

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
