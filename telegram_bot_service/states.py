import aiogram.fsm.state


class DepositForm(aiogram.fsm.state.StatesGroup):
    amount = aiogram.fsm.state.State()


class DepositeReceiptForm(aiogram.fsm.state.StatesGroup):
    file = aiogram.fsm.state.State()
