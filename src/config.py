from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent

private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"

class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: str
    POSTGRES_HOST: str

    DB_URL: str

    private_key: str = private_key_path.read_text()
    public_key: str = public_key_path.read_text()
    algorithm: str = "RS256"

    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30

    model_config = SettingsConfigDict(env_file='.env', extra="ignore")

settings = Settings()
