# ruff: noqa: S101, S105, D100, D101, D102, D103
from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from src.core.auth import ro_access, rw_access
from src.settings import get_settings

SETTINGS = SimpleNamespace(auth=SimpleNamespace(rw_x_api_key="rw-key", ro_x_api_key="ro-key"))


def _settings(rw, ro):
    return SimpleNamespace(auth=SimpleNamespace(rw_x_api_key=rw, ro_x_api_key=ro))


class TestRwAccess:
    def test_rw_key_is_accepted(self):
        assert rw_access("rw-key", SETTINGS) is None

    @pytest.mark.parametrize("key", ["ro-key", "nope", ""])
    def test_any_other_key_is_rejected(self, key):
        with pytest.raises(HTTPException) as exc:
            rw_access(key, SETTINGS)
        assert exc.value.status_code == 401
        assert exc.value.detail == "Invalid API Key"

    def test_non_ascii_key_is_rejected_not_type_error(self):
        with pytest.raises(HTTPException) as exc:
            rw_access("ключ", SETTINGS)
        assert exc.value.status_code == 401

    @pytest.mark.parametrize("key", ["rw-key", "", "ключ"])
    def test_unconfigured_rw_key_matches_nothing(self, key):
        with pytest.raises(HTTPException) as exc:
            rw_access(key, _settings(rw=None, ro="ro-key"))
        assert exc.value.status_code == 401

    def test_empty_configured_key_does_not_match_empty_header(self):
        with pytest.raises(HTTPException) as exc:
            rw_access("", _settings(rw="", ro="ro-key"))
        assert exc.value.status_code == 401


class TestRoAccess:
    @pytest.mark.parametrize("key", ["rw-key", "ro-key"])
    def test_rw_and_ro_keys_are_accepted(self, key):
        assert ro_access(key, SETTINGS) is None

    @pytest.mark.parametrize("key", ["nope", "", "RW-KEY"])
    def test_unknown_key_is_rejected(self, key):
        with pytest.raises(HTTPException) as exc:
            ro_access(key, SETTINGS)
        assert exc.value.status_code == 401
        assert exc.value.detail == "Invalid API Key"

    def test_non_ascii_key_is_rejected_not_type_error(self):
        with pytest.raises(HTTPException) as exc:
            ro_access("ключ", SETTINGS)
        assert exc.value.status_code == 401

    @pytest.mark.parametrize("key", ["nope", "ro-key", ""])
    def test_unconfigured_ro_key_matches_only_rw(self, key):
        with pytest.raises(HTTPException) as exc:
            ro_access(key, _settings(rw="rw-key", ro=None))
        assert exc.value.status_code == 401

    def test_unconfigured_ro_key_still_accepts_rw(self):
        assert ro_access("rw-key", _settings(rw="rw-key", ro=None)) is None

    def test_empty_configured_keys_do_not_match_empty_header(self):
        with pytest.raises(HTTPException) as exc:
            ro_access("", _settings(rw="", ro=""))
        assert exc.value.status_code == 401

    @pytest.mark.parametrize("key", ["", "rw-key", "ключ"])
    def test_nothing_configured_matches_nothing(self, key):
        with pytest.raises(HTTPException) as exc:
            ro_access(key, _settings(rw=None, ro=None))
        assert exc.value.status_code == 401


class TestGetSettings:
    @pytest.fixture(autouse=True)
    def _fresh_cache(self):
        get_settings.cache_clear()
        yield
        get_settings.cache_clear()

    def test_returns_the_same_object(self):
        assert get_settings() is get_settings()
