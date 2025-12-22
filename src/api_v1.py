from fastapi import APIRouter
from src.controllers.stores import router as stores_router

api_router = APIRouter()

api_router.include_router(stores_router, prefix="/stores", tags=["stores"])
