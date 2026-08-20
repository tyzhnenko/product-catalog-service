from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.category_status_enum import CategoryStatusEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.attributes_map import AttributesMap
    from ..models.image import Image
    from ..models.seo import SEO


T = TypeVar("T", bound="NewCategory")


@_attrs_define
class NewCategory:
    """Data required to create a new category

    Attributes:
        name (str): Name of the category
        path (str): Path of the category. Example: '/electronics/laptops'. Root categories have path as '/electronics'.
        description (None | str | Unset):
        status (CategoryStatusEnum | Unset):
        seo (None | SEO | Unset):
        attributes (AttributesMap | None | Unset):
        images (list[Image] | None | Unset):
    """

    name: str
    path: str
    description: None | str | Unset = UNSET
    status: CategoryStatusEnum | Unset = UNSET
    seo: None | SEO | Unset = UNSET
    attributes: AttributesMap | None | Unset = UNSET
    images: list[Image] | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.attributes_map import AttributesMap
        from ..models.seo import SEO

        name = self.name

        path = self.path

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        status: str | Unset = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        seo: dict[str, Any] | None | Unset
        if isinstance(self.seo, Unset):
            seo = UNSET
        elif isinstance(self.seo, SEO):
            seo = self.seo.to_dict()
        else:
            seo = self.seo

        attributes: dict[str, Any] | None | Unset
        if isinstance(self.attributes, Unset):
            attributes = UNSET
        elif isinstance(self.attributes, AttributesMap):
            attributes = self.attributes.to_dict()
        else:
            attributes = self.attributes

        images: list[dict[str, Any]] | None | Unset
        if isinstance(self.images, Unset):
            images = UNSET
        elif isinstance(self.images, list):
            images = []
            for componentsschemas_category_images_item_data in self.images:
                componentsschemas_category_images_item = componentsschemas_category_images_item_data.to_dict()
                images.append(componentsschemas_category_images_item)

        else:
            images = self.images

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "path": path,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if status is not UNSET:
            field_dict["status"] = status
        if seo is not UNSET:
            field_dict["seo"] = seo
        if attributes is not UNSET:
            field_dict["attributes"] = attributes
        if images is not UNSET:
            field_dict["images"] = images

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.attributes_map import AttributesMap
        from ..models.image import Image
        from ..models.seo import SEO

        d = dict(src_dict)
        name = d.pop("name")

        path = d.pop("path")

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        _status = d.pop("status", UNSET)
        status: CategoryStatusEnum | Unset
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = CategoryStatusEnum(_status)

        def _parse_seo(data: object) -> None | SEO | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                seo_type_0 = SEO.from_dict(data)

                return seo_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | SEO | Unset, data)

        seo = _parse_seo(d.pop("seo", UNSET))

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

        def _parse_images(data: object) -> list[Image] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
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
            return cast(list[Image] | None | Unset, data)

        images = _parse_images(d.pop("images", UNSET))

        new_category = cls(
            name=name,
            path=path,
            description=description,
            status=status,
            seo=seo,
            attributes=attributes,
            images=images,
        )

        new_category.additional_properties = d
        return new_category

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
