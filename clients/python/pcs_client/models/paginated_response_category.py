from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.category import Category


T = TypeVar("T", bound="PaginatedResponseCategory")


@_attrs_define
class PaginatedResponseCategory:
    """
    Attributes:
        items (list[Category]):
        start_cursor (None | str):
        end_cursor (None | str):
        has_next (bool):
        has_prev (bool):
        total (int):
    """

    items: list[Category]
    start_cursor: None | str
    end_cursor: None | str
    has_next: bool
    has_prev: bool
    total: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)

        start_cursor: None | str
        start_cursor = self.start_cursor

        end_cursor: None | str
        end_cursor = self.end_cursor

        has_next = self.has_next

        has_prev = self.has_prev

        total = self.total

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "items": items,
                "start_cursor": start_cursor,
                "end_cursor": end_cursor,
                "has_next": has_next,
                "has_prev": has_prev,
                "total": total,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.category import Category

        d = dict(src_dict)
        items = []
        _items = d.pop("items")
        for items_item_data in _items:
            items_item = Category.from_dict(items_item_data)

            items.append(items_item)

        def _parse_start_cursor(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        start_cursor = _parse_start_cursor(d.pop("start_cursor"))

        def _parse_end_cursor(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        end_cursor = _parse_end_cursor(d.pop("end_cursor"))

        has_next = d.pop("has_next")

        has_prev = d.pop("has_prev")

        total = d.pop("total")

        paginated_response_category = cls(
            items=items,
            start_cursor=start_cursor,
            end_cursor=end_cursor,
            has_next=has_next,
            has_prev=has_prev,
            total=total,
        )

        paginated_response_category.additional_properties = d
        return paginated_response_category

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
