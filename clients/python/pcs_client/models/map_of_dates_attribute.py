from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.map_of_dates_attribute_values import MapOfDatesAttributeValues


T = TypeVar("T", bound="MapOfDatesAttribute")


@_attrs_define
class MapOfDatesAttribute:
    """
    Attributes:
        name (str): Name of the attribute
        values (MapOfDatesAttributeValues): Map of date values
        type_ (Literal['map_of_dates'] | Unset):  Default: 'map_of_dates'.
    """

    name: str
    values: MapOfDatesAttributeValues
    type_: Literal["map_of_dates"] | Unset = "map_of_dates"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        values = self.values.to_dict()

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
        from ..models.map_of_dates_attribute_values import MapOfDatesAttributeValues

        d = dict(src_dict)
        name = d.pop("name")

        values = MapOfDatesAttributeValues.from_dict(d.pop("values"))

        type_ = cast(Literal["map_of_dates"] | Unset, d.pop("type", UNSET))
        if type_ != "map_of_dates" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'map_of_dates', got '{type_}'")

        map_of_dates_attribute = cls(
            name=name,
            values=values,
            type_=type_,
        )

        map_of_dates_attribute.additional_properties = d
        return map_of_dates_attribute

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
