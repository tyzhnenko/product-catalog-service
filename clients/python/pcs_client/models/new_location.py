from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.attributes_map import AttributesMap


T = TypeVar("T", bound="NewLocation")


@_attrs_define
class NewLocation:
    """
    Attributes:
        name (str): Name of the location
        attributes (AttributesMap | Unset): Map of attribute name to attribute
    """

    name: str
    attributes: AttributesMap | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        attributes: dict[str, Any] | Unset = UNSET
        if not isinstance(self.attributes, Unset):
            attributes = self.attributes.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if attributes is not UNSET:
            field_dict["attributes"] = attributes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.attributes_map import AttributesMap

        d = dict(src_dict)
        name = d.pop("name")

        _attributes = d.pop("attributes", UNSET)
        attributes: AttributesMap | Unset
        if isinstance(_attributes, Unset):
            attributes = UNSET
        else:
            attributes = AttributesMap.from_dict(_attributes)

        new_location = cls(
            name=name,
            attributes=attributes,
        )

        new_location.additional_properties = d
        return new_location

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
