from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.decimal_price import DecimalPrice
    from ..models.decimal_quantity_price import DecimalQuantityPrice
    from ..models.decimal_range_price import DecimalRangePrice


T = TypeVar("T", bound="PriceMap")


@_attrs_define
class PriceMap:
    """Mapping of price identifiers to their corresponding Price objects"""

    additional_properties: dict[str, DecimalPrice | DecimalQuantityPrice | DecimalRangePrice] = _attrs_field(
        init=False, factory=dict
    )

    def to_dict(self) -> dict[str, Any]:
        from ..models.decimal_price import DecimalPrice
        from ..models.decimal_range_price import DecimalRangePrice

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            if isinstance(prop, DecimalPrice):
                field_dict[prop_name] = prop.to_dict()
            elif isinstance(prop, DecimalRangePrice):
                field_dict[prop_name] = prop.to_dict()
            else:
                field_dict[prop_name] = prop.to_dict()

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.decimal_price import DecimalPrice
        from ..models.decimal_quantity_price import DecimalQuantityPrice
        from ..models.decimal_range_price import DecimalRangePrice

        d = dict(src_dict)
        price_map = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():

            def _parse_additional_property(data: object) -> DecimalPrice | DecimalQuantityPrice | DecimalRangePrice:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_price_type_0 = DecimalPrice.from_dict(data)

                    return componentsschemas_price_type_0
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_price_type_1 = DecimalRangePrice.from_dict(data)

                    return componentsschemas_price_type_1
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_price_type_2 = DecimalQuantityPrice.from_dict(data)

                return componentsschemas_price_type_2

            additional_property = _parse_additional_property(prop_dict)

            additional_properties[prop_name] = additional_property

        price_map.additional_properties = additional_properties
        return price_map

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> DecimalPrice | DecimalQuantityPrice | DecimalRangePrice:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: DecimalPrice | DecimalQuantityPrice | DecimalRangePrice) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
