
run:
    echo "Running the main task..."
    uv run python run_server.py

lint:
    echo "Linting the code..."
    uv run ruff check src/ tests/


default: run
