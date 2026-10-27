# ruff: noqa: S101, S105, S106, D100, D101, D102, D103
import pytest
from pymongo.uri_parser import parse_uri

from src.db import build_connection_string
from src.settings import Database

SPECIAL_PASSWORD = "p@ss:w/rd%#+ "


@pytest.fixture(autouse=True)
def clean_db_env(monkeypatch):
    # Database is an unprefixed BaseSettings, so bare env vars such as USER leak into its fields
    for name in ("DRIVER", "HOST", "PORT", "DATABASE", "USER", "PASSWORD", "AUTH_SOURCE", "TLS"):
        monkeypatch.delenv(name, raising=False)
        monkeypatch.delenv(name.lower(), raising=False)


def test_default_database_matches_legacy_string():
    assert build_connection_string(Database()) == "mongodb://localhost:27017/product_catalog"


def test_no_credentials_has_no_at_sign():
    assert "@" not in build_connection_string(Database())


def test_user_without_password_omits_credentials():
    result = build_connection_string(Database(user="alice"))
    assert result == "mongodb://localhost:27017/product_catalog"


def test_password_without_user_omits_credentials():
    result = build_connection_string(Database(password="secret"))
    assert result == "mongodb://localhost:27017/product_catalog"


def test_special_characters_round_trip():
    result = build_connection_string(Database(user="us@er:name", password=SPECIAL_PASSWORD))
    parsed = parse_uri(result)
    assert parsed["username"] == "us@er:name"
    assert parsed["password"] == SPECIAL_PASSWORD
    assert parsed["nodelist"] == [("localhost", 27017)]
    assert parsed["database"] == "product_catalog"


def test_auth_source_in_query_string():
    result = build_connection_string(Database(auth_source="admin"))
    assert result.endswith("?authSource=admin")
    assert "tls" not in result


def test_tls_in_query_string():
    result = build_connection_string(Database(tls=True))
    assert result.endswith("?tls=true")
    assert "authSource" not in result


def test_auth_source_and_tls_together():
    result = build_connection_string(Database(user="u", password="p", auth_source="admin", tls=True))
    assert result == "mongodb://u:p@localhost:27017/product_catalog?authSource=admin&tls=true"
    options = parse_uri(result)["options"]
    assert options["authSource"] == "admin"
    assert options["tls"] is True
