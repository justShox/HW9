import telebot
import buttonsWTH as bt
import databaseWTH as db
from geopy import Nominatim
from telebot.types import ReplyKeyboardRemove
import json
import requests

bot = telebot.TeleBot('6833110655:AAHwDhNRr5PO7KvMA-THdqIs5LdzGhBVReI')

# Для локации
geolocator = Nominatim(
    user_agent='Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36')

# Для погоды
API = '04ce9501ff1973178da581c5d24d4b4f'


# Напишите мне свое имя😀:
@bot.message_handler(commands=['start'])
def welcome(message):
    user_id = message.from_user.id
    check = db.checker(user_id)
    if check:
        bot.send_message(user_id, f'С возвращением {message.from_user.first_name}☺️!'
                                  f'\nДля начала выберите язык🙃:'
                                  f'\n\nWelcome back {message.from_user.first_name}☺️!'
                                  f'\n To begin please choose language🙃:',
                         reply_markup=bt.language())
        bot.register_next_step_handler(message, get_language)
    else:
        bot.send_message(user_id, f"Здравствуйте {message.from_user.first_name}👋🏻"
                                  f"\nДавайте начнем регистрацию. Для начала выберите язык:"
                                  f"\n\nHello {message.from_user.first_name}👋🏻"
                                  f"\nLet's start registration. To begin, select your language:",
                         reply_markup=bt.language())
        bot.register_next_step_handler(message, get_language)


def get_name_ru(message):
    user_id = message.from_user.id
    name = message.text.title()
    bot.send_message(user_id, 'Хорошо! Теперь поделитесь контактом😃:',
                     reply_markup=bt.number_bt())
    bot.register_next_step_handler(message, get_contact_ru, name)


def get_name_en(message):
    user_id = message.from_user.id
    name = message.text.title().strip()
    bot.send_message(user_id, 'Good! Now please share your contact😃:',
                     reply_markup=bt.number_bt_en())
    bot.register_next_step_handler(message, get_contact_en, name)


def get_contact_ru(message, name):
    user_id = message.from_user.id
    if message.contact:
        number = message.contact.phone_number
        bot.send_message(user_id, 'Ага! И последнее осталось ваша локация😉:',
                         reply_markup=bt.location_bt())
        bot.register_next_step_handler(message, get_location_ru, name, number)
    else:
        bot.send_message(user_id, 'Пожалуйста поделитесь контактом😕', reply_markup=bt.number_bt_en())
        bot.register_next_step_handler(message, get_contact_ru, name)


def get_contact_en(message, name):
    user_id = message.from_user.id
    if message.contact:
        number = message.contact.phone_number
        bot.send_message(user_id, 'Ok! And the last one please share your location😉:',
                         reply_markup=bt.location_bt_en())
        bot.register_next_step_handler(message, get_location_en, name, number)
    else:
        bot.send_message(user_id, 'Please share your contact😕', reply_markup=bt.number_bt_en())
        bot.register_next_step_handler(message, get_contact_en, name)


def get_location_ru(message, name, number):
    user_id = message.from_user.id
    if message.location:
        location = str(geolocator.reverse(f'{message.location.latitude},{message.location.longitude}'))
        db.registration(user_id, name, number, location)
        bot.send_message(user_id, 'Получилось! Вы зарегистрированы😊.'
                                  '\nВведите любой город, чтоб узнать погоду🙃:', reply_markup=ReplyKeyboardRemove())
        bot.register_next_step_handler(message, get_weather_ru)
    else:
        bot.send_message(user_id, 'Пожалуйста поделитесь локацией🫤', reply_markup=bt.location_bt())
        bot.register_next_step_handler(message, get_location_ru, name, number, )


def get_location_en(message, name, number):
    user_id = message.from_user.id
    if message.location:
        location = str(geolocator.reverse(f'{message.location.latitude},{message.location.longitude}'))
        db.registration(user_id, name, number, location)
        bot.send_message(user_id, 'Done! You are registered😊.'
                                  '\nEnter any city to get the weather🙃:', reply_markup=ReplyKeyboardRemove())
        bot.register_next_step_handler(message, get_weather_en)
    else:
        bot.send_message(user_id, 'Please share your location🫤', reply_markup=bt.location_bt_en())
        bot.register_next_step_handler(message, get_location_en, name, number, )


def get_weather_ru(message):
    user_id = message.from_user.id
    if message.text:
        city = message.text.strip().title()
        info = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
        if info.status_code == 200:
            weather = json.loads(info.text)
            bot.send_message(user_id, f'Информация о {weather["name"]}, {weather["sys"]["country"]}'
                                      f'\n'
                                      f'\n Температура🌡: {weather["main"]["temp"]}°С,'
                                      f'\n Ощущается как😮‍💨: {weather["main"]["feels_like"]}°С'
                                      f'\n Влажность💦: {weather["main"]["humidity"]}%'
                                      f'\n Давление🫨: {weather["main"]["pressure"]}гПа'
                                      f'\n Скорость ветра🌬: {weather["wind"]["speed"]}м/с'
                                      f'\n Видимость👁: {weather["visibility"]} м'
                                      f'\n\nВведите еще город:')
            bot.register_next_step_handler(message, get_weather_ru)
        else:
            bot.send_message(user_id, 'Города не найден😓!')
            bot.register_next_step_handler(message, get_weather_ru)
    else:
        bot.send_message(user_id, 'Я вас не понимаю🤨!')
        bot.register_next_step_handler(message, get_weather_ru)


def get_weather_en(message):
    user_id = message.from_user.id
    if message.text:
        city = message.text.strip().title()
        info = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
        if info.status_code == 200:
            weather = json.loads(info.text)
            bot.send_message(user_id, f'Information about {weather["name"]}, {weather["sys"]["country"]}'
                                      f'\n'
                                      f'\n Temperature🌡: {weather["main"]["temp"]}°С,'
                                      f'\nFeels like😮‍💨: {weather["main"]["feels_like"]}°С'
                                      f'\nHumidity💦: {weather["main"]["humidity"]}%'
                                      f'\nPressure🫨: {weather["main"]["pressure"]}hPa'
                                      f'\n Wind speed🌬: {weather["wind"]["speed"]}m/s'
                                      f'\nVisibility👁: {weather["visibility"]} m'
                                      f'\n\nEnter another city:')
            bot.register_next_step_handler(message, get_weather_en)
        else:
            bot.send_message(user_id, 'City not found😓!')
            bot.register_next_step_handler(message, get_weather_en)
    else:
        bot.send_message(user_id, 'I do not understand you🤨!')
        bot.register_next_step_handler(message, get_weather_en)


@bot.callback_query_handler(func=lambda call: True)
def get_language(call):
    user_id = call.from_user.id
    if call.data == 'Ru':
        bot.send_message(user_id, 'Отлично! Напишите мне свое имя:')
        bot.register_next_step_handler(call.message, get_name_ru)
    elif call.data == 'En':
        bot.send_message(call.from_user.id, 'Cool! Now please write your name:')
        bot.register_next_step_handler(call.message, get_name_en)


bot.polling(none_stop=True)
