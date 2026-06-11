from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.attributes_map import AttributesMap
    from ..models.image import Image
    from ..models.location_price_map import LocationPriceMap
    from ..models.price_map import PriceMap
    from ..models.region_price_map import RegionPriceMap


T = TypeVar("T", bound="UpdateBundle")


@_attrs_define
class UpdateBundle:
    """
    Attributes:
        name (None | str | Unset):
        description (None | str | Unset):
        components (list[str] | None | Unset):
        attributes (AttributesMap | None | Unset):
        categories (list[str] | None | Unset):
        price (None | PriceMap | Unset):
        location_price (LocationPriceMap | None | Unset):
        region_price (None | RegionPriceMap | Unset):
        images (list[Image] | None | Unset):
    """

    name: None | str | Unset = UNSET
    description: None | str | Unset = UNSET
    components: list[str] | None | Unset = UNSET
    attributes: AttributesMap | None | Unset = UNSET
    categories: list[str] | None | Unset = UNSET
    price: None | PriceMap | Unset = UNSET
    location_price: LocationPriceMap | None | Unset = UNSET
    region_price: None | RegionPriceMap | Unset = UNSET
    images: list[Image] | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.attributes_map import AttributesMap
        from ..models.location_price_map import LocationPriceMap
        from ..models.price_map import PriceMap
        from ..models.region_price_map import RegionPriceMap

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

        components: list[str] | None | Unset
        if isinstance(self.components, Unset):
            components = UNSET
        elif isinstance(self.components, list):
            components = self.components

        else:
            components = self.components

        attributes: dict[str, Any] | None | Unset
        if isinstance(self.attributes, Unset):
            attributes = UNSET
        elif isinstance(self.attributes, AttributesMap):
            attributes = self.attributes.to_dict()
        else:
            attributes = self.attributes

        categories: list[str] | None | Unset
        if isinstance(self.categories, Unset):
            categories = UNSET
        elif isinstance(self.categories, list):
            categories = self.categories

        else:
            categories = self.categories

        price: dict[str, Any] | None | Unset
        if isinstance(self.price, Unset):
            price = UNSET
        elif isinstance(self.price, PriceMap):
            price = self.price.to_dict()
        else:
            price = self.price

        location_price: dict[str, Any] | None | Unset
        if isinstance(self.location_price, Unset):
            location_price = UNSET
        elif isinstance(self.location_price, LocationPriceMap):
            location_price = self.location_price.to_dict()
        else:
            location_price = self.location_price

        region_price: dict[str, Any] | None | Unset
        if isinstance(self.region_price, Unset):
            region_price = UNSET
        elif isinstance(self.region_price, RegionPriceMap):
            region_price = self.region_price.to_dict()
        else:
            region_price = self.region_price

        images: list[dict[str, Any]] | None | Unset
        if isinstance(self.images, Unset):
            images = UNSET
        elif isinstance(self.images, list):
            images = []
            for componentsschemas_bundle_images_item_data in self.images:
                componentsschemas_bundle_images_item = componentsschemas_bundle_images_item_data.to_dict()
                images.append(componentsschemas_bundle_images_item)

        else:
            images = self.images

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if components is not UNSET:
            field_dict["components"] = components
        if attributes is not UNSET:
            field_dict["attributes"] = attributes
        if categories is not UNSET:
            field_dict["categories"] = categories
        if price is not UNSET:
            field_dict["price"] = price
        if location_price is not UNSET:
            field_dict["location_price"] = location_price
        if region_price is not UNSET:
            field_dict["region_price"] = region_price
        if images is not UNSET:
            field_dict["images"] = images

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.attributes_map import AttributesMap
        from ..models.image import Image
        from ..models.location_price_map import LocationPriceMap
        from ..models.price_map import PriceMap
        from ..models.region_price_map import RegionPriceMap

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

        def _parse_components(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                components_type_0 = cast(list[str], data)

                return components_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        components = _parse_components(d.pop("components", UNSET))

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

        def _parse_price(data: object) -> None | PriceMap | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                price_type_0 = PriceMap.from_dict(data)

                return price_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | PriceMap | Unset, data)

        price = _parse_price(d.pop("price", UNSET))

        def _parse_location_price(data: object) -> LocationPriceMap | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                location_price_type_0 = LocationPriceMap.from_dict(data)

                return location_price_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(LocationPriceMap | None | Unset, data)

        location_price = _parse_location_price(d.pop("location_price", UNSET))

        def _parse_region_price(data: object) -> None | RegionPriceMap | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                region_price_type_0 = RegionPriceMap.from_dict(data)

                return region_price_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | RegionPriceMap | Unset, data)

        region_price = _parse_region_price(d.pop("region_price", UNSET))

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
                for componentsschemas_bundle_images_item_data in _images_type_0:
                    componentsschemas_bundle_images_item = Image.from_dict(componentsschemas_bundle_images_item_data)

                    images_type_0.append(componentsschemas_bundle_images_item)

                return images_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[Image] | None | Unset, data)

        images = _parse_images(d.pop("images", UNSET))

        update_bundle = cls(
            name=name,
            description=description,
            components=components,
            attributes=attributes,
            categories=categories,
            price=price,
            location_price=location_price,
            region_price=region_price,
            images=images,
        )

        update_bundle.additional_properties = d
        return update_bundle

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
