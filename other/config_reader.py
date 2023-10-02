from aiogram import Bot
from fast_bitrix24 import BitrixAsync
from pydantic.v1 import BaseSettings, SecretStr


class Settings(BaseSettings):
    bot_token: SecretStr

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


class WebHookBitrix(BaseSettings):
    bitrix_webhook: SecretStr

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


config = Settings()
webhook_bitrix = WebHookBitrix()
bot = Bot(token=config.bot_token.get_secret_value())
bitrix = BitrixAsync("https://belkub24.bitrix24.ru/rest/1/m9ki5eppnymu5nmy/")
