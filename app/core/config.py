from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Gremlin Server websocket endpoint, e.g. ws://localhost:8182/gremlin
    GREMLIN_URL: str = "ws://localhost:8182/gremlin"
    # Traversal source name configured on Gremlin Server (commonly "g")
    GREMLIN_TRAVERSAL_SOURCE: str = "g"

    # API
    APP_NAME: str = "Quotation Importer"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    LOG_LEVEL: str = "INFO"


settings = Settings()
