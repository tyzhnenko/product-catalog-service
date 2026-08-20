from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.category_status_enum import CategoryStatusEnum

if TYPE_CHECKING:
    from ..models.attributes_map import AttributesMap
    from ..models.image import Image
    from ..models.seo import SEO


T = TypeVar("T", bound="Category")


@_attrs_define
class Category:
    """Category model

    Attributes:
        id (str):  Example: 5eb7cf5a86d9755df3a6c593.
        name (str): Name of the category
        description (None | str):
        status (CategoryStatusEnum):
        path (str): Path of the category. Example: '/electronics/laptops'. Root categories have path as '/electronics'.
        seo (None | SEO):
        attributes (AttributesMap | None):
        images (list[Image] | None):
        updated_at (datetime.datetime):
        created_at (datetime.datetime):
    """

    id: str
    name: str
    description: None | str
    status: CategoryStatusEnum
    path: str
    seo: None | SEO
    attributes: AttributesMap | None
    images: list[Image] | None
    updated_at: datetime.datetime
    created_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.attributes_map import AttributesMap
        from ..models.seo import SEO

        id = self.id

        name = self.name

        description: None | str
        description = self.description

        status = self.status.value

        path = self.path

        seo: dict[str, Any] | None
        if isinstance(self.seo, SEO):
            seo = self.seo.to_dict()
        else:
            seo = self.seo

        attributes: dict[str, Any] | None
        if isinstance(self.attributes, AttributesMap):
            attributes = self.attributes.to_dict()
        else:
            attributes = self.attributes

        images: list[dict[str, Any]] | None
        if isinstance(self.images, list):
            images = []
            for componentsschemas_category_images_item_data in self.images:
                componentsschemas_category_images_item = componentsschemas_category_images_item_data.to_dict()
                images.append(componentsschemas_category_images_item)

        else:
            images = self.images

        updated_at = self.updated_at.isoformat()

        created_at = self.created_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "description": description,
                "status": status,
                "path": path,
                "seo": seo,
                "attributes": attributes,
                "images": images,
                "updated_at": updated_at,
                "created_at": created_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.attributes_map import AttributesMap
        from ..models.image import Image
        from ..models.seo import SEO

        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        def _parse_description(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        description = _parse_description(d.pop("description"))

        status = CategoryStatusEnum(d.pop("status"))

        path = d.pop("path")

        def _parse_seo(data: object) -> None | SEO:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                seo_type_0 = SEO.from_dict(data)

                return seo_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | SEO, data)

        seo = _parse_seo(d.pop("seo"))

        def _parse_attributes(data: object) -> AttributesMap | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                attributes_type_0 = AttributesMap.from_dict(data)

                return attributes_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AttributesMap | None, data)

        attributes = _parse_attributes(d.pop("attributes"))

        def _parse_images(data: object) -> list[Image] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                images_type_0 = []
                _images_type_0 = data
                for componentsschemas_category_images_item_data in _images_type_0:
                    componentsschemas_category_images_item = Image.from_dict(
                        componentsschemas_category_images_item_data
                    )

                    images_type_0.append(componentsschemas_category_images_item)

                return images_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[Image] | None, data)

        images = _parse_images(d.pop("images"))

        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        category = cls(
            id=id,
            name=name,
            description=description,
            status=status,
            path=path,
            seo=seo,
            attributes=attributes,
            images=images,
            updated_at=updated_at,
            created_at=created_at,
        )

        category.additional_properties = d
        return category

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
