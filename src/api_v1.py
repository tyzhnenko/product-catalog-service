from fastapi import APIRouter

from src.controllers.locations import router as locations_router
from src.controllers.products import router as products_router
from src.controllers.stores import router as stores_router
from src.controllers.variants import router as variants_router

api_router = APIRouter()

api_router.include_router(stores_router, prefix="/stores", tags=["stores"])
api_router.include_router(locations_router, prefix="/locations", tags=["locations"])
api_router.include_router(products_router, prefix="/products", tags=["products"])
api_router.include_router(variants_router, prefix="/variants", tags=["variants"])
