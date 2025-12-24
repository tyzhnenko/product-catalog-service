from fastapi import APIRouter
from src.controllers.locations import router as locations_router
from src.controllers.stores import router as stores_router

api_router = APIRouter()

api_router.include_router(stores_router, prefix="/stores", tags=["stores"])
api_router.include_router(locations_router, prefix="/locations", tags=["locations"])
