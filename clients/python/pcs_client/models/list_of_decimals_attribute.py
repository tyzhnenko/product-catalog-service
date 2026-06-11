from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ListOfDecimalsAttribute")


@_attrs_define
class ListOfDecimalsAttribute:
    """
    Attributes:
        name (str): Name of the attribute
        values (list[float | str]): List of decimal values
        type_ (Literal['list_of_decimals'] | Unset):  Default: 'list_of_decimals'.
    """

    name: str
    values: list[float | str]
    type_: Literal["list_of_decimals"] | Unset = "list_of_decimals"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        values = []
        for values_item_data in self.values:
            values_item: float | str
            values_item = values_item_data
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

            def _parse_values_item(data: object) -> float | str:
                return cast(float | str, data)

            values_item = _parse_values_item(values_item_data)

            values.append(values_item)

        type_ = cast(Literal["list_of_decimals"] | Unset, d.pop("type", UNSET))
        if type_ != "list_of_decimals" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'list_of_decimals', got '{type_}'")

        list_of_decimals_attribute = cls(
            name=name,
            values=values,
            type_=type_,
        )

        list_of_decimals_attribute.additional_properties = d
        return list_of_decimals_attribute

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
