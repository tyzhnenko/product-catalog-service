from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.map_of_object_ids_attribute_values import MapOfObjectIdsAttributeValues


T = TypeVar("T", bound="MapOfObjectIdsAttribute")


@_attrs_define
class MapOfObjectIdsAttribute:
    """
    Attributes:
        name (str): Name of the attribute
        values (MapOfObjectIdsAttributeValues): Map of ObjectId values
        type_ (Literal['map_of_object_ids'] | Unset):  Default: 'map_of_object_ids'.
    """

    name: str
    values: MapOfObjectIdsAttributeValues
    type_: Literal["map_of_object_ids"] | Unset = "map_of_object_ids"
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
        from ..models.map_of_object_ids_attribute_values import MapOfObjectIdsAttributeValues

        d = dict(src_dict)
        name = d.pop("name")

        values = MapOfObjectIdsAttributeValues.from_dict(d.pop("values"))

        type_ = cast(Literal["map_of_object_ids"] | Unset, d.pop("type", UNSET))
        if type_ != "map_of_object_ids" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'map_of_object_ids', got '{type_}'")

        map_of_object_ids_attribute = cls(
            name=name,
            values=values,
            type_=type_,
        )

        map_of_object_ids_attribute.additional_properties = d
        return map_of_object_ids_attribute

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
