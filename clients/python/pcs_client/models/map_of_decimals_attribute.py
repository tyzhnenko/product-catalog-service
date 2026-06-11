from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.map_of_decimals_attribute_values import MapOfDecimalsAttributeValues


T = TypeVar("T", bound="MapOfDecimalsAttribute")


@_attrs_define
class MapOfDecimalsAttribute:
    """
    Attributes:
        name (str): Name of the attribute
        values (MapOfDecimalsAttributeValues): Map of decimal values
        type_ (Literal['map_of_decimals'] | Unset):  Default: 'map_of_decimals'.
    """

    name: str
    values: MapOfDecimalsAttributeValues
    type_: Literal["map_of_decimals"] | Unset = "map_of_decimals"
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
        from ..models.map_of_decimals_attribute_values import MapOfDecimalsAttributeValues

        d = dict(src_dict)
        name = d.pop("name")

        values = MapOfDecimalsAttributeValues.from_dict(d.pop("values"))

        type_ = cast(Literal["map_of_decimals"] | Unset, d.pop("type", UNSET))
        if type_ != "map_of_decimals" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'map_of_decimals', got '{type_}'")

        map_of_decimals_attribute = cls(
            name=name,
            values=values,
            type_=type_,
        )

        map_of_decimals_attribute.additional_properties = d
        return map_of_decimals_attribute

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
