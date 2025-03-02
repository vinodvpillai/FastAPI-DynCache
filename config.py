from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ENABLE_CACHE: bool = True  # Enable/Disable caching
    CACHE_BACKEND: str = "memory"  # Options: 'memory', 'redis', 'memcached'

    MEMCACHED_HOST: str = "localhost"
    MEMCACHED_PORT: int = 11211

    class Config:
        env_file = ".env"

settings = Settings()
