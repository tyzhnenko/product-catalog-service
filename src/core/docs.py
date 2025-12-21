from fastapi import FastAPI

from src.settings import Settings


def configure_docs(app: FastAPI, settings: Settings):
    app.title = settings.info.title
    app.version = settings.info.version
    app.description = settings.info.description
