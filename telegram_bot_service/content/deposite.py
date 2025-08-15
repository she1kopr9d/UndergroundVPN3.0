import schemas.deposite


def DEPOSITE_INFO(
    data: schemas.deposite.DepositeCreateANSW,
) -> str:
    return f"""
<b>Для вас созданна заявка на пополнение номер {data.payment_id}</b>

У вас есть 15 минут на совершение оплаты!

<b>Инструкция</b>
Метод оплаты: {data.method}
Стоимость: {data.amount}
Валюта: {data.currency}

Реквизиты: {data.requisite}

После совершения оплаты нажмите на кнопку - оплатил
"""


def WITHDRAWAL_INFO(
    data: schemas.deposite.WithdrawalInfo,
):
    withdrawal_type = None
    match data.status:
        case "first":
            withdrawal_type = "Покупка"
        case "add":
            withdrawal_type = "Продление"
    return f"""
<b>Списание</b>

<b>Сумма:</b> {data.amount}
<b>Тип:</b> {withdrawal_type}

<b>Остаток на счете:</b> {data.now_balance}
"""


def ERROR_WITHDRAWAL_INFO(
    data: schemas.deposite.WithdrawalInfo,
):
    return f"""
<b>ОШИБКА, у вас не хватает деняг</b>

<b>Сумма:</b> {data.amount}
<b>Баланс:</b> {data.now_balance}
"""
