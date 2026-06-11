import json

from src.main import app


def main():
    openapi_schema = app.openapi()

    with open("openapi.json", "w") as f:
        json.dump(openapi_schema, f, sort_keys=False)


if __name__ == "__main__":
    main()
