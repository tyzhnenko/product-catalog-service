from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware

from src.settings import Settings


def configure_gzip(app: FastAPI, settings: Settings) -> None:
    app.add_middleware(
        GZipMiddleware,
        minimum_size=1000,
    )
