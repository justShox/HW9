from telebot import types


# Кнопка для отправки номера
def num_bt():
    # Создание пространства
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Создание кнопки
    number = types.KeyboardButton('Поделиться контактом📲', request_contact=True)
    # Добавление кнопки
    kb.add(number)
    return kb


# Кнопка для отправки локации
def loc_bt():
    # Создание пространства
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Создание кнопки
    location = types.KeyboardButton('Поделиться локацией📍', request_location=True)
    # Добавление кнопки
    kb.add(location)
    return kb


# Кнопки выбора товара
def main_menu_buttons(prods_from_db):
    # Создание товара
    kb = types.InlineKeyboardMarkup(row_width=2)
    # Создание самих кнопок
    cart = types.InlineKeyboardButton(text='Корзина', callback_data='cart')
    all_products = [types.InlineKeyboardButton(text=f'{i[1]}', callback_data=f'{i[0]}') for i in prods_from_db
                    if i[2] > 0]
    # Добавление кнопок в пространство
    kb.add(*all_products)
    kb.add(cart)
    return kb


# Кнопки выбора товара
def choose_pr_count(amount=1, plus_or_minus=''):
    # Создаем пространство
    kb = types.InlineKeyboardMarkup(row_width=3)
    # Создаем сами кнопки
    back = types.InlineKeyboardButton(text='Назад', callback_data='back')
    to_cart = types.InlineKeyboardButton(text='Добавить в Корзину', callback_data='to_cart')
    plus = types.InlineKeyboardButton(text='+', callback_data='increment')
    minus = types.InlineKeyboardButton(text='-', callback_data='decrement')
    count = types.InlineKeyboardButton(text=str(amount), callback_data=str(amount))
    # Алгоритм добавления и удаления кол-ва товара
    if plus_or_minus == 'increment':
        new_amount = int(amount) + 1
        count = types.InlineKeyboardButton(text=str(new_amount), callback_data=str(new_amount))
    elif plus_or_minus == 'decrement':
        if amount > 1:
            new_amount = int(amount) - 1
            count = types.InlineKeyboardButton(text=str(new_amount), callback_data=str(new_amount))
    # Добавляем кнопки в пространство
    kb.add(minus, count, plus)
    kb.row(back, to_cart)
    return kb


## Кнопки для админки ##
# Меню админки
def admin_menu():
    # Создаем пространство
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Создаем кнопки
    but1 = types.KeyboardButton('Добавить продукт')
    but2 = types.KeyboardButton('Удалить продукт')
    but3 = types.KeyboardButton('Изменить продукт')
    but4 = types.KeyboardButton('Перейти в меню')
    # Добавление в пространство
    kb.add(but1, but2, but3)
    kb.row(but4)
    return kb


# Кнопки подтверждения
def confirm():
    # Создаем пространство
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Создаем кнопки
    but1 = types.KeyboardButton('Да')
    but2 = types.KeyboardButton('Нет')
    # Добавление в пространство
    kb.add(but1, but2)
    return kb


# Кнопки для корзины
def cart_buttons():
    # Создаем пространство
    kb = types.InlineKeyboardMarkup(row_width=2)
    # Создаем кнопки
    order = types.InlineKeyboardButton(text='Оформить заказ', callback_data='order')
    clear = types.InlineKeyboardButton(text='Очистить корзину', callback_data='clear')
    back = types.InlineKeyboardButton(text='Назад', callback_data='back')
    # Добавляем кнопки
    kb.add(order, clear)
    kb.row(back)
    return kb
