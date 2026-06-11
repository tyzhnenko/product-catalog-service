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
    from ..models.variant_option import VariantOption


T = TypeVar("T", bound="ProductVariant")


@_attrs_define
class ProductVariant:
    """Product variant information

    Attributes:
        id (str):  Example: 5eb7cf5a86d9755df3a6c593.
        product_id (str):  Example: 5eb7cf5a86d9755df3a6c593.
        title (str): Title of the variant
        sku (None | str | Unset):
        upc (None | str | Unset):
        ean (None | str | Unset):
        jan (None | str | Unset):
        isbn (None | str | Unset):
        options (list[VariantOption] | Unset): Additional options for the variant as key-value pairs
        attributes (AttributesMap | None | Unset):
        price (None | PriceMap | Unset):
        location_price (LocationPriceMap | None | Unset):
        region_price (None | RegionPriceMap | Unset):
        images (list[Image] | None | Unset):
    """

    id: str
    product_id: str
    title: str
    sku: None | str | Unset = UNSET
    upc: None | str | Unset = UNSET
    ean: None | str | Unset = UNSET
    jan: None | str | Unset = UNSET
    isbn: None | str | Unset = UNSET
    options: list[VariantOption] | Unset = UNSET
    attributes: AttributesMap | None | Unset = UNSET
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

        id = self.id

        product_id = self.product_id

        title = self.title

        sku: None | str | Unset
        if isinstance(self.sku, Unset):
            sku = UNSET
        else:
            sku = self.sku

        upc: None | str | Unset
        if isinstance(self.upc, Unset):
            upc = UNSET
        else:
            upc = self.upc

        ean: None | str | Unset
        if isinstance(self.ean, Unset):
            ean = UNSET
        else:
            ean = self.ean

        jan: None | str | Unset
        if isinstance(self.jan, Unset):
            jan = UNSET
        else:
            jan = self.jan

        isbn: None | str | Unset
        if isinstance(self.isbn, Unset):
            isbn = UNSET
        else:
            isbn = self.isbn

        options: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.options, Unset):
            options = []
            for componentsschemas_variant_options_item_data in self.options:
                componentsschemas_variant_options_item = componentsschemas_variant_options_item_data.to_dict()
                options.append(componentsschemas_variant_options_item)

        attributes: dict[str, Any] | None | Unset
        if isinstance(self.attributes, Unset):
            attributes = UNSET
        elif isinstance(self.attributes, AttributesMap):
            attributes = self.attributes.to_dict()
        else:
            attributes = self.attributes

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
            for componentsschemas_variant_images_item_data in self.images:
                componentsschemas_variant_images_item = componentsschemas_variant_images_item_data.to_dict()
                images.append(componentsschemas_variant_images_item)

        else:
            images = self.images

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "product_id": product_id,
                "title": title,
            }
        )
        if sku is not UNSET:
            field_dict["sku"] = sku
        if upc is not UNSET:
            field_dict["upc"] = upc
        if ean is not UNSET:
            field_dict["ean"] = ean
        if jan is not UNSET:
            field_dict["jan"] = jan
        if isbn is not UNSET:
            field_dict["isbn"] = isbn
        if options is not UNSET:
            field_dict["options"] = options
        if attributes is not UNSET:
            field_dict["attributes"] = attributes
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
        from ..models.variant_option import VariantOption

        d = dict(src_dict)
        id = d.pop("id")

        product_id = d.pop("product_id")

        title = d.pop("title")

        def _parse_sku(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        sku = _parse_sku(d.pop("sku", UNSET))

        def _parse_upc(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        upc = _parse_upc(d.pop("upc", UNSET))

        def _parse_ean(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        ean = _parse_ean(d.pop("ean", UNSET))

        def _parse_jan(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        jan = _parse_jan(d.pop("jan", UNSET))

        def _parse_isbn(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        isbn = _parse_isbn(d.pop("isbn", UNSET))

        _options = d.pop("options", UNSET)
        options: list[VariantOption] | Unset = UNSET
        if _options is not UNSET:
            options = []
            for componentsschemas_variant_options_item_data in _options:
                componentsschemas_variant_options_item = VariantOption.from_dict(
                    componentsschemas_variant_options_item_data
                )

                options.append(componentsschemas_variant_options_item)

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
                for componentsschemas_variant_images_item_data in _images_type_0:
                    componentsschemas_variant_images_item = Image.from_dict(componentsschemas_variant_images_item_data)

                    images_type_0.append(componentsschemas_variant_images_item)

                return images_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[Image] | None | Unset, data)

        images = _parse_images(d.pop("images", UNSET))

        product_variant = cls(
            id=id,
            product_id=product_id,
            title=title,
            sku=sku,
            upc=upc,
            ean=ean,
            jan=jan,
            isbn=isbn,
            options=options,
            attributes=attributes,
            price=price,
            location_price=location_price,
            region_price=region_price,
            images=images,
        )

        product_variant.additional_properties = d
        return product_variant

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
