from fastapi import FastAPI

from src.api_v1 import api_router
from src.core.cors import configure_cors
from src.core.docs import configure_docs
from src.core.gzip import configure_gzip
from src.core.services import configure_services
from src.core.types import FastAPIServices
from src.settings import Settings, load_settings


def configure_application(
    services: FastAPIServices,
    settings: Settings,
) -> FastAPI:
    app = FastAPI(
        lifespan=services.build_combined_lifespan(),
        separate_input_output_schemas=False,
    )

    configure_docs(app, settings)
    configure_cors(app, settings)
    configure_gzip(app, settings)

    app.include_router(api_router, prefix="/api/v1")

    return app


def get_app() -> FastAPI:
    """Return the application instance.

    This function initializes and configures the application instance.

    In case of any errors during initialization, it returns a diagnostic application instance.

    Returns:
        Application: The configured application instance.

    """
    return configure_application(*configure_services(load_settings()))


app = get_app()
