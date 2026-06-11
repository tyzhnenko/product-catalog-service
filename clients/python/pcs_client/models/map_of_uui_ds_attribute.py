from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.map_of_uui_ds_attribute_values import MapOfUUIDsAttributeValues


T = TypeVar("T", bound="MapOfUUIDsAttribute")


@_attrs_define
class MapOfUUIDsAttribute:
    """
    Attributes:
        name (str): Name of the attribute
        values (MapOfUUIDsAttributeValues): Map of UUID values
        type_ (Literal['map_of_uuids'] | Unset):  Default: 'map_of_uuids'.
    """

    name: str
    values: MapOfUUIDsAttributeValues
    type_: Literal["map_of_uuids"] | Unset = "map_of_uuids"
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
        from ..models.map_of_uui_ds_attribute_values import MapOfUUIDsAttributeValues

        d = dict(src_dict)
        name = d.pop("name")

        values = MapOfUUIDsAttributeValues.from_dict(d.pop("values"))

        type_ = cast(Literal["map_of_uuids"] | Unset, d.pop("type", UNSET))
        if type_ != "map_of_uuids" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'map_of_uuids', got '{type_}'")

        map_of_uui_ds_attribute = cls(
            name=name,
            values=values,
            type_=type_,
        )

        map_of_uui_ds_attribute.additional_properties = d
        return map_of_uui_ds_attribute

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
