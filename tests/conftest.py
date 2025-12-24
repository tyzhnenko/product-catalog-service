import logging
import os

import pytest
from fastapi.testclient import TestClient
from pytest_mongo import factories

if os.environ.get("CI"):
    mongo_proc = factories.mongo_noproc()  # type: ignore
else:
    mongo_proc = factories.mongo_proc()  # type: ignore
mongodb = factories.mongodb("mongo_proc")


logging.getLogger("pymongo").setLevel(logging.INFO)


@pytest.fixture
async def api_client(mongodb):
    from src.main import app

    with TestClient(app) as client:
        yield client
