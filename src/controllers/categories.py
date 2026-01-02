from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.routing import APIRouter

from src.domain.categories import CategoriesService
from src.domain.types.categories import Category, CategoryUUID, NewCategory, UpdateCategory
from src.domain.types.stores import StoreUUID

router = APIRouter()


@router.get("/{store_id}")
async def list_categories(
    store_id: StoreUUID,
    service: Annotated[CategoriesService, Depends(CategoriesService)],
) -> list[Category]:
    categories = await service.list_categories(store_id)
    if categories is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Store not found",
        )
    return categories


@router.post("/{store_id}")
async def create_category(
    store_id: StoreUUID,
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


@router.get("/{store_id}/{category_id}")
async def get_category(
    store_id: StoreUUID,
    category_id: CategoryUUID,
    service: Annotated[CategoriesService, Depends(CategoriesService)],
) -> Category:
    category = await service.get_category(store_id, category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
    return category


@router.put("/{store_id}/{category_id}")
async def update_category(
    store_id: StoreUUID,
    category_id: CategoryUUID,
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


@router.delete("/{store_id}/{category_id}")
async def delete_category(
    store_id: StoreUUID,
    category_id: CategoryUUID,
    service: Annotated[CategoriesService, Depends(CategoriesService)],
):
    success = await service.delete_category(store_id, category_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
    raise HTTPException(status_code=204)
