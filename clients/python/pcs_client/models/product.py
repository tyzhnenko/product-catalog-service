from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.product_status_enum import ProductStatusEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.attributes_map import AttributesMap
    from ..models.product_seo import ProductSEO


T = TypeVar("T", bound="Product")


@_attrs_define
class Product:
    """Product information

    Attributes:
        id (str):  Example: 5eb7cf5a86d9755df3a6c593.
        name (str): Name of the product
        updated_at (datetime.datetime):
        created_at (datetime.datetime):
        description (None | str | Unset):
        brand (None | str | Unset):
        tags (list[str] | Unset): Tags associated with the product
        seo (None | ProductSEO | Unset):
        status (ProductStatusEnum | Unset):
        categories (list[str] | Unset): List of category identifiers for the product
        attributes (AttributesMap | Unset): Map of attribute name to attribute
    """

    id: str
    name: str
    updated_at: datetime.datetime
    created_at: datetime.datetime
    description: None | str | Unset = UNSET
    brand: None | str | Unset = UNSET
    tags: list[str] | Unset = UNSET
    seo: None | ProductSEO | Unset = UNSET
    status: ProductStatusEnum | Unset = UNSET
    categories: list[str] | Unset = UNSET
    attributes: AttributesMap | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.product_seo import ProductSEO

        id = self.id

        name = self.name

        updated_at = self.updated_at.isoformat()

        created_at = self.created_at.isoformat()

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        brand: None | str | Unset
        if isinstance(self.brand, Unset):
            brand = UNSET
        else:
            brand = self.brand

        tags: list[str] | Unset = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        seo: dict[str, Any] | None | Unset
        if isinstance(self.seo, Unset):
            seo = UNSET
        elif isinstance(self.seo, ProductSEO):
            seo = self.seo.to_dict()
        else:
            seo = self.seo

        status: str | Unset = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        categories: list[str] | Unset = UNSET
        if not isinstance(self.categories, Unset):
            categories = self.categories

        attributes: dict[str, Any] | Unset = UNSET
        if not isinstance(self.attributes, Unset):
            attributes = self.attributes.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "updated_at": updated_at,
                "created_at": created_at,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if brand is not UNSET:
            field_dict["brand"] = brand
        if tags is not UNSET:
            field_dict["tags"] = tags
        if seo is not UNSET:
            field_dict["seo"] = seo
        if status is not UNSET:
            field_dict["status"] = status
        if categories is not UNSET:
            field_dict["categories"] = categories
        if attributes is not UNSET:
            field_dict["attributes"] = attributes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.attributes_map import AttributesMap
        from ..models.product_seo import ProductSEO

        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_brand(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        brand = _parse_brand(d.pop("brand", UNSET))

        tags = cast(list[str], d.pop("tags", UNSET))

        def _parse_seo(data: object) -> None | ProductSEO | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                seo_type_0 = ProductSEO.from_dict(data)

                return seo_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | ProductSEO | Unset, data)

        seo = _parse_seo(d.pop("seo", UNSET))

        _status = d.pop("status", UNSET)
        status: ProductStatusEnum | Unset
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = ProductStatusEnum(_status)

        categories = cast(list[str], d.pop("categories", UNSET))

        _attributes = d.pop("attributes", UNSET)
        attributes: AttributesMap | Unset
        if isinstance(_attributes, Unset):
            attributes = UNSET
        else:
            attributes = AttributesMap.from_dict(_attributes)

        product = cls(
            id=id,
            name=name,
            updated_at=updated_at,
            created_at=created_at,
            description=description,
            brand=brand,
            tags=tags,
            seo=seo,
            status=status,
            categories=categories,
            attributes=attributes,
        )

        product.additional_properties = d
        return product

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
