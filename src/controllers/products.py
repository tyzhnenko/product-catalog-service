from typing import Annotated

from fastapi import Depends, HTTPException, Response, Security, status
from fastapi.routing import APIRouter

from src.core.auth import ro_access, rw_access
from src.domain.products import ProductsService
from src.domain.types.products import NewProduct, Product, ProductID, UpdateProduct
from src.domain.types.stores import StoreID

router = APIRouter()


@router.get(
    "/{store_id}",
    name="List Products",
    description="Retrieve a list of all products for a specific store.",
    operation_id="list_products",
    dependencies=[Security(ro_access)],
)
async def list_products(
    store_id: StoreID,
    service: Annotated[ProductsService, Depends(ProductsService)],
) -> list[Product]:
    """List all products for a specific store."""
    products = await service.list_products(store_id)
    if products is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Store not found",
        )
    return products


@router.post(
    "/{store_id}",
    name="Create Product",
    description="Create a new product for a specific store.",
    operation_id="create_product",
    dependencies=[Security(rw_access)],
)
async def create_product(
    store_id: StoreID,
    new_product: NewProduct,
    service: Annotated[ProductsService, Depends(ProductsService)],
) -> Product:
    """Create a new product for a specific store."""
    product = await service.create_product(store_id, new_product)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Store not found",
        )
    return product


@router.get(
    "/{store_id}/{product_id}",
    name="Get Product",
    description="Retrieve a specific product by its unique identifier.",
    operation_id="get_product",
    dependencies=[Security(ro_access)],
)
async def get_product(
    store_id: StoreID,
    product_id: ProductID,
    service: Annotated[ProductsService, Depends(ProductsService)],
) -> Product:
    """Get a specific product by ID."""
    product = await service.get_product(store_id, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    return product


@router.patch(
    "/{store_id}/{product_id}",
    name="Update Product",
    description="Update a specific product's information.",
    operation_id="update_product",
    dependencies=[Security(rw_access)],
)
async def update_product(
    store_id: StoreID,
    product_id: ProductID,
    update_data: UpdateProduct,
    service: Annotated[ProductsService, Depends(ProductsService)],
) -> Product:
    """Update a product's information."""
    updated_product = await service.update_product(store_id, product_id, update_data)
    if not updated_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    return updated_product


@router.delete(
    "/{store_id}/{product_id}",
    name="Delete Product",
    description="Delete a specific product (soft delete).",
    operation_id="delete_product",
    dependencies=[Security(rw_access)],
)
async def delete_product(
    store_id: StoreID,
    product_id: ProductID,
    service: Annotated[ProductsService, Depends(ProductsService)],
) -> Response:
    """Delete a product (soft delete)."""
    success = await service.delete_product(store_id, product_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
