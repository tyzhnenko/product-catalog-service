from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ListOfDateTimesAttribute")


@_attrs_define
class ListOfDateTimesAttribute:
    """
    Attributes:
        name (str): Name of the attribute
        values (list[datetime.datetime]): List of datetime values
        type_ (Literal['list_of_datetimes'] | Unset):  Default: 'list_of_datetimes'.
    """

    name: str
    values: list[datetime.datetime]
    type_: Literal["list_of_datetimes"] | Unset = "list_of_datetimes"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        values = []
        for values_item_data in self.values:
            values_item = values_item_data.isoformat()
            values.append(values_item)

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "values": values,
            }
        )
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        values = []
        _values = d.pop("values")
        for values_item_data in _values:
            values_item = isoparse(values_item_data)

            values.append(values_item)

        type_ = cast(Literal["list_of_datetimes"] | Unset, d.pop("type", UNSET))
        if type_ != "list_of_datetimes" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'list_of_datetimes', got '{type_}'")

        list_of_date_times_attribute = cls(
            name=name,
            values=values,
            type_=type_,
        )

        list_of_date_times_attribute.additional_properties = d
        return list_of_date_times_attribute

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
