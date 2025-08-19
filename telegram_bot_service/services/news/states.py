import aiogram.fsm.state


class NewsStates(aiogram.fsm.state.StatesGroup):
    get_news = aiogram.fsm.state.State()
