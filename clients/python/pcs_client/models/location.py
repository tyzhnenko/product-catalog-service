from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.attributes_map import AttributesMap


T = TypeVar("T", bound="Location")


@_attrs_define
class Location:
    """
    Attributes:
        id (str):  Example: 5eb7cf5a86d9755df3a6c593.
        name (str): Name of the location
        store_id (str):  Example: 5eb7cf5a86d9755df3a6c593.
        attributes (AttributesMap | Unset): Map of attribute name to attribute
    """

    id: str
    name: str
    store_id: str
    attributes: AttributesMap | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        store_id = self.store_id

        attributes: dict[str, Any] | Unset = UNSET
        if not isinstance(self.attributes, Unset):
            attributes = self.attributes.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "store_id": store_id,
            }
        )
        if attributes is not UNSET:
            field_dict["attributes"] = attributes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.attributes_map import AttributesMap

        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        store_id = d.pop("store_id")

        _attributes = d.pop("attributes", UNSET)
        attributes: AttributesMap | Unset
        if isinstance(_attributes, Unset):
            attributes = UNSET
        else:
            attributes = AttributesMap.from_dict(_attributes)

        location = cls(
            id=id,
            name=name,
            store_id=store_id,
            attributes=attributes,
        )

        location.additional_properties = d
        return location

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
