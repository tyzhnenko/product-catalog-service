from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.seo import SEO


T = TypeVar("T", bound="PartialStore")


@_attrs_define
class PartialStore:
    """Sparse `Store` returned when the `fields` query param narrows the response.

    Attributes:
        id (str):  Example: 5eb7cf5a86d9755df3a6c593.
        name (None | str | Unset):
        url (None | str | Unset):
        seo (None | SEO | Unset):
    """

    id: str
    name: None | str | Unset = UNSET
    url: None | str | Unset = UNSET
    seo: None | SEO | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.seo import SEO

        id = self.id

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        url: None | str | Unset
        if isinstance(self.url, Unset):
            url = UNSET
        else:
            url = self.url

        seo: dict[str, Any] | None | Unset
        if isinstance(self.seo, Unset):
            seo = UNSET
        elif isinstance(self.seo, SEO):
            seo = self.seo.to_dict()
        else:
            seo = self.seo

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if url is not UNSET:
            field_dict["url"] = url
        if seo is not UNSET:
            field_dict["seo"] = seo

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.seo import SEO

        d = dict(src_dict)
        id = d.pop("id")

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        url = _parse_url(d.pop("url", UNSET))

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

        partial_store = cls(
            id=id,
            name=name,
            url=url,
            seo=seo,
        )

        partial_store.additional_properties = d
        return partial_store

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
