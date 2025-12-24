from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.routing import APIRouter

from src.domain.stores import StoresService
from src.domain.types.stores import NewStore, Store, StoreUUID, UpdateStore

router = APIRouter()


@router.get("/")
async def list_stores(
    service: Annotated[StoresService, Depends(StoresService)],
) -> list[Store]:
    return await service.list_stores()


@router.post("/")
async def create_store(
    new_store: NewStore,
    service: Annotated[StoresService, Depends(StoresService)],
) -> Store:
    store = await service.create_store(new_store)
    return store


@router.get("/{store_id}")
async def get_store(
    store_id: StoreUUID,
    service: Annotated[StoresService, Depends(StoresService)],
) -> Store:
    store = await service.get_store(store_id)
    if not store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Store not found",
        )
    return store


@router.put("/{store_id}")
async def update_store(
    store_id: StoreUUID,
    update_data: UpdateStore,
    service: Annotated[StoresService, Depends(StoresService)],
):
    updated_store = await service.update_store(store_id, update_data)
    if not updated_store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Store not found",
        )

    return updated_store


@router.delete("/{store_id}")
async def delete_store(
    store_id: StoreUUID,
    service: Annotated[StoresService, Depends(StoresService)],
):
    success = await service.delete_store(store_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Store not found",
        )
    raise HTTPException(status_code=204)
