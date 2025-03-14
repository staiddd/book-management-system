from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


def read_key_file(filename: str) -> str:
    """Reads the contents of the key file, checking two possible directories."""
    base_dirs = [Path(__file__).parent, Path(__file__).parent.parent]

    for base_dir in base_dirs:
        key_path = base_dir / "certs" / filename
        if key_path.exists():
            return key_path.read_text()

    raise FileNotFoundError(f"Key file '{filename}' not found in expected directories.")


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: str
    POSTGRES_HOST: str

    DB_URL: str

    private_key: str = read_key_file("jwt-private.pem")
    public_key: str = read_key_file("jwt-public.pem")
    algorithm: str = "RS256"

    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()