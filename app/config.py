from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Database connection string
    # Expected format for asyncpg: postgresql+asyncpg://user:password@host:port/dbname
    DATABASE_URL: str

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_ignore_empty=True, 
        extra="ignore"
    )

# Instantiate the settings object to be used throughout the app
settings = Settings()
