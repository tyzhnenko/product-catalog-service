from enum import StrEnum


class ProductStatusEnum(StrEnum):
    ACTIVE = "active"
    ARCHIVED = "archived"
    DRAFT = "draft"

    def __str__(self) -> str:
        return str(self.value)
