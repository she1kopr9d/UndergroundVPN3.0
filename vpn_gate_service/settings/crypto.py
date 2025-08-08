import aiocryptopay
import pydantic_settings


class Settings(pydantic_settings.BaseSettings):
    CRYPTO_API_TOKEN_MAIN: str
    CRYPTO_API_TOKEN_TEST: str
    CRYPTO_DEBUG: bool

    @property
    def get_net(self):
        return (
            aiocryptopay.Networks.TEST_NET
            if self.CRYPTO_DEBUG
            else aiocryptopay.Networks.MAIN_NET
        )

    @property
    def get_token(self):
        return (
            self.CRYPTO_API_TOKEN_TEST
            if self.CRYPTO_DEBUG
            else self.CRYPTO_API_TOKEN_MAIN
        )

    model_config = pydantic_settings.SettingsConfigDict(env_file=".env")
