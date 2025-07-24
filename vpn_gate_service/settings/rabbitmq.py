import pydantic_settings


class Settings(pydantic_settings.BaseSettings):
    BROKER_HOST: str
    BROKER_PORT: int
    RABBITMQ_DEFAULT_USER: str
    RABBITMQ_DEFAULT_PASS: str

    @property
    def rabbitmq_url(self):
        return (
            f"amqp://{self.RABBITMQ_DEFAULT_USER}:"
            f"{self.RABBITMQ_DEFAULT_PASS}@"
            f"{self.BROKER_HOST}:{self.BROKER_PORT}"
        )
