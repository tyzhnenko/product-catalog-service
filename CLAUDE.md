# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

Package management and task running use `uv` and `just` (see `Justfile`).

```bash
just run                # uv run python run_server.py
just lint               # ruff check src/ tests/
just format             # ruff format src/ tests/
just test               # pytest tests/
just pre-commit-install # uv run prek install
just pre-commit-run     # uv run prek run --all-files
just fetch-openapi       # regenerate openapi.json from the running app definition
just generate-client     # fetch-openapi + regenerate clients/python via openapi-python-client
```

Run a single test:
```bash
uv run pytest tests/test_endpoints/test_products.py::test_create_product -vv
```

Type checking is via mypy (run through pre-commit, not a `just` target):
```bash
uv run mypy src/
```

Tests spin up a real MongoDB (via `pytest-mongo`), not mocks — see `tests/conftest.py`. Locally it launches `mongod` (path configured in `pytest.ini` via `mongo_exec`/`mongo_port`); in CI (`CI` env var set) it uses `mongo_noproc` against a service container instead (`pytest-ci.ini`). Both configs force `APP_SETTINGS_FILE=settings.test.yaml`. There is no unit-test layer that mocks the DB — endpoint tests go through the real `TestClient` + Beanie + Mongo.

Docker Compose stack (app + Mongo + Mongo Express) for local exploration:
```bash
docker compose -p catalog -f docker/docker-compose.yaml up --build
```

## Architecture

FastAPI + Beanie (async MongoDB ODM) service with a strict layered structure repeated per resource (stores, categories, locations, products, variants, bundles):

```
src/controllers/<resource>.py   FastAPI routes: request/response wiring, HTTP status codes, calls into domain service
src/domain/<resource>.py        <Resource>Service class: business logic, orchestrates model queries
src/domain/types/<resource>.py  Pydantic API schemas (NewX, X, UpdateX, XID, enums) — what crosses the HTTP boundary
src/models/<resource>.py        Beanie Document classes — what's persisted in Mongo, extends BaseAppDocument
```

Controllers depend on domain services via `Depends(XService)` (services are stateless, instantiated per-request). Domain services never receive the request directly — they take plain values/schema objects and query models directly (no repository layer in between).

### Request flow
`src/main.py` builds the app: `configure_services()` (wires up Beanie lifespan via `src/core/services.py` + `src/db.py`) then `configure_application()` (docs, CORS, gzip, mounts `api_router` from `src/api_v1.py` at `/api/v1`). Each resource router is registered there with its own path prefix and OpenAPI tag.

### Auth
API-key based, via `x-api-key` header (`src/core/auth.py`). Two dependency functions gate routes: `rw_access` (must match `auth.rw_x_api_key`) for mutating endpoints, `ro_access` (matches either the RW or RO key) for reads. Applied per-route as `dependencies=[Security(rw_access)]` / `[Security(ro_access)]`.

### Settings
`src/settings.py` uses `pydantic-settings` layered from (highest to lowest precedence): init kwargs → env vars (`APP_` prefix, `__` nested delimiter) → `.env` → YAML file. The YAML file path comes from `APP_SETTINGS_FILE` (defaults to `settings.yaml`) — `settings.example.yaml` is the template to copy locally, `settings.test.yaml` is forced during tests. Settings sections: `info`, `app`, `auth`, `db`, `pagination`.

### Dynamic attributes and pricing
Products, variants, and bundles support open-ended, typed attribute maps rather than fixed columns. `src/domain/types/attributes.py` defines a tagged union `Attribute` (string/text/integer/float/decimal/bool/date/datetime/uuid/object_id/url, plus range and list/map variants of each) discriminated by a `type` literal, stored as `AttributesMap = dict[str, Attribute]`. Pricing follows the same shape in `src/domain/types/prices.py`: a tagged `Price` union (`decimal` / `decimal_range` / `decimal_quantity`) stored as `PriceMap`, with `LocationPriceMap` and `RegionPriceMap` nesting a `PriceMap` per location/country code. When adding a new attribute or price type, add the `BaseModel` variant and include it in the corresponding `type Attribute = Annotated[... | NewType, ...]` union — everything else (validation, OpenAPI schema, Mongo storage) follows from that.

Filtering on these dynamic maps happens via query-string mini-DSL parsed in `src/core/utils.py` (`build_attribute_filter`, `build_price_filter`, `build_location_price_filter`, `build_region_price_filter`), which build raw Mongo filter dicts (e.g. `attrs=color:red&attrs=color:blue` → OR via `$in`; different keys → AND). Products have a wildcard Mongo index on `attributes.$**` to support this.

### Pagination
Cursor-based, implemented once in `src/core/utils.py::paginate()` and reused by every service's `list_*` method. Cursors are base64-encoded Mongo `ObjectId`s (`encode_cursor`/`decode_cursor`); `after`/`before` query params page forward/backward. Returns `PaginatedResponse[T]` (`src/core/types.py`) with `items`, `start_cursor`, `end_cursor`, `has_next`, `has_prev`.

### Soft deletes and store scoping
All documents extend `BaseAppDocument` (`src/models/base.py`) with `created_at`/`updated_at`/`deleted_at`. Deletes set `deleted_at` rather than removing the row; every query filters `deleted_at: None`. Most resources (products, variants, bundles) are scoped under a `store_id` and every service method re-checks the parent store exists (and isn't soft-deleted) before touching the resource — follow this pattern for new store-scoped resources rather than trusting the path param alone.

### FastAPI lifespan composition
`src/core/types.py::FastAPIServices` lets independent modules register their own async lifespan context managers (currently just Beanie/Mongo init in `src/db.py::use_beanie`) which get combined into one `AsyncExitStack`-based lifespan in `build_combined_lifespan()`. Add new startup/shutdown resources (caches, other clients) by registering a lifespan here rather than hand-rolling FastAPI `@app.on_event`.

### Generated Python client
`clients/python` is generated output (via `just generate-client`), driven by `openapi.json` (fetched via `get_openapi.py`) and `openapi-python-client-config.yaml`. Don't hand-edit files under `clients/python` — regenerate instead.

## Conventions

- Commit messages follow Conventional Commits (`feat:`, `fix:`, `chore:`, `refactor:`, `test:`, etc. — see README for the full list); releases are automated via release-please based on these.
- Ruff line length 120, double quotes, target py313. Docstrings are optional (`D100-D107` ignored) but when present follow Google style (see `split_path` in `src/core/utils.py` for the expected format).
- `mypy` runs via pre-commit against `.venv/bin/python`, not standalone — install hooks with `just pre-commit-install` before relying on it locally.
