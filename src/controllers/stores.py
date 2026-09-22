from typing import Annotated

from fastapi import Depends, HTTPException, Security, status
from fastapi.routing import APIRouter

from src.core.auth import ro_access, rw_access
from src.core.fields import FieldsParams, sparse_response
from src.core.pagination import PaginationParams
from src.core.types import PaginatedResponse
from src.domain.stores import StoresService
from src.domain.types.stores import NewStore, PartialStore, Store, StoreRef, UpdateStore

router = APIRouter()


@router.get(
    "/",
    name="List Stores",
    description="Retrieve a list of all stores in the system.",
    operation_id="list_stores",
    dependencies=[Security(ro_access)],
    response_model=sparse_response(Store, PartialStore, paginated=True),
    response_model_exclude_unset=True,
)
async def list_stores(
    service: Annotated[StoresService, Depends(StoresService)],
    pagination: Annotated[PaginationParams, Depends()],
    fields: Annotated[FieldsParams, Depends()],
) -> PaginatedResponse[Store] | PaginatedResponse[PartialStore]:
    return await service.list_stores(pagination, fields=fields.resolve(Store))


@router.post(
    "/",
    name="Create Store",
    description="Create a new store in the system.",
    operation_id="create_store",
    dependencies=[Security(rw_access)],
)
async def create_store(
    new_store: NewStore,
    service: Annotated[StoresService, Depends(StoresService)],
) -> Store:
    store = await service.create_store(new_store)
    return store


@router.get(
    "/{store_id}",
    name="Get Store",
    description="Retrieve a store by its unique identifier.",
    operation_id="get_store",
    dependencies=[Security(ro_access)],
    response_model=sparse_response(Store, PartialStore),
    response_model_exclude_unset=True,
)
async def get_store(
    store_id: StoreRef,
    service: Annotated[StoresService, Depends(StoresService)],
    fields: Annotated[FieldsParams, Depends()],
) -> Store | PartialStore:
    store = await service.get_store(store_id, fields=fields.resolve(Store))
    if not store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Store not found",
        )
    return store


@router.put(
    "/{store_id}",
    name="Update Store",
    description="Update an existing store's information.",
    operation_id="update_store",
    dependencies=[Security(rw_access)],
)
async def update_store(
    store_id: StoreRef,
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


@router.delete(
    "/{store_id}",
    name="Delete Store",
    description="Delete a store by its unique identifier.",
    operation_id="delete_store",
    dependencies=[Security(rw_access)],
)
async def delete_store(
    store_id: StoreRef,
    service: Annotated[StoresService, Depends(StoresService)],
):
    success = await service.delete_store(store_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Store not found",
        )
    raise HTTPException(status_code=204)
