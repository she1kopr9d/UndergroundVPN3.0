import pydantic

# class BaseTelegram(pydantic.BaseModel):
#     telegram_bot: str

#     @pydantic.field_validator("telegram_bot")
#     def check_telegram_bot(cls, v):
#         if v != config.settings.TELEGRAM_BOT:
#             raise ValueError("Is not me")
#         return v


class BasePage(pydantic.BaseModel):
    max_page: int
    now_page: int


class DefaultTelegramANSW(pydantic.BaseModel):
    user_id: int
    message_id: int
