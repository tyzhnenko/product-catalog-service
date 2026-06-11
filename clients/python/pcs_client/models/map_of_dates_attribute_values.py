from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="MapOfDatesAttributeValues")


@_attrs_define
class MapOfDatesAttributeValues:
    """Map of date values"""

    additional_properties: dict[str, datetime.date] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.isoformat()

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        map_of_dates_attribute_values = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = isoparse(prop_dict).date()

            additional_properties[prop_name] = additional_property

        map_of_dates_attribute_values.additional_properties = additional_properties
        return map_of_dates_attribute_values

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> datetime.date:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: datetime.date) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
