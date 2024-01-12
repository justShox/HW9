from telebot import types


def language():
    language_button = types.InlineKeyboardMarkup(row_width=2)
    ru = types.InlineKeyboardButton(text='Ru🇷🇺', callback_data='Ru')
    en = types.InlineKeyboardButton(text='En🇬🇧', callback_data='En')
    language_button.add(ru, en)
    return language_button


def number_bt():
    user_contact = types.ReplyKeyboardMarkup(resize_keyboard=True)
    contact = types.KeyboardButton('Поделится контактом📲', request_contact=True)
    user_contact.add(contact)
    return user_contact


def number_bt_en():
    user_contact = types.ReplyKeyboardMarkup(resize_keyboard=True)
    contact = types.KeyboardButton('Share contact📲', request_contact=True)
    user_contact.add(contact)
    return user_contact


def location_bt():
    user_location = types.ReplyKeyboardMarkup(resize_keyboard=True)
    location = types.KeyboardButton('Поделиться локацией📍', request_location=True)
    user_location.add(location)
    return user_location


def location_bt_en():
    user_location = types.ReplyKeyboardMarkup(resize_keyboard=True)
    location = types.KeyboardButton('Share location📍', request_location=True)
    user_location.add(location)
    return user_location
