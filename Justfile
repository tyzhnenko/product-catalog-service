
run:
    echo "Running the main task..."
    uv run python run_server.py

lint:
    echo "Linting the code..."
    uv run ruff check src/ tests/

test:
    echo "Running tests..."
    uv run pytest tests/

format:
    echo "Formatting the code..."
    uv run ruff format src/ tests/

pre-commit-install:
    echo "Installing pre-commit hooks..."
    uv run prek install

pre-commit-run:
    echo "Running pre-commit checks..."
    uv run prek run --all-files

fetch-openapi:
    echo "Fetching OpenAPI specification..."
    uv run python fetch_openapi.py

generate-client: fetch-openapi
    echo "Generating client code from OpenAPI specification..."
    uv run openapi-python-client generate --overwrite --path openapi.json --config openapi-python-client-config.yaml --output-path clients/python

default: run
