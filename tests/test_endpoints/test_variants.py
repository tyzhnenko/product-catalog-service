# ruff: noqa: S101, D100, D101, D102, D103
import pytest
from beanie import PydanticObjectId


@pytest.fixture
def sample_store(api_client):
    """Create a sample store for testing variants."""
    store_data = {
        "name": "Test Store for Variants",
        "url": "https://teststorevariants.com/",
    }
    response = api_client.post("/api/v1/stores/", json=store_data)
    return response.json()


@pytest.fixture
def another_store(api_client):
    """Create another store for testing variants."""
    store_data = {
        "name": "Another Variant Store",
        "url": "https://anothervariantstore.com/",
    }
    response = api_client.post("/api/v1/stores/", json=store_data)
    return response.json()


@pytest.fixture
def sample_product(api_client, sample_store):
    """Create a sample product for testing variants."""
    product_data = {
        "name": "Ethiopian Coffee",
        "description": "Premium Ethiopian coffee beans",
        "tags": ["single-origin"],
    }
    response = api_client.post(f"/api/v1/products/{sample_store['id']}", json=product_data)
    return response.json()


@pytest.fixture
def another_product(api_client, sample_store):
    """Create another product for testing variants."""
    product_data = {
        "name": "Colombian Coffee",
        "description": "Colombian coffee beans",
        "tags": ["single-origin"],
    }
    response = api_client.post(f"/api/v1/products/{sample_store['id']}", json=product_data)
    return response.json()


@pytest.fixture
def sample_variant_data():
    """Sample data for creating a variant."""
    return {
        "title": "250g Whole Beans",
        "sku": "ETH-250-WB",
        "upc": "123456789012",
        "ean": "1234567890123",
        "options": [
            {"name": "Size", "value": "250g"},
            {"name": "Grind", "value": "Whole Beans"},
        ],
        "attributes": {
            "origin": {"type": "string", "name": "origin", "value": "Yirgacheffe"},
            "altitude": {"type": "integer", "name": "altitude", "value": 1800},
        },
    }


@pytest.fixture
def another_variant_data():
    """Another sample variant data for testing multiple variants."""
    return {
        "title": "500g Ground",
        "sku": "ETH-500-GR",
        "options": [
            {"name": "Size", "value": "500g"},
            {"name": "Grind", "value": "Ground"},
        ],
    }


@pytest.fixture
def minimal_variant_data():
    """Minimal variant data with only required fields."""
    return {
        "title": "Simple Variant",
        "options": [],
    }


@pytest.fixture
def comprehensive_variant_data():
    """Comprehensive variant data with all attribute and price types for testing MongoDB conversions."""
    from uuid import uuid4

    return {
        "title": "Comprehensive Test Variant",
        "sku": "COMP-TEST-001",
        "upc": "999999999999",
        "options": [{"name": "Test", "value": "Comprehensive"}],
        "attributes": {
            # Basic types
            "string_attr": {"type": "string", "name": "string_attr", "value": "test string"},
            "text_attr": {"type": "text", "name": "text_attr", "value": "This is a longer text description"},
            "integer_attr": {"type": "integer", "name": "integer_attr", "value": 42},
            "bool_attr": {"type": "bool", "name": "bool_attr", "value": True},
            "float_attr": {"type": "float", "name": "float_attr", "value": 3.14159},
            "decimal_attr": {"type": "decimal", "name": "decimal_attr", "value": "19.99"},
            "date_attr": {"type": "date", "name": "date_attr", "value": "2026-03-22"},
            "datetime_attr": {"type": "datetime", "name": "datetime_attr", "value": "2026-03-22T12:00:00Z"},
            "uuid_attr": {"type": "uuid", "name": "uuid_attr", "value": str(uuid4())},
            "url_attr": {"type": "url", "name": "url_attr", "value": "https://example.com"},
            # Range types
            "float_range_attr": {
                "type": "float_range",
                "name": "float_range_attr",
                "min_value": 0.0,
                "max_value": 100.0,
            },
            "integer_range_attr": {
                "type": "integer_range",
                "name": "integer_range_attr",
                "min_value": 10,
                "max_value": 50,
            },
            "decimal_range_attr": {
                "type": "decimal_range",
                "name": "decimal_range_attr",
                "min_value": "10.00",
                "max_value": "99.99",
            },
            # List types
            "list_strings_attr": {
                "type": "list_of_strings",
                "name": "list_strings_attr",
                "values": ["tag1", "tag2", "tag3"],
            },
            "list_integers_attr": {
                "type": "list_of_integers",
                "name": "list_integers_attr",
                "values": [1, 2, 3, 4, 5],
            },
            "list_floats_attr": {
                "type": "list_of_floats",
                "name": "list_floats_attr",
                "values": [1.1, 2.2, 3.3],
            },
            "list_decimals_attr": {
                "type": "list_of_decimals",
                "name": "list_decimals_attr",
                "values": ["10.99", "20.99", "30.99"],
            },
            # Map types
            "map_strings_attr": {
                "type": "map_of_strings",
                "name": "map_strings_attr",
                "values": {"key1": "value1", "key2": "value2"},
            },
            "map_integers_attr": {
                "type": "map_of_integers",
                "name": "map_integers_attr",
                "values": {"key1": 10, "key2": 20},
            },
            "map_floats_attr": {
                "type": "map_of_floats",
                "name": "map_floats_attr",
                "values": {"key1": 1.5, "key2": 2.5},
            },
            "map_decimals_attr": {
                "type": "map_of_decimals",
                "name": "map_decimals_attr",
                "values": {"price1": "15.99", "price2": "25.99"},
            },
        },
        "price": {
            # All price types
            "retail": {"type": "decimal", "name": "Retail Price", "value": "29.99"},
            "subscription_range": {
                "type": "decimal_range",
                "name": "Subscription Range",
                "min_value": "24.99",
                "max_value": "27.99",
            },
            "bulk_discount": {
                "type": "decimal_quantity",
                "name": "Bulk Discount",
                "min_quantity": 10,
                "value": "22.99",
            },
        },
    }


@pytest.fixture
def sample_location(api_client, sample_store):
    """Create a sample location for testing location-based pricing."""
    location_data = {
        "name": "Downtown Store",
        "attributes": {
            "address": {"type": "string", "name": "address", "value": "123 Main St"},
            "city": {"type": "string", "name": "city", "value": "Seattle"},
        },
    }
    response = api_client.post(f"/api/v1/locations/{sample_store['id']}", json=location_data)
    return response.json()


@pytest.fixture
def another_location(api_client, sample_store):
    """Create another location for testing."""
    location_data = {
        "name": "Airport Store",
        "attributes": {
            "address": {"type": "string", "name": "address", "value": "456 Airport Rd"},
            "city": {"type": "string", "name": "city", "value": "Seattle"},
        },
    }
    response = api_client.post(f"/api/v1/locations/{sample_store['id']}", json=location_data)
    return response.json()


class TestCreateVariant:
    """Tests for POST /api/v1/variants/{store_id}/{product_id}."""

    def test_create_variant_success(self, api_client, sample_variant_data, sample_store, sample_product):
        """Test successful variant creation."""
        response = api_client.post(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=sample_variant_data
        )

        assert response.status_code == 200
        data = response.json()

        assert data["title"] == sample_variant_data["title"]
        assert data["sku"] == sample_variant_data["sku"]
        assert data["product_id"] == sample_product["id"]
        assert len(data["options"]) == 2
        assert len(data["attributes"]) == 2
        assert "id" in data

    def test_create_variant_minimal_fields(self, api_client, minimal_variant_data, sample_store, sample_product):
        """Test variant creation with minimal required fields."""
        response = api_client.post(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=minimal_variant_data
        )

        assert response.status_code == 200
        data = response.json()

        assert data["title"] == minimal_variant_data["title"]
        assert data["options"] == []
        assert "id" in data

    def test_create_variant_missing_title(self, api_client, sample_store, sample_product):
        """Test variant creation without title."""
        invalid_data = {
            "options": [],
        }

        response = api_client.post(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=invalid_data)

        assert response.status_code == 422

    def test_create_variant_empty_title(self, api_client, sample_store, sample_product):
        """Test variant creation with empty title."""
        invalid_data = {
            "title": "",
            "options": [],
        }

        response = api_client.post(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=invalid_data)

        assert response.status_code == 422

    def test_create_variant_invalid_store_id(self, api_client, sample_variant_data, sample_product):
        """Test variant creation with invalid store_id format (rejected by path param validation)."""
        response = api_client.post(
            f"/api/v1/variants/not-a-valid-uuid/{sample_product['id']}", json=sample_variant_data
        )

        assert response.status_code == 422

    def test_create_variant_nonexistent_store(self, api_client, sample_variant_data, sample_product):
        """Test variant creation with non-existent store."""
        non_existent_store_id = str(PydanticObjectId())

        response = api_client.post(
            f"/api/v1/variants/{non_existent_store_id}/{sample_product['id']}", json=sample_variant_data
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "Product or store not found"

    def test_create_variant_nonexistent_product(self, api_client, sample_variant_data, sample_store):
        """Test variant creation with non-existent product."""
        non_existent_product_id = str(PydanticObjectId())

        response = api_client.post(
            f"/api/v1/variants/{sample_store['id']}/{non_existent_product_id}", json=sample_variant_data
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "Product or store not found"

    def test_create_variant_title_too_long(self, api_client, sample_store, sample_product):
        """Test variant creation with title exceeding max length."""
        invalid_data = {
            "title": "A" * 257,  # Max is 256
            "options": [],
        }

        response = api_client.post(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=invalid_data)

        assert response.status_code == 422

    def test_create_variant_with_duplicate_options(self, api_client, sample_store, sample_product, sample_variant_data):
        """Test that creating a variant with duplicate options fails."""
        # Create first variant
        response1 = api_client.post(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=sample_variant_data
        )
        assert response1.status_code == 200

        # Try to create second variant with same options
        duplicate_variant_data = {
            "title": "Different Title",
            "sku": "DIFFERENT-SKU",
            "options": sample_variant_data["options"],  # Same options
        }
        response2 = api_client.post(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=duplicate_variant_data
        )

        assert response2.status_code == 409
        assert "already exists" in response2.json()["detail"].lower()

    def test_create_variant_with_different_options(
        self, api_client, sample_store, sample_product, sample_variant_data, another_variant_data
    ):
        """Test that creating variants with different options succeeds."""
        # Create first variant
        response1 = api_client.post(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=sample_variant_data
        )
        assert response1.status_code == 200

        # Create second variant with different options - should succeed
        response2 = api_client.post(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=another_variant_data
        )
        assert response2.status_code == 200

    def test_create_variant_same_options_different_product(
        self, api_client, sample_store, sample_product, another_product, sample_variant_data
    ):
        """Test that same options can be used for variants of different products."""
        # Create variant for first product
        response1 = api_client.post(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=sample_variant_data
        )
        assert response1.status_code == 200

        # Create variant with same options for different product - should succeed
        response2 = api_client.post(
            f"/api/v1/variants/{sample_store['id']}/{another_product['id']}", json=sample_variant_data
        )
        assert response2.status_code == 200

    def test_create_variant_duplicate_slug_within_same_product_returns_409(
        self, api_client, sample_store, sample_product, sample_variant_data
    ):
        """Test that creating a second variant with the same slug within the same product returns 409."""
        variant_data = {**sample_variant_data, "seo": {"slug": "250g-whole-beans"}}
        first = api_client.post(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=variant_data)
        assert first.status_code == 200

        duplicate_data = {
            "title": "Different Title",
            "sku": "DIFFERENT-SKU",
            "options": [{"name": "Size", "value": "500g"}],
            "seo": {"slug": "250g-whole-beans"},
        }
        response = api_client.post(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=duplicate_data)

        assert response.status_code == 409

    def test_create_variant_same_slug_different_product_allowed(
        self, api_client, sample_store, sample_product, another_product, sample_variant_data
    ):
        """Test that the same variant slug can be reused across different products within one store."""
        variant_data = {**sample_variant_data, "seo": {"slug": "250g-whole-beans"}}
        response1 = api_client.post(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=variant_data)
        assert response1.status_code == 200

        response2 = api_client.post(f"/api/v1/variants/{sample_store['id']}/{another_product['id']}", json=variant_data)
        assert response2.status_code == 200

    def test_create_variant_empty_options_duplicate(self, api_client, sample_store, sample_product):
        """Test that creating multiple variants with empty options fails."""
        variant_data_1 = {
            "title": "Variant 1",
            "options": [],
        }
        variant_data_2 = {
            "title": "Variant 2",
            "options": [],
        }

        # Create first variant with empty options
        response1 = api_client.post(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=variant_data_1
        )
        assert response1.status_code == 200

        # Try to create second variant with empty options - should fail
        response2 = api_client.post(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=variant_data_2
        )
        assert response2.status_code == 409
        assert "already exists" in response2.json()["detail"].lower()


class TestListVariants:
    """Tests for GET /api/v1/variants/{store_id}/{product_id}."""

    def test_list_variants_by_store_slug(self, api_client, sample_variant_data):
        """Test that the store_id path segment also accepts an 's-<slug>' ref."""
        store_data = {
            "name": "Slug Store for Variants",
            "url": "https://slugstorevariants.com/",
            "seo": {"slug": "slug-store-variants"},
        }
        store = api_client.post("/api/v1/stores/", json=store_data).json()
        product = api_client.post(
            f"/api/v1/products/{store['id']}", json={"name": "Ethiopian Coffee", "tags": []}
        ).json()
        create_response = api_client.post(f"/api/v1/variants/{store['id']}/{product['id']}", json=sample_variant_data)
        created_variant = create_response.json()

        response = api_client.get(f"/api/v1/variants/s-slug-store-variants/{product['id']}")

        assert response.status_code == 200
        variants = response.json()["items"]
        assert len(variants) == 1
        assert variants[0]["id"] == created_variant["id"]

    def test_list_variants_empty(self, api_client, sample_store, sample_product):
        """Test listing variants when database is empty."""
        response = api_client.get(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}")

        assert response.status_code == 200
        assert response.json()["items"] == []

    def test_list_variants_with_one_variant(self, api_client, sample_variant_data, sample_store, sample_product):
        """Test listing variants with one variant in database."""
        # Create a variant first
        create_response = api_client.post(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=sample_variant_data
        )
        created_variant = create_response.json()

        # List variants
        response = api_client.get(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}")

        assert response.status_code == 200
        variants = response.json()["items"]
        assert len(variants) == 1
        assert variants[0]["id"] == created_variant["id"]
        assert variants[0]["title"] == sample_variant_data["title"]

    def test_list_variants_with_multiple_variants(
        self, api_client, sample_variant_data, another_variant_data, sample_store, sample_product
    ):
        """Test listing multiple variants."""
        # Create two variants
        api_client.post(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=sample_variant_data)
        api_client.post(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=another_variant_data)

        # List variants
        response = api_client.get(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}")

        assert response.status_code == 200
        variants = response.json()["items"]
        assert len(variants) == 2

        variant_titles = {variant["title"] for variant in variants}
        assert sample_variant_data["title"] in variant_titles
        assert another_variant_data["title"] in variant_titles

    def test_list_variants_different_products(
        self, api_client, sample_variant_data, sample_store, sample_product, another_product
    ):
        """Test that variants from different products are isolated."""
        # Create variant for first product
        api_client.post(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=sample_variant_data)

        # List variants for second product
        response = api_client.get(f"/api/v1/variants/{sample_store['id']}/{another_product['id']}")

        assert response.status_code == 200
        variants = response.json()["items"]
        assert len(variants) == 0

    def test_list_variants_nonexistent_product(self, api_client, sample_store):
        """Test listing variants for non-existent product."""
        non_existent_product_id = str(PydanticObjectId())

        response = api_client.get(f"/api/v1/variants/{sample_store['id']}/{non_existent_product_id}")

        assert response.status_code == 404
        assert response.json()["detail"] == "Product or store not found"

    def test_list_variants_filter_by_location_price_id(
        self, api_client, minimal_variant_data, sample_store, sample_product, sample_location
    ):
        """'loc:<id>' alone (no key) narrows to variants priced at that location."""
        priced_variant_data = {
            **minimal_variant_data,
            "location_price": {
                sample_location["id"]: {
                    "retail": {"type": "decimal", "name": "Retail Price", "value": "12.50"},
                }
            },
        }
        priced = api_client.post(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=priced_variant_data
        ).json()
        api_client.post(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=minimal_variant_data)

        response = api_client.get(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}",
            params={"price": f"loc:{sample_location['id']}"},
        )

        assert response.status_code == 200
        items = response.json()["items"]
        assert len(items) == 1
        assert items[0]["id"] == priced["id"]

    def test_list_variants_invalid_price_token_returns_400(self, api_client, sample_store, sample_product):
        """A price token with a non-numeric range value is rejected."""
        response = api_client.get(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}",
            params={"price": "USD>=notanumber"},
        )

        assert response.status_code == 400


class TestGetVariant:
    """Tests for GET /api/v1/variants/{store_id}/{product_id}/{variant_id}."""

    def test_get_variant_success(self, api_client, sample_variant_data, sample_store, sample_product):
        """Test successful retrieval of a specific variant."""
        # Create a variant first
        create_response = api_client.post(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=sample_variant_data
        )
        created_variant = create_response.json()
        variant_id = created_variant["id"]

        # Get the variant
        response = api_client.get(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}/{variant_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == variant_id
        assert data["title"] == sample_variant_data["title"]
        assert data["sku"] == sample_variant_data["sku"]

    def test_get_variant_not_found(self, api_client, sample_store, sample_product):
        """Test getting a non-existent variant."""
        non_existent_id = str(PydanticObjectId())

        response = api_client.get(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}/{non_existent_id}")

        assert response.status_code == 404
        assert response.json()["detail"] == "Variant not found"

    def test_get_variant_by_slug(self, api_client, sample_variant_data, sample_store, sample_product):
        """Test that a variant can be looked up by its 's-<slug>' ref, resolving to the same document."""
        variant_data = {**sample_variant_data, "seo": {"slug": "250g-whole-beans"}}
        create_response = api_client.post(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=variant_data
        )
        created_variant = create_response.json()

        response = api_client.get(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}/s-250g-whole-beans")

        assert response.status_code == 200
        assert response.json()["id"] == created_variant["id"]

    def test_get_variant_by_slug_with_product_slug(self, api_client, sample_variant_data, sample_store):
        """Test end-to-end slug resolution: both product_id and variant_id as 's-<slug>' refs."""
        product_data = {
            "name": "Ethiopian Coffee",
            "tags": ["single-origin"],
            "seo": {"slug": "ethiopian-coffee"},
        }
        product_response = api_client.post(f"/api/v1/products/{sample_store['id']}", json=product_data)
        product = product_response.json()

        variant_data = {**sample_variant_data, "seo": {"slug": "250g-whole-beans"}}
        create_response = api_client.post(f"/api/v1/variants/{sample_store['id']}/{product['id']}", json=variant_data)
        created_variant = create_response.json()

        response = api_client.get(f"/api/v1/variants/{sample_store['id']}/s-ethiopian-coffee/s-250g-whole-beans")

        assert response.status_code == 200
        assert response.json()["id"] == created_variant["id"]

    def test_get_variant_wrong_product(
        self, api_client, sample_variant_data, sample_store, sample_product, another_product
    ):
        """Test getting a variant from wrong product."""
        # Create variant for first product
        create_response = api_client.post(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=sample_variant_data
        )
        variant_id = create_response.json()["id"]

        # Try to get from second product
        response = api_client.get(f"/api/v1/variants/{sample_store['id']}/{another_product['id']}/{variant_id}")

        assert response.status_code == 404
        assert response.json()["detail"] == "Variant not found"

    def test_get_variant_invalid_uuid(self, api_client, sample_store, sample_product):
        """Test getting a variant with invalid UUID format (rejected by path param validation)."""
        invalid_id = "not-a-valid-uuid"

        response = api_client.get(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}/{invalid_id}")

        assert response.status_code == 422


class TestUpdateVariant:
    """Tests for PUT /api/v1/variants/{store_id}/{product_id}/{variant_id}."""

    def test_update_variant_title(self, api_client, sample_variant_data, sample_store, sample_product):
        """Test updating variant title."""
        # Create a variant first
        create_response = api_client.post(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=sample_variant_data
        )
        variant_id = create_response.json()["id"]

        # Update the variant title
        update_data = {"title": "Updated Variant Title"}
        response = api_client.patch(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}/{variant_id}", json=update_data
        )

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == variant_id
        assert data["title"] == "Updated Variant Title"
        assert data["sku"] == sample_variant_data["sku"]  # Should remain unchanged

    def test_update_variant_sku(self, api_client, sample_variant_data, sample_store, sample_product):
        """Test updating variant SKU."""
        # Create a variant first
        create_response = api_client.post(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=sample_variant_data
        )
        variant_id = create_response.json()["id"]

        # Update the SKU
        update_data = {"sku": "NEW-SKU-123"}
        response = api_client.patch(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}/{variant_id}", json=update_data
        )

        assert response.status_code == 200
        data = response.json()
        assert data["sku"] == "NEW-SKU-123"

    def test_update_variant_options(self, api_client, sample_variant_data, sample_store, sample_product):
        """Test updating variant options."""
        # Create a variant first
        create_response = api_client.post(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=sample_variant_data
        )
        variant_id = create_response.json()["id"]

        # Update options
        update_data = {"options": [{"name": "Weight", "value": "1kg"}]}
        response = api_client.patch(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}/{variant_id}", json=update_data
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["options"]) == 1
        assert data["options"][0]["name"] == "Weight"

    def test_update_variant_attributes(self, api_client, sample_variant_data, sample_store, sample_product):
        """Test updating variant attributes."""
        # Create a variant first
        create_response = api_client.post(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=sample_variant_data
        )
        variant_id = create_response.json()["id"]

        # Update attributes
        update_data = {"attributes": {"color": {"type": "string", "name": "color", "value": "brown"}}}
        response = api_client.patch(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}/{variant_id}", json=update_data
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["attributes"]) == 1
        assert "color" in data["attributes"]
        assert data["attributes"]["color"]["name"] == "color"

    def test_update_variant_not_found(self, api_client, sample_store, sample_product):
        """Test updating a non-existent variant."""
        non_existent_id = str(PydanticObjectId())

        update_data = {"title": "Updated Title"}
        response = api_client.patch(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}/{non_existent_id}", json=update_data
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "Variant not found"

    def test_update_variant_nonexistent_store(self, api_client, sample_variant_data, sample_store, sample_product):
        """Test updating a variant scoped to a well-formed but non-existent store."""
        create_response = api_client.post(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=sample_variant_data
        )
        variant_id = create_response.json()["id"]

        non_existent_store_id = str(PydanticObjectId())
        update_data = {"title": "Hacked Title"}
        response = api_client.patch(
            f"/api/v1/variants/{non_existent_store_id}/{sample_product['id']}/{variant_id}", json=update_data
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "Variant not found"

    def test_update_variant_duplicate_slug_returns_409(
        self, api_client, sample_store, sample_product, sample_variant_data
    ):
        """Test that updating a variant's slug to collide with another variant on the same product returns 409."""
        first_data = {**sample_variant_data, "seo": {"slug": "first-variant"}}
        second_data = {
            "title": "Second Variant",
            "options": [{"name": "Size", "value": "1kg"}],
            "seo": {"slug": "second-variant"},
        }
        api_client.post(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=first_data)
        second = api_client.post(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=second_data
        ).json()

        response = api_client.patch(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}/{second['id']}",
            json={"seo": {"slug": "first-variant"}},
        )

        assert response.status_code == 409

    def test_update_variant_wrong_product(
        self, api_client, sample_variant_data, sample_store, sample_product, another_product
    ):
        """Test updating a variant from wrong product."""
        # Create variant for first product
        create_response = api_client.post(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=sample_variant_data
        )
        variant_id = create_response.json()["id"]

        # Try to update from second product
        update_data = {"title": "Hacked Title"}
        response = api_client.patch(
            f"/api/v1/variants/{sample_store['id']}/{another_product['id']}/{variant_id}", json=update_data
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "Variant not found"

    def test_update_variant_with_duplicate_options(
        self, api_client, sample_store, sample_product, sample_variant_data, another_variant_data
    ):
        """Test that updating a variant to have duplicate options fails."""
        # Create first variant
        response1 = api_client.post(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=sample_variant_data
        )
        variant1_id = response1.json()["id"]
        assert response1.status_code == 200

        # Create second variant with different options
        response2 = api_client.post(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=another_variant_data
        )
        variant2_id = response2.json()["id"]
        assert response2.status_code == 200
        assert variant1_id != variant2_id

        # Try to update second variant to have same options as first - should fail
        update_data = {"options": sample_variant_data["options"]}
        response = api_client.patch(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}/{variant2_id}", json=update_data
        )

        assert response.status_code == 409
        assert "already exists" in response.json()["detail"].lower()

    def test_update_variant_with_same_options(self, api_client, sample_store, sample_product, sample_variant_data):
        """Test that updating a variant with its own options succeeds."""
        # Create a variant
        create_response = api_client.post(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=sample_variant_data
        )
        variant_id = create_response.json()["id"]

        # Update the variant with the same options (and different title) - should succeed
        update_data = {
            "title": "Updated Title",
            "options": sample_variant_data["options"],
        }
        response = api_client.patch(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}/{variant_id}", json=update_data
        )

        assert response.status_code == 200
        assert response.json()["title"] == "Updated Title"
        assert response.json()["options"] == sample_variant_data["options"]

    def test_update_variant_options_to_unique(
        self, api_client, sample_store, sample_product, sample_variant_data, another_variant_data
    ):
        """Test that updating a variant to have unique options succeeds."""
        # Create first variant
        response1 = api_client.post(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=sample_variant_data
        )
        variant1_id = response1.json()["id"]

        # Create second variant
        response2 = api_client.post(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=another_variant_data
        )
        variant2_id = response2.json()["id"]
        assert response2.status_code == 200
        assert variant1_id != variant2_id

        # Update first variant to have completely different options - should succeed
        new_options = [
            {"name": "Size", "value": "1kg"},
            {"name": "Type", "value": "Organic"},
        ]
        update_data = {"options": new_options}
        response = api_client.patch(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}/{variant1_id}", json=update_data
        )

        assert response.status_code == 200
        assert response.json()["options"] == new_options


class TestDeleteVariant:
    """Tests for DELETE /api/v1/variants/{store_id}/{product_id}/{variant_id}."""

    def test_delete_variant_success(self, api_client, sample_variant_data, sample_store, sample_product):
        """Test successful soft delete of a variant."""
        # Create a variant first
        create_response = api_client.post(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=sample_variant_data
        )
        variant_id = create_response.json()["id"]

        # Delete the variant
        response = api_client.delete(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}/{variant_id}")

        assert response.status_code == 204

    def test_delete_variant_not_found(self, api_client, sample_store, sample_product):
        """Test deleting a non-existent variant."""
        non_existent_id = str(PydanticObjectId())

        response = api_client.delete(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}/{non_existent_id}")

        assert response.status_code == 404
        assert response.json()["detail"] == "Variant not found"

    def test_delete_variant_nonexistent_store(self, api_client, sample_variant_data, sample_store, sample_product):
        """Test deleting a variant scoped to a well-formed but non-existent store."""
        create_response = api_client.post(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=sample_variant_data
        )
        variant_id = create_response.json()["id"]

        non_existent_store_id = str(PydanticObjectId())
        response = api_client.delete(f"/api/v1/variants/{non_existent_store_id}/{sample_product['id']}/{variant_id}")

        assert response.status_code == 404
        assert response.json()["detail"] == "Variant not found"

    def test_delete_variant_wrong_product(
        self, api_client, sample_variant_data, sample_store, sample_product, another_product
    ):
        """Test deleting a variant from wrong product."""
        # Create variant for first product
        create_response = api_client.post(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=sample_variant_data
        )
        variant_id = create_response.json()["id"]

        # Try to delete from second product
        response = api_client.delete(f"/api/v1/variants/{sample_store['id']}/{another_product['id']}/{variant_id}")

        assert response.status_code == 404
        assert response.json()["detail"] == "Variant not found"

    def test_delete_variant_invalid_uuid(self, api_client, sample_store, sample_product):
        """Test deleting a variant with invalid UUID format (rejected by path param validation)."""
        invalid_id = "not-a-valid-uuid"

        response = api_client.delete(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}/{invalid_id}")

        assert response.status_code == 422


class TestVariantCRUDIntegration:
    """Integration tests for complete CRUD workflows."""

    def test_full_crud_lifecycle(self, api_client, sample_variant_data, sample_store, sample_product):
        """Test the complete CRUD lifecycle of a variant."""
        # Create
        create_response = api_client.post(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=sample_variant_data
        )
        assert create_response.status_code == 200
        created_variant = create_response.json()
        variant_id = created_variant["id"]

        # Read (single)
        get_response = api_client.get(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}/{variant_id}")
        assert get_response.status_code == 200
        assert get_response.json()["id"] == variant_id

        # Read (list)
        list_response = api_client.get(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}")
        assert list_response.status_code == 200
        assert len(list_response.json()["items"]) >= 1

        # Update
        update_data = {
            "title": "Updated Variant Title",
            "sku": "UPDATED-SKU",
        }
        update_response = api_client.patch(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}/{variant_id}", json=update_data
        )
        assert update_response.status_code == 200
        assert update_response.json()["title"] == "Updated Variant Title"
        assert update_response.json()["sku"] == "UPDATED-SKU"

        # Verify update
        get_updated_response = api_client.get(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}/{variant_id}"
        )
        assert get_updated_response.status_code == 200
        assert get_updated_response.json()["title"] == "Updated Variant Title"

        # Delete
        delete_response = api_client.delete(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}/{variant_id}"
        )
        assert delete_response.status_code == 204

        # Verify deletion
        get_deleted_response = api_client.get(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}/{variant_id}"
        )
        assert get_deleted_response.status_code == 404

    def test_multiple_variants_for_product(
        self, api_client, sample_variant_data, another_variant_data, sample_store, sample_product
    ):
        """Test creating and managing multiple variants for the same product."""
        # Create first variant
        variant1_response = api_client.post(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=sample_variant_data
        )
        assert variant1_response.status_code == 200
        variant1_id = variant1_response.json()["id"]

        # Create second variant
        variant2_response = api_client.post(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=another_variant_data
        )
        assert variant2_response.status_code == 200
        variant2_id = variant2_response.json()["id"]

        # List variants - should have both
        list_response = api_client.get(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}")
        assert list_response.status_code == 200
        variants = list_response.json()["items"]
        assert len(variants) == 2

        variant_ids = {v["id"] for v in variants}
        assert variant1_id in variant_ids
        assert variant2_id in variant_ids

        # Update first variant
        update_response = api_client.patch(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}/{variant1_id}",
            json={"title": "Updated First Variant"},
        )
        assert update_response.status_code == 200

        # Delete second variant
        delete_response = api_client.delete(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}/{variant2_id}"
        )
        assert delete_response.status_code == 204


class TestVariantPriceMap:
    """Tests for priceMap functionality in variants."""

    def test_create_variant_with_decimal_price(self, api_client, sample_store, sample_product):
        """Test creating a variant with a decimal price."""
        variant_data = {
            "title": "Coffee 250g",
            "sku": "COFFEE-250",
            "options": [{"name": "Size", "value": "250g"}],
            "price": {
                "retail": {
                    "type": "decimal",
                    "name": "Retail Price",
                    "value": "19.99",
                }
            },
        }

        response = api_client.post(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=variant_data)

        assert response.status_code == 200
        data = response.json()
        assert "price" in data
        assert "retail" in data["price"]
        assert data["price"]["retail"]["type"] == "decimal"
        assert data["price"]["retail"]["name"] == "Retail Price"
        assert data["price"]["retail"]["value"] == "19.99"

    def test_create_variant_with_multiple_prices(self, api_client, sample_store, sample_product):
        """Test creating a variant with multiple price types."""
        variant_data = {
            "title": "Coffee 500g",
            "options": [],
            "price": {
                "retail": {
                    "type": "decimal",
                    "name": "Retail Price",
                    "value": "35.50",
                },
                "wholesale": {
                    "type": "decimal",
                    "name": "Wholesale Price",
                    "value": "28.00",
                },
                "member": {
                    "type": "decimal",
                    "name": "Member Price",
                    "value": "31.99",
                },
            },
        }

        response = api_client.post(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=variant_data)

        assert response.status_code == 200
        data = response.json()
        assert len(data["price"]) == 3
        assert "retail" in data["price"]
        assert "wholesale" in data["price"]
        assert "member" in data["price"]

    def test_create_variant_with_decimal_range_price(self, api_client, sample_store, sample_product):
        """Test creating a variant with a decimal range price."""
        variant_data = {
            "title": "Coffee Subscription",
            "options": [],
            "price": {
                "subscription": {
                    "type": "decimal_range",
                    "name": "Subscription Price Range",
                    "min_value": "25.00",
                    "max_value": "45.00",
                }
            },
        }

        response = api_client.post(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=variant_data)

        assert response.status_code == 200
        data = response.json()
        assert data["price"]["subscription"]["type"] == "decimal_range"
        assert data["price"]["subscription"]["min_value"] == "25.00"
        assert data["price"]["subscription"]["max_value"] == "45.00"

    def test_create_variant_with_decimal_quantity_price(self, api_client, sample_store, sample_product):
        """Test creating a variant with a decimal quantity price."""
        variant_data = {
            "title": "Coffee Bulk",
            "options": [],
            "price": {
                "bulk_tier_1": {
                    "type": "decimal_quantity",
                    "name": "Bulk Price 10+",
                    "min_quantity": 10,
                    "value": "15.99",
                },
                "bulk_tier_2": {
                    "type": "decimal_quantity",
                    "name": "Bulk Price 50+",
                    "min_quantity": 50,
                    "value": "12.99",
                },
            },
        }

        response = api_client.post(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=variant_data)

        assert response.status_code == 200
        data = response.json()
        assert data["price"]["bulk_tier_1"]["type"] == "decimal_quantity"
        assert data["price"]["bulk_tier_1"]["min_quantity"] == 10
        assert data["price"]["bulk_tier_1"]["value"] == "15.99"
        assert data["price"]["bulk_tier_2"]["min_quantity"] == 50

    def test_create_variant_with_mixed_price_types(self, api_client, sample_store, sample_product):
        """Test creating a variant with mixed price types."""
        variant_data = {
            "title": "Coffee Premium",
            "options": [],
            "price": {
                "retail": {
                    "type": "decimal",
                    "name": "Retail Price",
                    "value": "29.99",
                },
                "subscription": {
                    "type": "decimal_range",
                    "name": "Subscription Range",
                    "min_value": "24.99",
                    "max_value": "27.99",
                },
                "bulk": {
                    "type": "decimal_quantity",
                    "name": "Bulk Discount",
                    "min_quantity": 20,
                    "value": "22.99",
                },
            },
        }

        response = api_client.post(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=variant_data)

        assert response.status_code == 200
        data = response.json()
        assert len(data["price"]) == 3
        assert data["price"]["retail"]["type"] == "decimal"
        assert data["price"]["subscription"]["type"] == "decimal_range"
        assert data["price"]["bulk"]["type"] == "decimal_quantity"

    def test_create_variant_with_empty_price_map(self, api_client, sample_store, sample_product):
        """Test creating a variant with an empty price map."""
        variant_data = {
            "title": "Coffee No Price",
            "options": [],
            "price": {},
        }

        response = api_client.post(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=variant_data)

        assert response.status_code == 200
        data = response.json()
        assert data["price"] == {}

    def test_create_variant_without_price_map(self, api_client, sample_store, sample_product):
        """Test creating a variant without a price map (null)."""
        variant_data = {
            "title": "Coffee Default",
            "options": [],
        }

        response = api_client.post(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=variant_data)

        assert response.status_code == 200
        data = response.json()
        assert data["price"] is None

    def test_update_variant_add_price(self, api_client, sample_store, sample_product):
        """Test adding a price to a variant that had no price."""
        # Create variant without price
        variant_data = {"title": "Coffee", "options": []}
        create_response = api_client.post(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=variant_data
        )
        variant_id = create_response.json()["id"]

        # Add price
        update_data = {
            "price": {
                "retail": {
                    "type": "decimal",
                    "name": "Retail Price",
                    "value": "24.99",
                }
            }
        }
        response = api_client.patch(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}/{variant_id}", json=update_data
        )

        assert response.status_code == 200
        data = response.json()
        assert data["price"]["retail"]["value"] == "24.99"

    def test_update_variant_modify_price(self, api_client, sample_store, sample_product):
        """Test modifying an existing price in a variant."""
        # Create variant with price
        variant_data = {
            "title": "Coffee",
            "options": [],
            "price": {
                "retail": {
                    "type": "decimal",
                    "name": "Retail Price",
                    "value": "20.00",
                }
            },
        }
        create_response = api_client.post(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=variant_data
        )
        variant_id = create_response.json()["id"]

        # Update price value
        update_data = {
            "price": {
                "retail": {
                    "type": "decimal",
                    "name": "Retail Price",
                    "value": "22.50",
                }
            }
        }
        response = api_client.patch(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}/{variant_id}", json=update_data
        )

        assert response.status_code == 200
        data = response.json()
        assert data["price"]["retail"]["value"] == "22.50"

    def test_update_variant_add_multiple_prices(self, api_client, sample_store, sample_product):
        """Test adding multiple prices to a variant."""
        # Create variant with one price
        variant_data = {
            "title": "Coffee",
            "options": [],
            "price": {
                "retail": {
                    "type": "decimal",
                    "name": "Retail Price",
                    "value": "30.00",
                }
            },
        }
        create_response = api_client.post(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=variant_data
        )
        variant_id = create_response.json()["id"]

        # Add more prices
        update_data = {
            "price": {
                "retail": {
                    "type": "decimal",
                    "name": "Retail Price",
                    "value": "30.00",
                },
                "wholesale": {
                    "type": "decimal",
                    "name": "Wholesale Price",
                    "value": "24.00",
                },
                "member": {
                    "type": "decimal",
                    "name": "Member Price",
                    "value": "27.00",
                },
            }
        }
        response = api_client.patch(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}/{variant_id}", json=update_data
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["price"]) == 3
        assert "wholesale" in data["price"]
        assert "member" in data["price"]

    def test_update_variant_remove_price(self, api_client, sample_store, sample_product):
        """Test removing price from a variant."""
        # Create variant with price
        variant_data = {
            "title": "Coffee",
            "options": [],
            "price": {
                "retail": {
                    "type": "decimal",
                    "name": "Retail Price",
                    "value": "25.00",
                }
            },
        }
        create_response = api_client.post(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=variant_data
        )
        variant_id = create_response.json()["id"]

        # Remove price by setting to empty dict
        update_data = {"price": {}}
        response = api_client.patch(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}/{variant_id}", json=update_data
        )

        assert response.status_code == 200
        data = response.json()
        assert data["price"] == {}

    def test_list_variants_with_prices(self, api_client, sample_store, sample_product):
        """Test listing variants correctly returns price information."""
        # Create multiple variants with different prices
        variant1_data = {
            "title": "Small Size",
            "options": [{"name": "Size", "value": "Small"}],
            "price": {"retail": {"type": "decimal", "name": "Retail Price", "value": "15.99"}},
        }
        variant2_data = {
            "title": "Large Size",
            "options": [{"name": "Size", "value": "Large"}],
            "price": {"retail": {"type": "decimal", "name": "Retail Price", "value": "29.99"}},
        }

        api_client.post(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=variant1_data)
        api_client.post(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=variant2_data)

        # List variants
        response = api_client.get(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}")

        assert response.status_code == 200
        variants = response.json()["items"]
        assert len(variants) == 2

        # Both should have price data
        for variant in variants:
            assert "price" in variant
            assert variant["price"] is not None
            assert "retail" in variant["price"]

    def test_get_variant_with_price(self, api_client, sample_store, sample_product):
        """Test getting a specific variant returns complete price information."""
        variant_data = {
            "title": "Premium Coffee",
            "options": [],
            "price": {
                "retail": {"type": "decimal", "name": "Retail Price", "value": "39.99"},
                "wholesale": {"type": "decimal", "name": "Wholesale Price", "value": "32.00"},
            },
        }

        create_response = api_client.post(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=variant_data
        )
        variant_id = create_response.json()["id"]

        # Get the variant
        response = api_client.get(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}/{variant_id}")

        assert response.status_code == 200
        data = response.json()
        assert len(data["price"]) == 2
        assert data["price"]["retail"]["value"] == "39.99"
        assert data["price"]["wholesale"]["value"] == "32.00"

    def test_create_variant_invalid_price_type(self, api_client, sample_store, sample_product):
        """Test creating a variant with invalid price type."""
        variant_data = {
            "title": "Coffee",
            "options": [],
            "price": {
                "retail": {
                    "type": "invalid_type",
                    "name": "Retail Price",
                    "value": "20.00",
                }
            },
        }

        response = api_client.post(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=variant_data)

        assert response.status_code == 422

    def test_create_variant_missing_price_fields(self, api_client, sample_store, sample_product):
        """Test creating a variant with missing required price fields."""
        variant_data = {
            "title": "Coffee",
            "options": [],
            "price": {
                "retail": {
                    "type": "decimal",
                    "name": "Retail Price",
                    # Missing 'value' field
                }
            },
        }

        response = api_client.post(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=variant_data)

        assert response.status_code == 422

    def test_create_variant_invalid_decimal_value(self, api_client, sample_store, sample_product):
        """Test creating a variant with invalid decimal value."""
        variant_data = {
            "title": "Coffee",
            "options": [],
            "price": {
                "retail": {
                    "type": "decimal",
                    "name": "Retail Price",
                    "value": "not-a-number",
                }
            },
        }

        response = api_client.post(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=variant_data)

        assert response.status_code == 422

    def test_price_decimal_precision(self, api_client, sample_store, sample_product):
        """Test that decimal prices maintain precision."""
        variant_data = {
            "title": "Coffee",
            "options": [],
            "price": {
                "retail": {
                    "type": "decimal",
                    "name": "Retail Price",
                    "value": "19.9950",  # Extra precision
                }
            },
        }

        response = api_client.post(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=variant_data)

        assert response.status_code == 200
        data = response.json()
        # Check that decimal precision is preserved
        assert "19.99" in data["price"]["retail"]["value"] or data["price"]["retail"]["value"] == "19.9950"


class TestVariantLocationPrice:
    """Tests for location_price functionality in variants."""

    def test_create_variant_with_location_price(self, api_client, sample_store, sample_product, sample_location):
        """Test creating a variant with location-specific pricing."""
        variant_data = {
            "title": "Coffee with Location Price",
            "options": [],
            "location_price": {
                sample_location["id"]: {
                    "retail": {
                        "type": "decimal",
                        "name": "Downtown Retail Price",
                        "value": "22.99",
                    }
                }
            },
        }

        response = api_client.post(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=variant_data)

        assert response.status_code == 200
        data = response.json()
        assert "location_price" in data
        assert sample_location["id"] in data["location_price"]
        assert data["location_price"][sample_location["id"]]["retail"]["value"] == "22.99"

    def test_create_variant_with_multiple_location_prices(
        self, api_client, sample_store, sample_product, sample_location, another_location
    ):
        """Test creating a variant with prices for multiple locations."""
        variant_data = {
            "title": "Coffee Multi-Location",
            "options": [],
            "location_price": {
                sample_location["id"]: {
                    "retail": {"type": "decimal", "name": "Downtown Price", "value": "20.00"},
                    "member": {"type": "decimal", "name": "Downtown Member Price", "value": "18.00"},
                },
                another_location["id"]: {
                    "retail": {"type": "decimal", "name": "Airport Price", "value": "25.00"},
                    "member": {"type": "decimal", "name": "Airport Member Price", "value": "23.00"},
                },
            },
        }

        response = api_client.post(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=variant_data)

        assert response.status_code == 200
        data = response.json()
        assert len(data["location_price"]) == 2
        assert sample_location["id"] in data["location_price"]
        assert another_location["id"] in data["location_price"]
        assert data["location_price"][sample_location["id"]]["retail"]["value"] == "20.00"
        assert data["location_price"][another_location["id"]]["retail"]["value"] == "25.00"

    def test_create_variant_with_location_range_prices(self, api_client, sample_store, sample_product, sample_location):
        """Test creating a variant with location-specific range prices."""
        variant_data = {
            "title": "Coffee Location Range",
            "options": [],
            "location_price": {
                sample_location["id"]: {
                    "subscription": {
                        "type": "decimal_range",
                        "name": "Subscription Range",
                        "min_value": "18.00",
                        "max_value": "22.00",
                    }
                }
            },
        }

        response = api_client.post(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=variant_data)

        assert response.status_code == 200
        data = response.json()
        assert data["location_price"][sample_location["id"]]["subscription"]["type"] == "decimal_range"
        assert data["location_price"][sample_location["id"]]["subscription"]["min_value"] == "18.00"

    def test_create_variant_with_location_quantity_prices(
        self, api_client, sample_store, sample_product, sample_location
    ):
        """Test creating a variant with location-specific quantity-based pricing."""
        variant_data = {
            "title": "Coffee Location Bulk",
            "options": [],
            "location_price": {
                sample_location["id"]: {
                    "bulk_10": {
                        "type": "decimal_quantity",
                        "name": "Bulk 10+",
                        "min_quantity": 10,
                        "value": "15.00",
                    },
                    "bulk_50": {
                        "type": "decimal_quantity",
                        "name": "Bulk 50+",
                        "min_quantity": 50,
                        "value": "12.00",
                    },
                }
            },
        }

        response = api_client.post(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=variant_data)

        assert response.status_code == 200
        data = response.json()
        location_prices = data["location_price"][sample_location["id"]]
        assert location_prices["bulk_10"]["min_quantity"] == 10
        assert location_prices["bulk_50"]["value"] == "12.00"

    def test_update_variant_add_location_price(self, api_client, sample_store, sample_product, sample_location):
        """Test adding location price to a variant."""
        # Create variant without location price
        variant_data = {"title": "Coffee", "options": []}
        create_response = api_client.post(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=variant_data
        )
        variant_id = create_response.json()["id"]

        # Add location price
        update_data = {
            "location_price": {
                sample_location["id"]: {"retail": {"type": "decimal", "name": "Downtown Price", "value": "21.00"}}
            }
        }
        response = api_client.patch(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}/{variant_id}", json=update_data
        )

        assert response.status_code == 200
        data = response.json()
        assert sample_location["id"] in data["location_price"]
        assert data["location_price"][sample_location["id"]]["retail"]["value"] == "21.00"

    def test_update_variant_modify_location_price(self, api_client, sample_store, sample_product, sample_location):
        """Test modifying existing location price."""
        # Create variant with location price
        variant_data = {
            "title": "Coffee",
            "options": [],
            "location_price": {
                sample_location["id"]: {"retail": {"type": "decimal", "name": "Original Price", "value": "20.00"}}
            },
        }
        create_response = api_client.post(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=variant_data
        )
        variant_id = create_response.json()["id"]

        # Update location price
        update_data = {
            "location_price": {
                sample_location["id"]: {"retail": {"type": "decimal", "name": "Updated Price", "value": "23.50"}}
            }
        }
        response = api_client.patch(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}/{variant_id}", json=update_data
        )

        assert response.status_code == 200
        data = response.json()
        assert data["location_price"][sample_location["id"]]["retail"]["value"] == "23.50"

    def test_create_variant_with_both_price_and_location_price(
        self, api_client, sample_store, sample_product, sample_location
    ):
        """Test creating a variant with both base price and location-specific pricing."""
        variant_data = {
            "title": "Coffee Hybrid Pricing",
            "options": [],
            "price": {"retail": {"type": "decimal", "name": "Base Retail", "value": "19.99"}},
            "location_price": {
                sample_location["id"]: {"retail": {"type": "decimal", "name": "Downtown Price", "value": "22.99"}}
            },
        }

        response = api_client.post(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=variant_data)

        assert response.status_code == 200
        data = response.json()
        assert data["price"]["retail"]["value"] == "19.99"
        assert data["location_price"][sample_location["id"]]["retail"]["value"] == "22.99"


class TestVariantRegionPrice:
    """Tests for region_price functionality in variants."""

    def test_create_variant_with_region_price(self, api_client, sample_store, sample_product):
        """Test creating a variant with region-specific pricing."""
        variant_data = {
            "title": "Coffee with Region Price",
            "options": [],
            "region_price": {
                "US": {"retail": {"type": "decimal", "name": "US Retail Price", "value": "24.99"}},
            },
        }

        response = api_client.post(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=variant_data)

        assert response.status_code == 200
        data = response.json()
        assert "region_price" in data
        assert "US" in data["region_price"]
        assert data["region_price"]["US"]["retail"]["value"] == "24.99"

    def test_create_variant_with_multiple_region_prices(self, api_client, sample_store, sample_product):
        """Test creating a variant with prices for multiple regions."""
        variant_data = {
            "title": "Coffee Multi-Region",
            "options": [],
            "region_price": {
                "US": {
                    "retail": {"type": "decimal", "name": "US Price", "value": "20.00"},
                    "wholesale": {"type": "decimal", "name": "US Wholesale", "value": "16.00"},
                },
                "CA": {
                    "retail": {"type": "decimal", "name": "Canada Price", "value": "26.00"},
                    "wholesale": {"type": "decimal", "name": "Canada Wholesale", "value": "21.00"},
                },
                "GB": {
                    "retail": {"type": "decimal", "name": "UK Price", "value": "18.50"},
                },
            },
        }

        response = api_client.post(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=variant_data)

        assert response.status_code == 200
        data = response.json()
        assert len(data["region_price"]) == 3
        assert "US" in data["region_price"]
        assert "CA" in data["region_price"]
        assert "GB" in data["region_price"]
        assert data["region_price"]["US"]["retail"]["value"] == "20.00"
        assert data["region_price"]["CA"]["retail"]["value"] == "26.00"
        assert data["region_price"]["GB"]["retail"]["value"] == "18.50"

    def test_create_variant_with_region_range_prices(self, api_client, sample_store, sample_product):
        """Test creating a variant with region-specific range prices."""
        variant_data = {
            "title": "Coffee Region Range",
            "options": [],
            "region_price": {
                "DE": {
                    "subscription": {
                        "type": "decimal_range",
                        "name": "Germany Subscription Range",
                        "min_value": "15.00",
                        "max_value": "20.00",
                    }
                }
            },
        }

        response = api_client.post(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=variant_data)

        assert response.status_code == 200
        data = response.json()
        assert data["region_price"]["DE"]["subscription"]["type"] == "decimal_range"
        assert data["region_price"]["DE"]["subscription"]["min_value"] == "15.00"
        assert data["region_price"]["DE"]["subscription"]["max_value"] == "20.00"

    def test_create_variant_with_region_quantity_prices(self, api_client, sample_store, sample_product):
        """Test creating a variant with region-specific quantity-based pricing."""
        variant_data = {
            "title": "Coffee Region Bulk",
            "options": [],
            "region_price": {
                "JP": {
                    "bulk_tier1": {
                        "type": "decimal_quantity",
                        "name": "Japan Bulk Tier 1",
                        "min_quantity": 10,
                        "value": "16.00",
                    },
                    "bulk_tier2": {
                        "type": "decimal_quantity",
                        "name": "Japan Bulk Tier 2",
                        "min_quantity": 25,
                        "value": "14.00",
                    },
                }
            },
        }

        response = api_client.post(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=variant_data)

        assert response.status_code == 200
        data = response.json()
        japan_prices = data["region_price"]["JP"]
        assert japan_prices["bulk_tier1"]["min_quantity"] == 10
        assert japan_prices["bulk_tier2"]["value"] == "14.00"

    def test_update_variant_add_region_price(self, api_client, sample_store, sample_product):
        """Test adding region price to a variant."""
        # Create variant without region price
        variant_data = {"title": "Coffee", "options": []}
        create_response = api_client.post(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=variant_data
        )
        variant_id = create_response.json()["id"]

        # Add region price
        update_data = {
            "region_price": {"AU": {"retail": {"type": "decimal", "name": "Australia Price", "value": "28.00"}}}
        }
        response = api_client.patch(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}/{variant_id}", json=update_data
        )

        assert response.status_code == 200
        data = response.json()
        assert "AU" in data["region_price"]
        assert data["region_price"]["AU"]["retail"]["value"] == "28.00"

    def test_update_variant_modify_region_price(self, api_client, sample_store, sample_product):
        """Test modifying existing region price."""
        # Create variant with region price
        variant_data = {
            "title": "Coffee",
            "options": [],
            "region_price": {"FR": {"retail": {"type": "decimal", "name": "France Price", "value": "22.00"}}},
        }
        create_response = api_client.post(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=variant_data
        )
        variant_id = create_response.json()["id"]

        # Update region price
        update_data = {
            "region_price": {"FR": {"retail": {"type": "decimal", "name": "France Updated", "value": "24.50"}}}
        }
        response = api_client.patch(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}/{variant_id}", json=update_data
        )

        assert response.status_code == 200
        data = response.json()
        assert data["region_price"]["FR"]["retail"]["value"] == "24.50"

    def test_create_variant_with_invalid_region_code(self, api_client, sample_store, sample_product):
        """Test creating a variant with invalid region/country code."""
        variant_data = {
            "title": "Coffee",
            "options": [],
            "region_price": {"INVALID": {"retail": {"type": "decimal", "name": "Invalid Region", "value": "20.00"}}},
        }

        response = api_client.post(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=variant_data)

        assert response.status_code == 422

    def test_create_variant_with_all_price_types(self, api_client, sample_store, sample_product, sample_location):
        """Test creating a variant with base price, location price, and region price."""
        variant_data = {
            "title": "Coffee All Prices",
            "options": [],
            "price": {"retail": {"type": "decimal", "name": "Base Price", "value": "19.99"}},
            "location_price": {
                sample_location["id"]: {"retail": {"type": "decimal", "name": "Downtown Price", "value": "22.99"}}
            },
            "region_price": {"US": {"retail": {"type": "decimal", "name": "US Price", "value": "24.99"}}},
        }

        response = api_client.post(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=variant_data)

        assert response.status_code == 200
        data = response.json()
        assert data["price"]["retail"]["value"] == "19.99"
        assert data["location_price"][sample_location["id"]]["retail"]["value"] == "22.99"
        assert data["region_price"]["US"]["retail"]["value"] == "24.99"

    def test_list_variants_with_location_and_region_prices(
        self, api_client, sample_store, sample_product, sample_location
    ):
        """Test listing variants correctly returns location and region price information."""
        variant_data = {
            "title": "Coffee Complex",
            "options": [],
            "price": {"retail": {"type": "decimal", "name": "Base", "value": "20.00"}},
            "location_price": {
                sample_location["id"]: {"retail": {"type": "decimal", "name": "Location", "value": "23.00"}}
            },
            "region_price": {"CA": {"retail": {"type": "decimal", "name": "Canada", "value": "26.00"}}},
        }

        api_client.post(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=variant_data)

        # List variants
        response = api_client.get(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}")

        assert response.status_code == 200
        variants = response.json()["items"]
        assert len(variants) >= 1

        # Find our variant
        variant = next((v for v in variants if v["title"] == "Coffee Complex"), None)
        assert variant is not None
        assert variant["price"]["retail"]["value"] == "20.00"
        assert variant["location_price"][sample_location["id"]]["retail"]["value"] == "23.00"
        assert variant["region_price"]["CA"]["retail"]["value"] == "26.00"


class TestVariantLocationPriceValidation:
    """Tests for location_price validation - filtering invalid location IDs."""

    def test_create_variant_filters_invalid_location_ids(
        self, api_client, sample_store, sample_product, sample_location
    ):
        """Test that invalid location IDs are filtered out when creating a variant."""
        invalid_location_id = str(PydanticObjectId())
        variant_data = {
            "title": "Coffee with Mixed Locations",
            "options": [],
            "location_price": {
                sample_location["id"]: {"retail": {"type": "decimal", "name": "Valid Location", "value": "20.00"}},
                invalid_location_id: {"retail": {"type": "decimal", "name": "Invalid Location", "value": "25.00"}},
            },
        }

        response = api_client.post(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=variant_data)

        assert response.status_code == 200
        data = response.json()
        # Only valid location should be present
        assert sample_location["id"] in data["location_price"]
        assert invalid_location_id not in data["location_price"]
        assert len(data["location_price"]) == 1
        assert data["location_price"][sample_location["id"]]["retail"]["value"] == "20.00"

    def test_create_variant_all_invalid_locations_becomes_none(self, api_client, sample_store, sample_product):
        """Test that location_price becomes None when all location IDs are invalid."""
        variant_data = {
            "title": "Coffee with Invalid Locations",
            "options": [],
            "location_price": {
                str(PydanticObjectId()): {"retail": {"type": "decimal", "name": "Invalid 1", "value": "20.00"}},
                str(PydanticObjectId()): {"retail": {"type": "decimal", "name": "Invalid 2", "value": "25.00"}},
            },
        }

        response = api_client.post(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=variant_data)

        assert response.status_code == 200
        data = response.json()
        # All locations were invalid, so location_price should be None
        assert data["location_price"] is None

    def test_create_variant_deleted_location_filtered_out(
        self, api_client, sample_store, sample_product, sample_location
    ):
        """Test that deleted locations are filtered out."""
        # Create another location
        location_data = {"name": "To Be Deleted Location", "attributes": {}}
        create_response = api_client.post(f"/api/v1/locations/{sample_store['id']}", json=location_data)
        location_to_delete = create_response.json()

        # Delete the location
        api_client.delete(f"/api/v1/locations/{sample_store['id']}/{location_to_delete['id']}")

        # Try to create variant with both locations
        variant_data = {
            "title": "Coffee with Deleted Location",
            "options": [],
            "location_price": {
                sample_location["id"]: {"retail": {"type": "decimal", "name": "Valid", "value": "20.00"}},
                location_to_delete["id"]: {"retail": {"type": "decimal", "name": "Deleted", "value": "25.00"}},
            },
        }

        response = api_client.post(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=variant_data)

        assert response.status_code == 200
        data = response.json()
        # Only the non-deleted location should be present
        assert sample_location["id"] in data["location_price"]
        assert location_to_delete["id"] not in data["location_price"]
        assert len(data["location_price"]) == 1

    def test_update_variant_filters_invalid_location_ids(
        self, api_client, sample_store, sample_product, sample_location
    ):
        """Test that invalid location IDs are filtered out when updating a variant."""
        # Create variant
        variant_data = {"title": "Coffee", "options": []}
        create_response = api_client.post(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=variant_data
        )
        variant_id = create_response.json()["id"]

        # Update with mixed valid/invalid locations
        invalid_location_id = str(PydanticObjectId())
        update_data = {
            "location_price": {
                sample_location["id"]: {"retail": {"type": "decimal", "name": "Valid", "value": "22.00"}},
                invalid_location_id: {"retail": {"type": "decimal", "name": "Invalid", "value": "30.00"}},
            }
        }

        response = api_client.patch(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}/{variant_id}", json=update_data
        )

        assert response.status_code == 200
        data = response.json()
        # Only valid location should be present
        assert sample_location["id"] in data["location_price"]
        assert invalid_location_id not in data["location_price"]
        assert len(data["location_price"]) == 1

    def test_update_variant_all_invalid_locations_becomes_none(
        self, api_client, sample_store, sample_product, sample_location
    ):
        """Test that location_price becomes None when updating with all invalid location IDs."""
        # Create variant with valid location
        variant_data = {
            "title": "Coffee",
            "options": [],
            "location_price": {
                sample_location["id"]: {"retail": {"type": "decimal", "name": "Valid", "value": "20.00"}}
            },
        }
        create_response = api_client.post(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=variant_data
        )
        variant_id = create_response.json()["id"]

        # Update with all invalid locations
        update_data = {
            "location_price": {
                str(PydanticObjectId()): {"retail": {"type": "decimal", "name": "Invalid", "value": "25.00"}}
            }
        }

        response = api_client.patch(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}/{variant_id}", json=update_data
        )

        assert response.status_code == 200
        data = response.json()
        # All locations were invalid, should become None
        assert data["location_price"] is None

    def test_create_variant_location_from_different_store_filtered(
        self, api_client, sample_store, another_store, sample_product
    ):
        """Test that locations from a different store are filtered out."""
        # Create location in another store
        location_data = {"name": "Other Store Location", "attributes": {}}
        create_response = api_client.post(f"/api/v1/locations/{another_store['id']}", json=location_data)
        other_store_location = create_response.json()

        # Create location in the correct store
        location_data = {"name": "Correct Store Location", "attributes": {}}
        create_response = api_client.post(f"/api/v1/locations/{sample_store['id']}", json=location_data)
        correct_location = create_response.json()

        # Try to create variant with both locations
        variant_data = {
            "title": "Coffee Cross-Store",
            "options": [],
            "location_price": {
                correct_location["id"]: {"retail": {"type": "decimal", "name": "Correct", "value": "20.00"}},
                other_store_location["id"]: {"retail": {"type": "decimal", "name": "Wrong Store", "value": "25.00"}},
            },
        }

        response = api_client.post(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=variant_data)

        assert response.status_code == 200
        data = response.json()
        # Only location from the correct store should be present
        assert correct_location["id"] in data["location_price"]
        assert other_store_location["id"] not in data["location_price"]
        assert len(data["location_price"]) == 1


class TestVariantImages:
    """Tests for variant images field."""

    def test_create_variant_with_single_image(self, api_client, sample_store, sample_product):
        """Test creating a variant with a single image."""
        variant_data = {
            "title": "Variant with Image",
            "options": [],
            "images": [
                {
                    "url": "https://example.com/image1.jpg",
                    "alt_text": "Variant Image 1",
                    "height": 800,
                    "width": 600,
                }
            ],
        }

        response = api_client.post(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=variant_data)

        assert response.status_code == 200
        data = response.json()
        assert "images" in data
        assert data["images"] is not None
        assert len(data["images"]) == 1
        assert data["images"][0]["url"] == "https://example.com/image1.jpg"
        assert data["images"][0]["alt_text"] == "Variant Image 1"
        assert data["images"][0]["height"] == 800
        assert data["images"][0]["width"] == 600

    def test_create_variant_with_multiple_images(self, api_client, sample_store, sample_product):
        """Test creating a variant with multiple images."""
        variant_data = {
            "title": "Variant with Multiple Images",
            "options": [],
            "images": [
                {
                    "url": "https://example.com/image1.jpg",
                    "alt_text": "Front view",
                },
                {
                    "url": "https://example.com/image2.jpg",
                    "alt_text": "Side view",
                    "height": 1024,
                    "width": 768,
                },
                {
                    "url": "https://example.com/image3.jpg",
                },
            ],
        }

        response = api_client.post(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=variant_data)

        assert response.status_code == 200
        data = response.json()
        assert len(data["images"]) == 3
        assert data["images"][0]["url"] == "https://example.com/image1.jpg"
        assert data["images"][1]["height"] == 1024
        assert data["images"][2]["alt_text"] is None

    def test_create_variant_with_image_attributes(self, api_client, sample_store, sample_product):
        """Test creating a variant with images that have custom attributes."""
        variant_data = {
            "title": "Variant with Image Attributes",
            "options": [],
            "images": [
                {
                    "url": "https://example.com/product.jpg",
                    "alt_text": "Product image",
                    "attributes": {
                        "photographer": {
                            "type": "string",
                            "name": "photographer",
                            "value": "John Doe",
                        },
                        "is_featured": {
                            "type": "bool",
                            "name": "is_featured",
                            "value": True,
                        },
                    },
                }
            ],
        }

        response = api_client.post(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=variant_data)

        assert response.status_code == 200
        data = response.json()
        assert len(data["images"]) == 1
        assert "attributes" in data["images"][0]
        assert data["images"][0]["attributes"]["photographer"]["value"] == "John Doe"
        assert data["images"][0]["attributes"]["is_featured"]["value"] is True

    def test_create_variant_without_images(self, api_client, sample_store, sample_product):
        """Test that variants can be created without images (images is optional)."""
        variant_data = {
            "title": "Variant without Images",
            "options": [],
        }

        response = api_client.post(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=variant_data)

        assert response.status_code == 200
        data = response.json()
        assert data["images"] is None

    def test_create_variant_with_empty_images_list(self, api_client, sample_store, sample_product):
        """Test creating a variant with an empty images list."""
        variant_data = {
            "title": "Variant with Empty Images",
            "options": [],
            "images": [],
        }

        response = api_client.post(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=variant_data)

        assert response.status_code == 200
        data = response.json()
        assert data["images"] == []

    def test_update_variant_add_images(self, api_client, sample_store, sample_product):
        """Test adding images to an existing variant."""
        # Create variant without images
        variant_data = {
            "title": "Variant to Update",
            "options": [],
        }
        create_response = api_client.post(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=variant_data
        )
        created_variant = create_response.json()

        # Update variant with images
        update_data = {
            "images": [
                {
                    "url": "https://example.com/new-image.jpg",
                    "alt_text": "New image",
                }
            ],
        }

        response = api_client.patch(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}/{created_variant['id']}", json=update_data
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["images"]) == 1
        assert data["images"][0]["url"] == "https://example.com/new-image.jpg"

    def test_update_variant_modify_images(self, api_client, sample_store, sample_product):
        """Test modifying existing images of a variant."""
        # Create variant with images
        variant_data = {
            "title": "Variant to Update",
            "options": [],
            "images": [
                {
                    "url": "https://example.com/old-image.jpg",
                    "alt_text": "Old image",
                }
            ],
        }
        create_response = api_client.post(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=variant_data
        )
        created_variant = create_response.json()

        # Update images
        update_data = {
            "images": [
                {
                    "url": "https://example.com/new-image1.jpg",
                    "alt_text": "New image 1",
                },
                {
                    "url": "https://example.com/new-image2.jpg",
                    "alt_text": "New image 2",
                },
            ],
        }

        response = api_client.patch(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}/{created_variant['id']}", json=update_data
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["images"]) == 2
        assert data["images"][0]["url"] == "https://example.com/new-image1.jpg"
        assert data["images"][1]["url"] == "https://example.com/new-image2.jpg"

    def test_update_variant_remove_images(self, api_client, sample_store, sample_product):
        """Test removing images from a variant by setting to empty list."""
        # Create variant with images
        variant_data = {
            "title": "Variant to Update",
            "options": [],
            "images": [
                {
                    "url": "https://example.com/image.jpg",
                }
            ],
        }
        create_response = api_client.post(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=variant_data
        )
        created_variant = create_response.json()

        # Remove images
        update_data = {"images": []}

        response = api_client.patch(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}/{created_variant['id']}", json=update_data
        )

        assert response.status_code == 200
        data = response.json()
        assert data["images"] == []

    def test_get_variant_with_images(self, api_client, sample_store, sample_product):
        """Test retrieving a variant with images."""
        # Create variant with images
        variant_data = {
            "title": "Variant with Images",
            "options": [],
            "images": [
                {
                    "url": "https://example.com/image.jpg",
                    "alt_text": "Test image",
                    "height": 500,
                    "width": 500,
                }
            ],
        }
        create_response = api_client.post(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=variant_data
        )
        created_variant = create_response.json()

        # Retrieve variant
        response = api_client.get(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}/{created_variant['id']}"
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["images"]) == 1
        assert data["images"][0]["url"] == "https://example.com/image.jpg"
        assert data["images"][0]["alt_text"] == "Test image"

    def test_list_variants_with_images(self, api_client, sample_store, sample_product):
        """Test listing variants includes images."""
        # Create variant with images
        variant_data = {
            "title": "Variant 1",
            "options": [{"name": "Type", "value": "With Images"}],
            "images": [{"url": "https://example.com/image1.jpg"}],
        }
        api_client.post(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=variant_data)

        # Create variant without images
        variant_data2 = {
            "title": "Variant 2",
            "options": [{"name": "Type", "value": "Without Images"}],
        }
        api_client.post(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=variant_data2)

        # List variants
        response = api_client.get(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}")

        assert response.status_code == 200
        data = response.json()["items"]
        assert len(data) == 2

        # Find variant with images
        variant_with_images = next(v for v in data if v["title"] == "Variant 1")
        variant_without_images = next(v for v in data if v["title"] == "Variant 2")

        assert len(variant_with_images["images"]) == 1
        assert variant_without_images["images"] is None

    def test_create_variant_invalid_image_url(self, api_client, sample_store, sample_product):
        """Test that invalid image URLs are rejected."""
        variant_data = {
            "title": "Variant with Invalid URL",
            "options": [],
            "images": [
                {
                    "url": "not-a-valid-url",
                    "alt_text": "Invalid",
                }
            ],
        }

        response = api_client.post(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=variant_data)

        assert response.status_code == 422

    def test_create_variant_image_with_negative_dimensions(self, api_client, sample_store, sample_product):
        """Test that negative image dimensions are rejected."""
        variant_data = {
            "title": "Variant with Invalid Dimensions",
            "options": [],
            "images": [
                {
                    "url": "https://example.com/image.jpg",
                    "height": -100,
                    "width": 500,
                }
            ],
        }

        response = api_client.post(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=variant_data)

        assert response.status_code == 422

    def test_create_variant_image_alt_text_too_long(self, api_client, sample_store, sample_product):
        """Test that alt_text exceeding max length is rejected."""
        variant_data = {
            "title": "Variant with Long Alt Text",
            "options": [],
            "images": [
                {
                    "url": "https://example.com/image.jpg",
                    "alt_text": "a" * 513,  # Max is 512
                }
            ],
        }

        response = api_client.post(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=variant_data)

        assert response.status_code == 422


class TestVariantAttributeTypesConversion:
    """Tests for MongoDB conversion of all attribute types (decimal, etc.)."""

    def test_create_and_retrieve_variant_with_all_attribute_types(
        self, api_client, comprehensive_variant_data, sample_store, sample_product
    ):
        """Test that all attribute types survive round-trip to MongoDB correctly.

        This test specifically checks that MongoDB types like Decimal128 are
        properly converted back to Python types during deserialization.
        """
        # Create variant with comprehensive attributes
        create_response = api_client.post(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=comprehensive_variant_data
        )

        assert create_response.status_code == 200
        created_variant = create_response.json()
        variant_id = created_variant["id"]

        # Verify attributes on creation response
        assert "attributes" in created_variant
        assert "decimal_attr" in created_variant["attributes"]
        assert created_variant["attributes"]["decimal_attr"]["value"] == "19.99"

        # Get variant by ID - this retrieves from MongoDB
        get_response = api_client.get(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}/{variant_id}")

        assert get_response.status_code == 200, f"Failed to get variant: {get_response.json()}"
        retrieved_variant = get_response.json()

        # Verify all basic attribute types
        attrs = retrieved_variant["attributes"]
        assert attrs["string_attr"]["type"] == "string"
        assert attrs["string_attr"]["value"] == "test string"

        assert attrs["text_attr"]["type"] == "text"
        assert "longer text" in attrs["text_attr"]["value"]

        assert attrs["integer_attr"]["type"] == "integer"
        assert attrs["integer_attr"]["value"] == 42

        assert attrs["bool_attr"]["type"] == "bool"
        assert attrs["bool_attr"]["value"] is True

        assert attrs["float_attr"]["type"] == "float"
        assert abs(attrs["float_attr"]["value"] - 3.14159) < 0.001

        # Critical test: decimal attribute from MongoDB
        assert attrs["decimal_attr"]["type"] == "decimal"
        assert attrs["decimal_attr"]["value"] == "19.99"

        assert attrs["date_attr"]["type"] == "date"
        assert "2026-03-22" in attrs["date_attr"]["value"]

        assert attrs["datetime_attr"]["type"] == "datetime"
        assert "2026-03-22" in attrs["datetime_attr"]["value"]

        assert attrs["uuid_attr"]["type"] == "uuid"
        assert attrs["url_attr"]["type"] == "url"
        assert "example.com" in attrs["url_attr"]["value"]

        # Verify range types
        assert attrs["float_range_attr"]["type"] == "float_range"
        assert attrs["float_range_attr"]["min_value"] == 0.0
        assert attrs["float_range_attr"]["max_value"] == 100.0

        assert attrs["integer_range_attr"]["type"] == "integer_range"
        assert attrs["integer_range_attr"]["min_value"] == 10
        assert attrs["integer_range_attr"]["max_value"] == 50

        # Critical test: decimal range from MongoDB
        assert attrs["decimal_range_attr"]["type"] == "decimal_range"
        assert attrs["decimal_range_attr"]["min_value"] == "10.00"
        assert attrs["decimal_range_attr"]["max_value"] == "99.99"

        # Verify list types
        assert attrs["list_strings_attr"]["type"] == "list_of_strings"
        assert attrs["list_strings_attr"]["values"] == ["tag1", "tag2", "tag3"]

        assert attrs["list_integers_attr"]["type"] == "list_of_integers"
        assert attrs["list_integers_attr"]["values"] == [1, 2, 3, 4, 5]

        assert attrs["list_floats_attr"]["type"] == "list_of_floats"
        assert len(attrs["list_floats_attr"]["values"]) == 3

        # Critical test: list of decimals from MongoDB
        assert attrs["list_decimals_attr"]["type"] == "list_of_decimals"
        assert len(attrs["list_decimals_attr"]["values"]) == 3
        assert "10.99" in attrs["list_decimals_attr"]["values"]

        # Verify map types
        assert attrs["map_strings_attr"]["type"] == "map_of_strings"
        assert attrs["map_strings_attr"]["values"]["key1"] == "value1"

        assert attrs["map_integers_attr"]["type"] == "map_of_integers"
        assert attrs["map_integers_attr"]["values"]["key1"] == 10

        assert attrs["map_floats_attr"]["type"] == "map_of_floats"
        assert attrs["map_floats_attr"]["values"]["key1"] == 1.5

        # Critical test: map of decimals from MongoDB
        assert attrs["map_decimals_attr"]["type"] == "map_of_decimals"
        assert attrs["map_decimals_attr"]["values"]["price1"] == "15.99"
        assert attrs["map_decimals_attr"]["values"]["price2"] == "25.99"

    def test_list_variants_with_all_attribute_types(
        self, api_client, comprehensive_variant_data, sample_store, sample_product
    ):
        """Test that listing variants correctly handles all attribute types from MongoDB."""
        # Create variant
        create_response = api_client.post(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=comprehensive_variant_data
        )
        assert create_response.status_code == 200

        # List variants - this retrieves from MongoDB
        list_response = api_client.get(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}")

        assert list_response.status_code == 200, f"Failed to list variants: {list_response.json()}"
        variants = list_response.json()["items"]
        assert len(variants) >= 1

        # Find our variant
        variant = next((v for v in variants if v["title"] == "Comprehensive Test Variant"), None)
        assert variant is not None, "Comprehensive variant not found in list"

        # Verify critical decimal types are deserialized correctly
        attrs = variant["attributes"]
        assert attrs["decimal_attr"]["value"] == "19.99"
        assert attrs["decimal_range_attr"]["min_value"] == "10.00"
        assert "10.99" in attrs["list_decimals_attr"]["values"]
        assert attrs["map_decimals_attr"]["values"]["price1"] == "15.99"

    def test_create_and_retrieve_variant_with_all_price_types(
        self, api_client, comprehensive_variant_data, sample_store, sample_product
    ):
        """Test that all price types survive round-trip to MongoDB correctly."""
        # Create variant with all price types
        create_response = api_client.post(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=comprehensive_variant_data
        )

        assert create_response.status_code == 200
        created_variant = create_response.json()
        variant_id = created_variant["id"]

        # Get variant by ID - this retrieves from MongoDB
        get_response = api_client.get(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}/{variant_id}")

        assert get_response.status_code == 200, f"Failed to get variant: {get_response.json()}"
        retrieved_variant = get_response.json()

        # Verify all price types
        prices = retrieved_variant["price"]

        # DecimalPrice
        assert prices["retail"]["type"] == "decimal"
        assert prices["retail"]["value"] == "29.99"

        # DecimalRangePrice
        assert prices["subscription_range"]["type"] == "decimal_range"
        assert prices["subscription_range"]["min_value"] == "24.99"
        assert prices["subscription_range"]["max_value"] == "27.99"

        # DecimalQuantityPrice
        assert prices["bulk_discount"]["type"] == "decimal_quantity"
        assert prices["bulk_discount"]["min_quantity"] == 10
        assert prices["bulk_discount"]["value"] == "22.99"

    def test_update_variant_with_decimal_attributes(self, api_client, sample_store, sample_product):
        """Test updating variant with decimal attributes works correctly."""
        # Create simple variant
        variant_data = {"title": "Simple Variant", "options": []}
        create_response = api_client.post(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=variant_data
        )
        variant_id = create_response.json()["id"]

        # Update with decimal attributes
        update_data = {
            "attributes": {
                "weight": {"type": "decimal", "name": "weight", "value": "250.50"},
                "price_range": {
                    "type": "decimal_range",
                    "name": "price_range",
                    "min_value": "10.00",
                    "max_value": "50.00",
                },
                "discounts": {
                    "type": "list_of_decimals",
                    "name": "discounts",
                    "values": ["5.00", "10.00", "15.00"],
                },
            }
        }

        update_response = api_client.patch(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}/{variant_id}", json=update_data
        )

        assert update_response.status_code == 200

        # Retrieve and verify
        get_response = api_client.get(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}/{variant_id}")

        assert get_response.status_code == 200, f"Failed to get updated variant: {get_response.json()}"
        retrieved_variant = get_response.json()

        attrs = retrieved_variant["attributes"]
        assert attrs["weight"]["value"] == "250.50"
        assert attrs["price_range"]["min_value"] == "10.00"
        assert attrs["price_range"]["max_value"] == "50.00"
        assert "5.00" in attrs["discounts"]["values"]
        assert "10.00" in attrs["discounts"]["values"]
        assert "15.00" in attrs["discounts"]["values"]

    def test_variant_with_zero_decimal_value(self, api_client, sample_store, sample_product):
        """Test that decimal attributes with zero value work correctly (common edge case)."""
        variant_data = {
            "title": "Zero Weight Variant",
            "options": [],
            "attributes": {
                "weight_gr": {"type": "decimal", "name": "weight_gr", "value": "0"},
                "discount": {"type": "decimal", "name": "discount", "value": "0.00"},
            },
            "price": {
                "free": {"type": "decimal", "name": "Free Price", "value": "0.00"},
            },
        }

        create_response = api_client.post(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=variant_data
        )

        assert create_response.status_code == 200
        variant_id = create_response.json()["id"]

        # Retrieve from MongoDB
        get_response = api_client.get(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}/{variant_id}")

        assert get_response.status_code == 200, f"Failed to get variant with zero decimals: {get_response.json()}"
        retrieved_variant = get_response.json()

        # Verify zero decimal values are handled correctly
        assert retrieved_variant["attributes"]["weight_gr"]["value"] == "0"
        assert retrieved_variant["attributes"]["discount"]["value"] == "0.00"
        assert retrieved_variant["price"]["free"]["value"] == "0.00"


class TestListVariantsPagination:
    """Pagination tests for GET /api/v1/variants/{store_id}/{product_id}."""

    def test_first_page_no_cursor(self, api_client, sample_store, sample_product):
        """No cursor: first page, has_next when more items exist."""
        for i in range(3):
            api_client.post(
                f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}",
                json={"title": f"Variant {i}", "options": [{"name": "size", "value": str(i)}]},
            )

        response = api_client.get(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", params={"limit": 2})

        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 2
        assert data["has_next"] is True
        assert data["has_prev"] is False

    def test_forward_pagination(self, api_client, sample_store, sample_product):
        """after=end_cursor fetches the next page."""
        for i in range(3):
            api_client.post(
                f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}",
                json={"title": f"VarFwd {i}", "options": [{"name": "size", "value": str(i)}]},
            )

        page1 = api_client.get(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", params={"limit": 2}
        ).json()
        page2_resp = api_client.get(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}",
            params={"after": page1["end_cursor"], "limit": 2},
        )

        assert page2_resp.status_code == 200
        page2 = page2_resp.json()
        assert len(page2["items"]) == 1
        assert page2["has_next"] is False
        assert page2["has_prev"] is True

    def test_middle_page_has_next(self, api_client, sample_store, sample_product):
        """after=end_cursor on a middle page returns has_next=True and truncates to limit."""
        for i in range(5):
            api_client.post(
                f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}",
                json={"title": f"VarMid {i}", "options": [{"name": "size", "value": str(i)}]},
            )

        page1 = api_client.get(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", params={"limit": 2}
        ).json()
        page2_resp = api_client.get(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}",
            params={"after": page1["end_cursor"], "limit": 2},
        )

        assert page2_resp.status_code == 200
        page2 = page2_resp.json()
        assert len(page2["items"]) == 2
        assert page2["has_next"] is True
        assert page2["has_prev"] is True

    def test_middle_page_has_prev(self, api_client, sample_store, sample_product):
        """before=start_cursor on a middle page returns has_prev=True and truncates to limit."""
        for i in range(5):
            api_client.post(
                f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}",
                json={"title": f"VarPrev {i}", "options": [{"name": "size", "value": str(i)}]},
            )

        page1 = api_client.get(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", params={"limit": 2}
        ).json()
        page2 = api_client.get(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}",
            params={"after": page1["end_cursor"], "limit": 2},
        ).json()
        page3 = api_client.get(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}",
            params={"after": page2["end_cursor"], "limit": 2},
        ).json()

        back_resp = api_client.get(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}",
            params={"before": page3["start_cursor"], "limit": 2},
        )

        assert back_resp.status_code == 200
        back = back_resp.json()
        assert len(back["items"]) == 2
        assert back["has_prev"] is True
        assert back["has_next"] is True

    def test_empty_result(self, api_client, sample_store, sample_product):
        """No variants: empty paginated response."""
        response = api_client.get(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}")

        assert response.status_code == 200
        data = response.json()
        assert data["items"] == []
        assert data["start_cursor"] is None
        assert data["end_cursor"] is None
        assert data["has_next"] is False
        assert data["has_prev"] is False

    def test_invalid_cursor(self, api_client, sample_store, sample_product):
        """Invalid cursor returns 400."""
        response = api_client.get(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}",
            params={"after": "not-a-valid-cursor"},
        )
        assert response.status_code == 400

    def test_limit_max_enforced(self, api_client, sample_store, sample_product):
        """Limit > max_limit returns 422."""
        response = api_client.get(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", params={"limit": 999}
        )
        assert response.status_code == 422


class TestListVariantsByAttributes:
    """Tests for GET /api/v1/variants/{store_id}/{product_id}?attrs= filtering."""

    def test_filter_by_attribute_match(
        self, api_client, sample_variant_data, another_variant_data, sample_store, sample_product
    ):
        """Filter returns only variants matching the attribute value."""
        another_variant_data["attributes"] = {"origin": {"type": "string", "name": "origin", "value": "Huila"}}
        api_client.post(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=sample_variant_data)
        api_client.post(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=another_variant_data)

        response = api_client.get(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}",
            params={"attrs": "origin:Yirgacheffe"},
        )

        assert response.status_code == 200
        items = response.json()["items"]
        assert len(items) == 1
        assert items[0]["attributes"]["origin"]["value"] == "Yirgacheffe"

    def test_filter_by_attribute_no_match(self, api_client, sample_variant_data, sample_store, sample_product):
        """Filter returns empty list when no variants match."""
        api_client.post(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=sample_variant_data)

        response = api_client.get(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}",
            params={"attrs": "origin:Unknown"},
        )

        assert response.status_code == 200
        assert response.json()["items"] == []

    def test_filter_by_integer_attribute(
        self, api_client, sample_variant_data, another_variant_data, sample_store, sample_product
    ):
        """Integer attribute values are coerced and matched correctly."""
        another_variant_data["attributes"] = {"altitude": {"type": "integer", "name": "altitude", "value": 2000}}
        api_client.post(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=sample_variant_data)
        api_client.post(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=another_variant_data)

        response = api_client.get(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}",
            params={"attrs": "altitude:1800"},
        )

        assert response.status_code == 200
        items = response.json()["items"]
        assert len(items) == 1
        assert items[0]["attributes"]["altitude"]["value"] == 1800

    def test_filter_by_same_key_multiple_values_or(
        self, api_client, sample_variant_data, another_variant_data, sample_store, sample_product
    ):
        """Same-key attrs with multiple values are ORed."""
        another_variant_data["attributes"] = {"origin": {"type": "string", "name": "origin", "value": "Huila"}}
        api_client.post(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=sample_variant_data)
        api_client.post(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=another_variant_data)

        response = api_client.get(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}",
            params=[("attrs", "origin:Yirgacheffe"), ("attrs", "origin:Huila")],
        )

        assert response.status_code == 200
        assert len(response.json()["items"]) == 2

    def test_empty_attrs_returns_all(
        self, api_client, sample_variant_data, another_variant_data, sample_store, sample_product
    ):
        """Empty attrs list applies no filter."""
        api_client.post(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=sample_variant_data)
        api_client.post(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=another_variant_data)

        response = api_client.get(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}")

        assert response.status_code == 200
        assert len(response.json()["items"]) == 2


class TestListVariantsByPrice:
    """Tests for price/location_price/region_price filtering on list variants."""

    @pytest.fixture
    def variant_with_price(self, api_client, sample_store, sample_product):
        data = {
            "title": "Priced Variant",
            "options": [{"name": "Size", "value": "250g"}],
            "price": {"USD": {"type": "decimal", "name": "USD Price", "value": "29.99"}},
        }
        return api_client.post(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=data).json()

    @pytest.fixture
    def variant_with_high_price(self, api_client, sample_store, sample_product):
        data = {
            "title": "Expensive Variant",
            "options": [{"name": "Size", "value": "1kg"}],
            "price": {"USD": {"type": "decimal", "name": "USD Price", "value": "89.99"}},
        }
        return api_client.post(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=data).json()

    def test_filter_by_price_min(
        self, api_client, sample_store, sample_product, variant_with_price, variant_with_high_price
    ):
        """'USD>=<value>' filters out variants below the minimum."""
        response = api_client.get(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}",
            params={"price": "USD>=50.00"},
        )

        assert response.status_code == 200
        items = response.json()["items"]
        assert len(items) == 1
        assert items[0]["id"] == variant_with_high_price["id"]

    def test_filter_by_price_max(
        self, api_client, sample_store, sample_product, variant_with_price, variant_with_high_price
    ):
        """'USD<=<value>' filters out variants above the maximum."""
        response = api_client.get(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}",
            params={"price": "USD<=50.00"},
        )

        assert response.status_code == 200
        items = response.json()["items"]
        assert len(items) == 1
        assert items[0]["id"] == variant_with_price["id"]

    def test_filter_by_price_range(
        self, api_client, sample_store, sample_product, variant_with_price, variant_with_high_price
    ):
        """'USD>=<min> USD<=<max>' together define an inclusive range."""
        response = api_client.get(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}",
            params={"price": "USD>=20.00 USD<=50.00"},
        )

        assert response.status_code == 200
        items = response.json()["items"]
        assert len(items) == 1
        assert items[0]["id"] == variant_with_price["id"]

    def test_price_key_without_range_returns_all(
        self, api_client, sample_store, sample_product, variant_with_price, variant_with_high_price
    ):
        """A bare key with no operator applies no filter."""
        response = api_client.get(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}",
            params={"price": "USD"},
        )

        assert response.status_code == 200
        assert len(response.json()["items"]) == 2
