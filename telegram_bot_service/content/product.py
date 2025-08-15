import schemas.product


def PRODUCT_INFO(
    data: schemas.product.ProductView
):
    product_type = None
    match data.product_type:
        case "recurring":
            product_type = "Подписка"
        case "one_time":
            product_type = "Пермаментная покупка"
    return f"""
<b>{data.product_name}</b>

Тип: {product_type}
Стоимость товара: {data.product_price} рублей
Срок действия: {data.duration_days if data.duration_days else 'бессрочно'}
"""
