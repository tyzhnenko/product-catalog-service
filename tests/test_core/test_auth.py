# ruff: noqa: S101, S105, D100, D101, D102, D103
from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from src.core.auth import ro_access, rw_access

SETTINGS = SimpleNamespace(auth=SimpleNamespace(rw_x_api_key="rw-key", ro_x_api_key="ro-key"))


class TestRwAccess:
    def test_rw_key_is_accepted(self):
        assert rw_access("rw-key", SETTINGS) is None

    @pytest.mark.parametrize("key", ["ro-key", "nope", ""])
    def test_any_other_key_is_rejected(self, key):
        with pytest.raises(HTTPException) as exc:
            rw_access(key, SETTINGS)
        assert exc.value.status_code == 401
        assert exc.value.detail == "Invalid API Key"


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
