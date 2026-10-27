# ruff: noqa: S101, D100, D101, D102, D103
"""Scope keys (store_id, deleted_at, ...) must win over caller-supplied filters in list_* queries."""

from dataclasses import dataclass
from datetime import UTC, datetime

import pytest
from pydantic import HttpUrl

from src.core.pagination import PaginationParams
from src.db import init_db
from src.domain.bundles import BundlesService
from src.domain.categories import CategoriesService
from src.domain.locations import LocationsService
from src.domain.products import ProductsService
from src.domain.stores import StoresService
from src.domain.types.bundles import NewBundle
from src.domain.types.categories import NewCategory
from src.domain.types.locations import NewLocation
from src.domain.types.products import NewProduct
from src.domain.types.stores import NewStore
from src.domain.types.variants import NewProductVariant, VariantOption
from src.domain.variants import VariantsService
from src.models.bundles import BundleModel
from src.models.categories import CategoryModel
from src.models.locations import LocationModel
from src.models.products import ProductModel
from src.models.variants import VariantModel


@pytest.fixture
async def beanie_db(mongodb, app_settings):
    client = await init_db(app_settings)
    yield
    await client.close()


@dataclass
class Scope:
    store_a: str
    store_b: str
    # model-native store id, as stored in documents
    store_b_id: object


@pytest.fixture
async def scope(beanie_db) -> Scope:
    stores = StoresService()
    store_a = await stores.create_store(NewStore(name="Store A", url=HttpUrl("https://store-a.example.com/")))
    store_b = await stores.create_store(NewStore(name="Store B", url=HttpUrl("https://store-b.example.com/")))
    return Scope(store_a=str(store_a.id), store_b=str(store_b.id), store_b_id=store_b.id)


async def _soft_delete(model, doc_id) -> None:
    doc = await model.get(doc_id)
    assert doc is not None
    doc.deleted_at = datetime.now(UTC)
    await doc.save()


def _ids(result) -> set:
    assert result is not None
    return {item.id for item in result.items}


async def test_categories_scope_keys_win(scope: Scope):
    service = CategoriesService()
    live = await service.create_category(scope.store_a, NewCategory(name="A live", path="/a-live"))
    deleted = await service.create_category(scope.store_a, NewCategory(name="A deleted", path="/a-deleted"))
    await service.create_category(scope.store_b, NewCategory(name="B", path="/b"))
    assert live and deleted
    await _soft_delete(CategoryModel, deleted.id)

    for filters in ({"store_id": scope.store_b_id}, {"deleted_at": {"$ne": None}}):
        result = await service.list_categories(scope.store_a, PaginationParams(), filters=filters)
        assert _ids(result) == {live.id}


async def test_locations_scope_keys_win(scope: Scope):
    service = LocationsService()
    live = await service.create_location(scope.store_a, NewLocation(name="A live"))
    deleted = await service.create_location(scope.store_a, NewLocation(name="A deleted"))
    await service.create_location(scope.store_b, NewLocation(name="B"))
    assert live and deleted
    await _soft_delete(LocationModel, deleted.id)

    for filters in ({"store_id": scope.store_b_id}, {"deleted_at": {"$ne": None}}):
        result = await service.list_locations(scope.store_a, PaginationParams(), filters=filters)
        assert _ids(result) == {live.id}


async def test_bundles_scope_keys_win(scope: Scope):
    service = BundlesService()
    live = await service.create_bundle(scope.store_a, NewBundle(name="A live"))
    deleted = await service.create_bundle(scope.store_a, NewBundle(name="A deleted"))
    await service.create_bundle(scope.store_b, NewBundle(name="B"))
    assert live and deleted
    await _soft_delete(BundleModel, deleted.id)

    for filters in ({"store_id": scope.store_b_id}, {"deleted_at": {"$ne": None}}):
        result = await service.list_bundles(scope.store_a, PaginationParams(), filters=filters)
        assert _ids(result) == {live.id}


async def test_variants_scope_keys_win(scope: Scope):
    products = ProductsService()
    service = VariantsService()
    product_a = await products.create_product(scope.store_a, NewProduct(tags=[], name="Product A"))
    product_b = await products.create_product(scope.store_b, NewProduct(tags=[], name="Product B"))
    assert product_a and product_b

    live = await service.create_variant(scope.store_a, str(product_a.id), NewProductVariant(title="A live", options=[]))
    other = await service.create_variant(
        scope.store_a,
        str(product_a.id),
        NewProductVariant(title="A deleted", options=[VariantOption(name="size", value="L")]),
    )
    await service.create_variant(scope.store_b, str(product_b.id), NewProductVariant(title="B", options=[]))
    assert live and other
    await _soft_delete(VariantModel, other.id)

    for filters in (
        {"store_id": scope.store_b_id},
        {"product_id": product_b.id},
        {"deleted_at": {"$ne": None}},
    ):
        result = await service.list_variants(scope.store_a, str(product_a.id), PaginationParams(), filters=filters)
        assert _ids(result) == {live.id}


async def test_products_scope_keys_win(scope: Scope):
    service = ProductsService()
    live = await service.create_product(scope.store_a, NewProduct(tags=[], name="A live"))
    deleted = await service.create_product(scope.store_a, NewProduct(tags=[], name="A deleted"))
    await service.create_product(scope.store_b, NewProduct(tags=[], name="B"))
    assert live and deleted
    await _soft_delete(ProductModel, deleted.id)

    for filters in ({"store_id": scope.store_b_id}, {"deleted_at": {"$ne": None}}):
        result = await service.list_products(scope.store_a, PaginationParams(), filters=filters)
        assert _ids(result) == {live.id}


async def test_products_variant_filters_scope_keys_win(scope: Scope):
    products = ProductsService()
    variants = VariantsService()
    with_live = await products.create_product(scope.store_a, NewProduct(tags=[], name="A with live variant"))
    with_deleted = await products.create_product(scope.store_a, NewProduct(tags=[], name="A with deleted variant"))
    in_b = await products.create_product(scope.store_b, NewProduct(tags=[], name="B with variant"))
    assert with_live and with_deleted and in_b

    await variants.create_variant(scope.store_a, str(with_live.id), NewProductVariant(title="live", options=[]))
    deleted_variant = await variants.create_variant(
        scope.store_a, str(with_deleted.id), NewProductVariant(title="deleted", options=[])
    )
    await variants.create_variant(scope.store_b, str(in_b.id), NewProductVariant(title="B", options=[]))
    assert deleted_variant
    await _soft_delete(VariantModel, deleted_variant.id)

    for variant_filters in ({"store_id": scope.store_b_id}, {"deleted_at": {"$ne": None}}):
        result = await products.list_products(scope.store_a, PaginationParams(), variant_filters=variant_filters)
        assert _ids(result) == {with_live.id}
