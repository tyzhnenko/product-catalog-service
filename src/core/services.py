from src.core.types import FastAPIServices
from src.db import use_beanie
from src.settings import Settings


def configure_services(settings: Settings) -> tuple[FastAPIServices, Settings]:
    services = FastAPIServices()

    use_beanie(services, settings)

    return services, settings
