from typing import Annotated

from fastapi import Depends, HTTPException, Query, Security, status
from fastapi.routing import APIRouter

from src.core.auth import ro_access, rw_access
from src.core.fields import FieldsParams, sparse_response
from src.core.pagination import PaginationParams
from src.core.types import PaginatedResponse
from src.core.utils import build_attribute_filter
from src.domain.categories import CategoriesService
from src.domain.types.categories import Category, CategoryRef, NewCategory, PartialCategory, UpdateCategory
from src.domain.types.stores import StoreRef

router = APIRouter()


def category_filters(
    attrs: Annotated[
        list[str],
        Query(
            default_factory=list,
            description=(
                "Attribute filters in 'key:value' format. Repeat for multiple values. "
                "Same key = OR, different keys = AND."
            ),
        ),
    ],
) -> dict | None:
    return build_attribute_filter(attrs) or None


CategoryFilters = Annotated[dict | None, Depends(category_filters)]


@router.get(
    "/{store_id}",
    name="List Categories",
    description="Retrieve a list of all categories for a specific store.",
    operation_id="list_categories",
    dependencies=[Security(ro_access)],
    response_model=sparse_response(Category, PartialCategory, paginated=True),
    response_model_exclude_unset=True,
)
async def list_categories(
    store_id: StoreRef,
    service: Annotated[CategoriesService, Depends(CategoriesService)],
    pagination: Annotated[PaginationParams, Depends()],
    filters: CategoryFilters,
    fields: Annotated[FieldsParams, Depends()],
) -> PaginatedResponse[Category] | PaginatedResponse[PartialCategory]:
    result = await service.list_categories(
        store_id,
        pagination,
        filters=filters,
        fields=fields.resolve(Category),
    )
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Store not found",
        )
    return result


@router.post(
    "/{store_id}",
    name="Create Category",
    description="Create a new category for a specific store.",
    operation_id="create_category",
    dependencies=[Security(rw_access)],
)
async def create_category(
    store_id: StoreRef,
    new_category: NewCategory,
    service: Annotated[CategoriesService, Depends(CategoriesService)],
) -> Category:
    category = await service.create_category(store_id, new_category)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Store not found",
        )
    return category


@router.get(
    "/{store_id}/{category_id}",
    name="Get Category",
    description="Retrieve details of a specific category by its ID for a specific store.",
    operation_id="get_category",
    dependencies=[Security(ro_access)],
    response_model=sparse_response(Category, PartialCategory),
    response_model_exclude_unset=True,
)
async def get_category(
    store_id: StoreRef,
    category_id: CategoryRef,
    service: Annotated[CategoriesService, Depends(CategoriesService)],
    fields: Annotated[FieldsParams, Depends()],
) -> Category | PartialCategory:
    category = await service.get_category(store_id, category_id, fields=fields.resolve(Category))
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
    return category


@router.put(
    "/{store_id}/{category_id}",
    name="Update Category",
    description="Update details of a specific category by its ID for a specific store.",
    operation_id="update_category",
    dependencies=[Security(rw_access)],
)
async def update_category(
    store_id: StoreRef,
    category_id: CategoryRef,
    update_data: UpdateCategory,
    service: Annotated[CategoriesService, Depends(CategoriesService)],
):
    updated_category = await service.update_category(store_id, category_id, update_data)
    if not updated_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )

    return updated_category


@router.delete(
    "/{store_id}/{category_id}",
    name="Delete Category",
    description="Delete a specific category by its ID for a specific store.",
    operation_id="delete_category",
    dependencies=[Security(rw_access)],
)
async def delete_category(
    store_id: StoreRef,
    category_id: CategoryRef,
    service: Annotated[CategoriesService, Depends(CategoriesService)],
):
    success = await service.delete_category(store_id, category_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
    raise HTTPException(status_code=204)
