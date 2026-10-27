# ruff: noqa: S101, D100, D101, D102, D103


def test_non_ascii_api_key_is_rejected_with_401(api_client):
    # httpx only encodes str header values as ASCII, so send raw UTF-8 bytes.
    response = api_client.get("/api/v1/stores/", headers={"x-api-key": "ключ".encode()})
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid API Key"


def test_valid_api_key_is_accepted(api_client):
    assert api_client.get("/api/v1/stores/").status_code == 200
