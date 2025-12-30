from typing import Annotated

from fastapi import Depends, HTTPException, Response, status
from fastapi.routing import APIRouter

from src.domain.products import ProductsService
from src.domain.types.products import NewProduct, Product, ProductUUID, UpdateProduct
from src.domain.types.stores import StoreUUID

router = APIRouter()


@router.get("/{store_id}")
async def list_products(
    store_id: StoreUUID,
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


@router.post("/{store_id}")
async def create_product(
    store_id: StoreUUID,
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


@router.get("/{store_id}/{product_id}")
async def get_product(
    store_id: StoreUUID,
    product_id: ProductUUID,
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


@router.patch("/{store_id}/{product_id}")
async def update_product(
    store_id: StoreUUID,
    product_id: ProductUUID,
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


@router.delete("/{store_id}/{product_id}")
async def delete_product(
    store_id: StoreUUID,
    product_id: ProductUUID,
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
