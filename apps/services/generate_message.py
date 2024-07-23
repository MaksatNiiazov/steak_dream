# views.py


def generate_order_message(order, delivery_distance_km, delivery_fee):
    if order.is_pickup:
        delivery_info = "Самовывоз"
        delivery_fee_info = ""
    else:
        delivery_info = (
            f"Расстояние доставки: {delivery_distance_km:.2f} км\n"
            f"Стоимость доставки: {delivery_fee} сом\n"
        )
        delivery_fee_info = f"Стоимость доставки: {delivery_fee} сом\n"

    payment_info = (
        f"Способ оплаты: {order.get_payment_method_display()}\n"
        f"Сумма наличными: {order.change if order.change else 0} сом\n"
        f"Сдача: {order.change - order.total_amount if order.change else 0} сом\n"
    )

    message = (
        f"Новый заказ #{order.id}\n"
        f"Пользователь: {order.user.full_name if order.user.full_name else 'Имя не указано'}\n"
        f"Номер: {order.user.phone_number}\n"

        f"Ресторан: {order.restaurant.name}\n"

        "ЗАКАЗ:\n"
        "===============\n"
    )
    message += "-----------------\n"

    for item in order.order_items.all():
        if item.product_size:
            item_details = f"Продукт: {item.product_size.product.name} ({item.product_size.size.name})\n"
        # else:
            # item_details = f"Сет: {item.set.name}\n"

        item_details += f"Количество: {item.quantity}\n"

        if not item.is_bonus:
            item_details += f"Сумма: {item.total_amount}\n"
        else:
            item_details += f"БОНУСНЫЙ ПРОДУКТ\n"

        if item.topping.exists():
            item_details += "Топинги:\n"
            for topping in item.topping.all():
                item_details += f" - {topping.name}\n"

        if item.excluded_ingredient.exists():
            item_details += "Исключенные ингредиенты:\n"
            for ingredient in item.excluded_ingredient.all():
                item_details += f" - {ingredient.name}\n"

        message += item_details + "-----------------\n"
    message += "===============\n"

    user_address = order.delivery.user_address
    address = (
        f"Город: {user_address.city}\n"
        f"Адрес: {user_address.street} {user_address.house_number}\n"
        f"Квартира: {user_address.apartment_number}\n"
        f"Подъезд: {user_address.entrance}\n"
        f"Этаж: {user_address.floor}\n"
        f"Домофон: {user_address.intercom}\n"
        f"Комментарии: {user_address.comment}\n"
    )

    message += (
        f"Адрес доставки:\n{address if not order.is_pickup else 'Самовывоз'}\n"
        f"Статус: {order.get_order_status_display()}\n \n"
        f"{delivery_info}\n"
        f"{payment_info}\n"
        f"Общая сумма: {order.total_amount}\n"
    )

    return message
