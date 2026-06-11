from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.product_status_enum import ProductStatusEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.attributes_map import AttributesMap
    from ..models.product_seo import ProductSEO


T = TypeVar("T", bound="UpdateProduct")


@_attrs_define
class UpdateProduct:
    """Data required to update a product

    Attributes:
        name (None | str | Unset):
        description (None | str | Unset):
        brand (None | str | Unset):
        tags (list[str] | None | Unset):
        seo (None | ProductSEO | Unset):
        status (None | ProductStatusEnum | Unset):
        categories (list[str] | None | Unset):
        attributes (AttributesMap | None | Unset):
    """

    name: None | str | Unset = UNSET
    description: None | str | Unset = UNSET
    brand: None | str | Unset = UNSET
    tags: list[str] | None | Unset = UNSET
    seo: None | ProductSEO | Unset = UNSET
    status: None | ProductStatusEnum | Unset = UNSET
    categories: list[str] | None | Unset = UNSET
    attributes: AttributesMap | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.attributes_map import AttributesMap
        from ..models.product_seo import ProductSEO

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

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

        tags: list[str] | None | Unset
        if isinstance(self.tags, Unset):
            tags = UNSET
        elif isinstance(self.tags, list):
            tags = self.tags

        else:
            tags = self.tags

        seo: dict[str, Any] | None | Unset
        if isinstance(self.seo, Unset):
            seo = UNSET
        elif isinstance(self.seo, ProductSEO):
            seo = self.seo.to_dict()
        else:
            seo = self.seo

        status: None | str | Unset
        if isinstance(self.status, Unset):
            status = UNSET
        elif isinstance(self.status, ProductStatusEnum):
            status = self.status.value
        else:
            status = self.status

        categories: list[str] | None | Unset
        if isinstance(self.categories, Unset):
            categories = UNSET
        elif isinstance(self.categories, list):
            categories = self.categories

        else:
            categories = self.categories

        attributes: dict[str, Any] | None | Unset
        if isinstance(self.attributes, Unset):
            attributes = UNSET
        elif isinstance(self.attributes, AttributesMap):
            attributes = self.attributes.to_dict()
        else:
            attributes = self.attributes

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
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

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

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

        def _parse_tags(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                tags_type_0 = cast(list[str], data)

                return tags_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        tags = _parse_tags(d.pop("tags", UNSET))

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

        def _parse_status(data: object) -> None | ProductStatusEnum | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                status_type_0 = ProductStatusEnum(data)

                return status_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | ProductStatusEnum | Unset, data)

        status = _parse_status(d.pop("status", UNSET))

        def _parse_categories(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                categories_type_0 = cast(list[str], data)

                return categories_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        categories = _parse_categories(d.pop("categories", UNSET))

        def _parse_attributes(data: object) -> AttributesMap | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                attributes_type_0 = AttributesMap.from_dict(data)

                return attributes_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AttributesMap | None | Unset, data)

        attributes = _parse_attributes(d.pop("attributes", UNSET))

        update_product = cls(
            name=name,
            description=description,
            brand=brand,
            tags=tags,
            seo=seo,
            status=status,
            categories=categories,
            attributes=attributes,
        )

        update_product.additional_properties = d
        return update_product

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
