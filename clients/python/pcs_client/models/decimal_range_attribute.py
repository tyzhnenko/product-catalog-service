from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="DecimalRangeAttribute")


@_attrs_define
class DecimalRangeAttribute:
    """
    Attributes:
        name (str): Name of the attribute
        min_value (float | str): Decimal value represented as a float in string format
        max_value (float | str): Decimal value represented as a float in string format
        type_ (Literal['decimal_range'] | Unset):  Default: 'decimal_range'.
    """

    name: str
    min_value: float | str
    max_value: float | str
    type_: Literal["decimal_range"] | Unset = "decimal_range"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        min_value: float | str
        min_value = self.min_value

        max_value: float | str
        max_value = self.max_value

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "min_value": min_value,
                "max_value": max_value,
            }
        )
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        def _parse_min_value(data: object) -> float | str:
            return cast(float | str, data)

        min_value = _parse_min_value(d.pop("min_value"))

        def _parse_max_value(data: object) -> float | str:
            return cast(float | str, data)

        max_value = _parse_max_value(d.pop("max_value"))

        type_ = cast(Literal["decimal_range"] | Unset, d.pop("type", UNSET))
        if type_ != "decimal_range" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'decimal_range', got '{type_}'")

        decimal_range_attribute = cls(
            name=name,
            min_value=min_value,
            max_value=max_value,
            type_=type_,
        )

        decimal_range_attribute.additional_properties = d
        return decimal_range_attribute

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
