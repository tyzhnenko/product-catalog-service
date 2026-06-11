from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ListOfURLsAttribute")


@_attrs_define
class ListOfURLsAttribute:
    """
    Attributes:
        name (str): Name of the attribute
        values (list[str]): List of URL values
        type_ (Literal['list_of_urls'] | Unset):  Default: 'list_of_urls'.
    """

    name: str
    values: list[str]
    type_: Literal["list_of_urls"] | Unset = "list_of_urls"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        values = self.values

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

        values = cast(list[str], d.pop("values"))

        type_ = cast(Literal["list_of_urls"] | Unset, d.pop("type", UNSET))
        if type_ != "list_of_urls" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'list_of_urls', got '{type_}'")

        list_of_ur_ls_attribute = cls(
            name=name,
            values=values,
            type_=type_,
        )

        list_of_ur_ls_attribute.additional_properties = d
        return list_of_ur_ls_attribute

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
