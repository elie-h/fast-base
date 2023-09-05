from typing import List, Union

from pydantic import AnyHttpUrl, validator
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    PROJECT_NAME: str = "Fast Base"
    VERSION: str = "0.0.1"

    API_V1_STR: str = "/api/v1"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    INJECT_SECURITY_HEADERS: bool = True
    INJECT_CSP_HEADERS: bool = False  # Usually not required if not serving HTML
    REDIRECT_HTTPS: bool = False
    TRUSTED_HOSTS: List[str] = ["*"]
    GZIP_ENABLED: bool = True
    GZIP_MIN_SIZE: int = 500
    CORRELATION_ID_ENABLED: bool = True
    INJECT_PROCESS_TIME: bool = True
    JSON_LOGGING: bool = True
    LOG_LEVEL: str = "INFO"

    DATABASE_URL: str

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        # Environment variables are loaded from the environment first, then from the .env file
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"  # Ignore extra env variables


config = Config()  # type: ignore
