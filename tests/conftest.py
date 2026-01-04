import logging
import os

import pytest
from fastapi.testclient import TestClient
from pytest_mongo import factories

from src.settings import Settings

if os.environ.get("CI"):
    mongo_proc = factories.mongo_noproc()  # type: ignore
else:
    mongo_proc = factories.mongo_proc()  # type: ignore
mongodb = factories.mongodb("mongo_proc")


logging.getLogger("pymongo").setLevel(logging.INFO)


@pytest.fixture
async def api_client(mongodb, app_settings: Settings):
    from src.main import app

    headers = {"x-api-key": str(app_settings.auth.rw_x_api_key)}

    with TestClient(app, headers=headers) as client:
        yield client


@pytest.fixture
def app_settings() -> Settings:
    from src.settings import load_settings

    return load_settings()
