import telebot, buttons as bt, database as db
from geopy import Nominatim
from telebot.types import ReplyKeyboardRemove

bot = telebot.TeleBot('6592791880:AAGhH3HHcOYbtqZ5lZsWkX3YigMTF9MGnTQ')
# Использование карт
geolocator = Nominatim(
    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

# Временные файлы
users = {}


# Обработка команды старт
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    check = db.checker(user_id)
    if check:
        products = db.get_pr_but()
        bot.send_message(user_id, f'Добро Пожаловать {message.from_user.first_name}!',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.send_message(user_id, f'Выберите пункт меню:',
                         reply_markup=bt.main_menu_buttons(products))
    else:
        bot.send_message(user_id, 'Здравствуйте! Давайте начнем регистрацию☺️!'
                                  '\nВведите свое имя:')
        # Переход на этап получения имени
        bot.register_next_step_handler(message, get_name)


# Этап получения имени
def get_name(message):
    user_id = message.from_user.id
    name = message.text
    bot.send_message(user_id, 'Отлично! Пожалуйста поделитесь контактом☎️:', reply_markup=bt.num_bt())
    # Этап получения номера
    bot.register_next_step_handler(message, get_number, name)


# Этап получения номера
def get_number(message, name):
    user_id = message.from_user.id
    # Если юзер отправил номер по кнопке
    if message.contact:
        number = message.contact.phone_number
        bot.send_message(user_id, 'Принято! И последнее поделитесь локацией🗺:', reply_markup=bt.loc_bt())
        # Этап получения локации
        bot.register_next_step_handler(message, get_location, name, number)
    # Если юзер отправил не по кнопке
    else:
        bot.send_message(user_id, 'Пожалуйста поделитесь контактом☎️!', reply_markup=bt.num_bt())
        # Этап получения номера
        bot.register_next_step_handler(message, get_number, name)


# Этап получения локации
def get_location(message, name, number):
    user_id = message.from_user.id
    # Если юзер отправил локацию по кнопке
    if message.location:
        location = str(geolocator.reverse(f'{message.location.latitude}, '
                                          f'{message.location.longitude}'))
        db.registration(user_id, name, number, location)
        products = db.get_pr_but()
        bot.send_message(user_id, 'Все готово! Регистрация прошла успешно✅',
                         reply_markup=bt.main_menu_buttons(products))
    # Если юзер отправил не по кнопке
    else:
        bot.send_message(user_id, 'Пожалуйста поделитесь локацией🗺!', reply_markup=bt.loc_bt())
        # Этап получения локации
        bot.register_next_step_handler(message, get_location, name, number)


# Функция выбора количества
@bot.callback_query_handler(lambda call: call.data in ['back', 'to_cart', 'increment', 'decrement'])
def choose_count(call):
    chat_id = call.message.chat.id
    if call.data == 'increment':
        count = users[chat_id]['pr_amount']
        users[chat_id]['pr_amount'] += 1
        bot.edit_message_reply_markup(chat_id=chat_id, message_id=call.message.message_id,
                                      reply_markup=bt.choose_pr_count(count, 'increment'))
    elif call.data == 'decrement':
        count = users[chat_id]['pr_amount']
        users[chat_id]['pr_amount'] -= 1
        bot.edit_message_reply_markup(chat_id=chat_id, message_id=call.message.message_id,
                                      reply_markup=bt.choose_pr_count(count, 'decrement'))
    elif call.data == 'back':
        products = db.get_pr_but()
        bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
        bot.send_message(chat_id, 'Возвращаю вас обратно в меню',
                         reply_markup=bt.main_menu_buttons(products))
    elif call.data == 'to_cart':
        products = db.get_pr(users[chat_id]['pr_name'])
        prod_amount = users[chat_id]['pr_amount']
        user_total = products[4] * prod_amount
        db.add_pr_to_cart(chat_id, products[0], prod_amount, user_total)
        bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
        bot.send_message(chat_id, 'Товар успешно добавлен в корзину, ваши действия ?',
                         reply_markup=bt.cart_buttons())


# Корзина
@bot.callback_query_handler(lambda call: call.data in ['cart', 'back', 'order', 'clear'])
def cart_handle(call):
    chat_id = call.message.chat.id
    products = db.get_pr_but()

    if call.data == 'clear':
        db.clear_cart(chat_id)
        bot.edit_message_text('Ваша корзина пуста, выберите новый товар', chat_id=chat_id,
                              message_id=call.message.message_id,
                              reply_markup=bt.main_menu_buttons(products))
    elif call.data == 'order':
        group_id = -4100883166
        cart = db.make_order(chat_id)
        text = f'Новый заказ! \n\n' \
               f'id пользователя: {cart[0][0]}\n' \
               f'Товара: {cart[0][1]}\n' \
               f'Количество: {cart[0][2]}\n' \
               f'Итого: {cart[0][3]}\n\n' \
               f'Адрес: {cart[1]}'
        bot.send_message(group_id, text)
        bot.edit_message_text('Спасибо за оформление заказа, с вами скоро свяжутся',
                              chat_id=chat_id, message_id=call.message.message_id,
                              reply_markup=bt.main_menu_buttons(products))
    elif call.data == 'back':
        bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
        bot.send_message(chat_id, 'Возвращаю вас обратно в меню',
                         reply_markup=bt.main_menu_buttons(products))
    elif call.data == 'cart':
        cart = db.show_cart(chat_id)
        text = f'Ваша корзина: \n\n' \
               f'Товар: {cart[0]}\n' \
               f'Количество: {cart[1]}\n' \
               f'Итого: {cart[2]}\n\n' \
               f'Что хотите сделать ?'
        bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
        bot.send_message(chat_id, text, reply_markup=bt.cart_buttons())


# Вывод информации о продукте
@bot.callback_query_handler(lambda call: int(call.data) in db.get_pr_but()[0])
def get_user_product(call):
    chat_id = call.message.chat.id
    prod = db.get_pr(int(call.data))
    users[chat_id] = {'pr_name': call.data, 'pr_amount': 1}
    bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
    text = f'Название товара: {prod[0]}' \
           f'\nОписание товара: {prod[1]}' \
           f'\nКоличество на складе: {prod[2]}' \
           f'\nЦены: ${prod[4]}'
    bot.send_photo(chat_id, prod[3], caption=text, reply_markup=bt.choose_pr_count())


# Обработка команды admin
@bot.message_handler(commands=['admin'])
def act(message):
    admin_id = 692440883
    if message.from_user.id == admin_id:
        bot.send_message(admin_id, 'Выберите действие:', reply_markup=bt.admin_menu())
        # Переход на этап выбора
        bot.register_next_step_handler(message, admin_choose)
    else:
        bot.send_message(message.from_user.id, 'Вы не админ!')


# Выбор действия админом
def admin_choose(message):
    admin_id = 692440883
    if message.text == 'Добавить продукт':
        bot.send_message(admin_id, 'Напишите название продукта!',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        # Переход на этап получения названия
        bot.register_next_step_handler(message, get_pr_name)
    elif message.text == 'Удалить продукт':
        check = db.check_pr()
        if check:
            bot.send_message(admin_id, 'Напишите id продукта!',
                             reply_markup=telebot.types.ReplyKeyboardRemove())
            # Переход на этап получения названия
            bot.register_next_step_handler(message, get_pr_id)
        else:
            bot.send_message(admin_id, 'Продуктов в базе пока нет!')
            # Возврат на этап выбора
            bot.register_next_step_handler(message, admin_choose)
    elif message.text == 'Изменить продукт':
        check = db.check_pr()
        if check:
            bot.send_message(admin_id, 'Напишите id продукта!',
                             reply_markup=telebot.types.ReplyKeyboardRemove())
            # Переход на этап получения названия
            bot.register_next_step_handler(message, get_pr_change)
        else:
            bot.send_message(admin_id, 'Продуктов в базе пока нет!')
            # Возврат на этап выбора
            bot.register_next_step_handler(message, admin_choose)
    elif message.text == 'Перейти в меню':
        products = db.get_pr_but()
        bot.send_message(admin_id, 'Ок!',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.send_message(admin_id, 'Добро Пожаловать в меню!',
                         reply_markup=bt.main_menu_buttons(products))

    else:
        bot.send_message(admin_id, 'Неизвестная операция', reply_markup=bt.admin_menu())
        # Возврат на этап выбора
        bot.register_next_step_handler(message, admin_choose)


# Этап получения названия продукта
def get_pr_name(message):
    admin_id = 692440883
    if message.text:
        pr_name = message.text
        bot.send_message(admin_id, 'Отлично теперь придумайте описание!')
        # Переход на этап получения описания
        bot.register_next_step_handler(message, get_pr_des, pr_name)
    else:
        bot.send_message(admin_id, 'Отправьте название товара в виде текста')
        # Возврат на этап получения названия
        bot.register_next_step_handler(message, get_pr_name)


# Этап получения описания
def get_pr_des(message, pr_name):
    admin_id = 692440883
    if message.text:
        pr_des = message.text
        bot.send_message(admin_id, 'Теперь введите количество товара:')
        bot.register_next_step_handler(message, get_pr_count, pr_name, pr_des)
    else:
        bot.send_message(admin_id, 'Отправьте описание товара в виде текста')
        # Возврат на этап получения описание
        bot.register_next_step_handler(message, get_pr_des, pr_name)


# Этап получения количества
def get_pr_count(message, pr_name, pr_des):
    admin_id = 692440883
    try:
        pr_count = int(message.text)
        bot.send_message(admin_id, 'А сейчас перейдите на сайт https://postimages.org/, загрузите '
                                   'фото товара и отправьте прямую ссылку на него!')
        # Переход на этап получения фото
        bot.register_next_step_handler(message, get_pr_photo, pr_name, pr_des, pr_count)
    except ValueError or telebot.apihelper.ApiTelegramException:
        bot.send_message(admin_id, 'Ошибка в количестве, попробуйте еще раз!')
        # Возврат на этап получения кол-ва
        bot.register_next_step_handler(message, get_pr_count, pr_name, pr_des)


# Этап получения фото
def get_pr_photo(message, pr_name, pr_des, pr_count):
    admin_id = 692440883
    if message.text:
        pr_photo = message.text
        bot.send_message(admin_id, 'Отлично! И последнее какова цена товара?')
        # Переход на этап получения цены
        bot.register_next_step_handler(message, get_pr_price, pr_name, pr_des, pr_count, pr_photo)
    else:
        bot.send_message(admin_id, 'Некорректная ссылка!')
        # Возврат на этап получения фото
        bot.register_next_step_handler(message, get_pr_photo, pr_name, pr_des, pr_count)


# Этап получения цены
def get_pr_price(message, pr_name, pr_des, pr_count, pr_photo):
    admin_id = 692440883
    try:
        pr_price = float(message.text)
        db.add_pr(pr_name, pr_des, pr_count, pr_photo, pr_price)
        bot.send_message(admin_id, 'Продукт успешно добавлен, хотите что-то еще?',
                         reply_markup=bt.admin_menu())
        # Переход на этап выбора
        bot.register_next_step_handler(message, admin_choose)
    except ValueError or telebot.apihelper.ApiTelegramException:
        bot.send_message(admin_id, 'Ошибка в цене, попробуйте еще раз!')
        # Возврат на этап получения кол-ва
        bot.register_next_step_handler(message, get_pr_price, pr_name, pr_des, pr_count, pr_photo)


# Этап удаления продукта
def get_pr_id(message):
    admin_id = 692440883
    try:
        pr_id = int(message.text)
        check = db.check_pr_id(pr_id)
        if check:
            db.del_pr(pr_id)
            bot.send_message(admin_id, 'Продукт успешно удален, что-то ещё?',
                             reply_markup=bt.admin_menu())
            # Переход на этап выбора
            bot.register_next_step_handler(message, admin_choose)
        else:
            bot.send_message(admin_id, 'Такого продукта нет!')
            # Возврат на этап получения id
            bot.register_next_step_handler(message, get_pr_id)
    except ValueError or telebot.apihelper.ApiTelegramException:
        bot.send_message(admin_id, 'Ошибка id, попробуйте еще раз!')
        # Возврат на этап получения id
        bot.register_next_step_handler(message, get_pr_id)


# Этап изменения кол-во товара
def get_pr_change(message):
    admin_id = 692440883
    try:
        pr_id = int(message.text)
        check = db.check_pr_id(pr_id)
        if check:
            bot.send_message(admin_id, 'Сколько товара прибыло?')
            # Переход на этап прихода
            bot.register_next_step_handler(message, get_amount, pr_id)
        else:
            bot.send_message(admin_id, 'Такого продукта нет!')
            # Возврат на этап получения id
            bot.register_next_step_handler(message, get_pr_change)
    except ValueError or telebot.apihelper.ApiTelegramException:
        bot.send_message(admin_id, 'Ошибка id, попробуйте еще раз!')
        # Возврат на этап получения id
        bot.register_next_step_handler(message, get_pr_change)


# Этап прихода товара
def get_amount(message, pr_id):
    admin_id = 692440883
    try:
        new_amount = int(message.text)
        db.change_pr_count(pr_id, new_amount)
        bot.send_message(admin_id, 'Количество продукта изменено успешно! Что-то ещё?',
                         reply_markup=bt.admin_menu())
        # Переход на этап выбора
        bot.register_next_step_handler(message, admin_choose)
    except ValueError or telebot.apihelper.ApiTelegramException:
        bot.send_message(admin_id, 'Ошибка в количестве, попробуйте еще раз!')
        # Возврат на этап получения количества
        bot.register_next_step_handler(message, get_amount, pr_id)


bot.polling(none_stop=True)
