from pydantic_settings import BaseSettings, PydanticBaseSettingsSource, SettingsConfigDict, YamlConfigSettingsSource


class Info(BaseSettings):
    title: str = "Product Catalog Service"
    # TODO: Get version from installed package metadata ???
    version: str = "0.1.0"
    description: str = "Service for managing product catalog."


class App(BaseSettings):
    debug: bool = False
    cors_origins: list[str] = []


class Auth(BaseSettings):
    rw_x_api_key: str | None = None
    ro_x_api_key: str | None = None


class Database(BaseSettings):
    driver: str = "mongodb"
    host: str = "localhost"
    port: int = 27017
    database: str = "product_catalog"
    user: str | None = None
    password: str | None = None


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="APP_",
        yaml_file="settings.yaml",
    )

    info: Info = Info()
    app: App = App()
    auth: Auth = Auth()
    db: Database = Database()

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            file_secret_settings,
            YamlConfigSettingsSource(settings_cls),
        )


def load_settings() -> Settings:
    return Settings()
