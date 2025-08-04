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
