import aiogram.fsm.state


class DepositForm(aiogram.fsm.state.StatesGroup):
    amount = aiogram.fsm.state.State()
