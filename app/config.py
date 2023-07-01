from pydantic import BaseSettings

class Config(BaseSettings):
    SERVERS_FILE: str = 'servers.json'

    DISCORD_KEY: str
    DISCORD_CHANNEL_ID: int
    DISCORD_MESSAGE_ID: int | None

    TELEGRAM_KEY: str
    TELEGRAM_CHANNEL_ID: int
    TELEGRAM_MESSAGE_ID: int | None
    TELEGRAM_ADMIN_ID: int | None

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        env_nested_delimiter = '__'

config = Config()
