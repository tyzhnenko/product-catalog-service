from enum import StrEnum


class CategoryStatusEnum(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"

    def __str__(self) -> str:
        return str(self.value)
