from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ListOfUUIDsAttribute")


@_attrs_define
class ListOfUUIDsAttribute:
    """
    Attributes:
        name (str): Name of the attribute
        values (list[UUID]): List of UUID values
        type_ (Literal['list_of_uuids'] | Unset):  Default: 'list_of_uuids'.
    """

    name: str
    values: list[UUID]
    type_: Literal["list_of_uuids"] | Unset = "list_of_uuids"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        values = []
        for values_item_data in self.values:
            values_item = str(values_item_data)
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
            values_item = UUID(values_item_data)

            values.append(values_item)

        type_ = cast(Literal["list_of_uuids"] | Unset, d.pop("type", UNSET))
        if type_ != "list_of_uuids" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'list_of_uuids', got '{type_}'")

        list_of_uui_ds_attribute = cls(
            name=name,
            values=values,
            type_=type_,
        )

        list_of_uui_ds_attribute.additional_properties = d
        return list_of_uui_ds_attribute

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
