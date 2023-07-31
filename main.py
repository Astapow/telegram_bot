import json
import sqlite3

import requests
import telebot
from telebot import types
import webbrowser

from settings import BOT_TOKEN, API_KEY

bot = telebot.TeleBot(BOT_TOKEN)
API = API_KEY
name = None


# @bot.message_handler(commands=['start'])
# def url(message):
#     markup = types.InlineKeyboardMarkup()
#     btn1 = types.InlineKeyboardButton(text='Мой сайт', url='http://127.0.0.1:8000')
#     markup.add(btn1)
#     bot.send_message(message.from_user.id, "По этой кнопке можно перейти на сайт")


# @bot.message_handler(commands=['start'])
# def start(message):
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     btn1 = types.KeyboardButton('Украінський')
#     btn2 = types.KeyboardButton('Русский')
#     btn3 = types.KeyboardButton('English')
#     markup.add(btn1, btn2, btn3)
#     bot.send_message(message.chat.id, "Выберите язык / Оберіть мову / Choose your language", reply_markup=markup)


@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('database.sql')
    cur = conn.cursor()

    cur.execute(
        'CREATE TABLE IF NOT EXISTS users '
        '(id int auto_increment primary key,'
        ' name varchar(50),'
        ' pass varchar(50)'
        ')')
    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, "Привет👋, давай мы тебя зарегестрируем😎 Введите имя")
    bot.register_next_step_handler(message, user_name)


def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, "Отлично👍, Теперь введите пароль:")
    bot.register_next_step_handler(message, user_pass)


def user_pass(message):
    password = message.text.strip()

    conn = sqlite3.connect('database.sql')
    cur = conn.cursor()

    cur.execute("INSERT INTO users (name, pass) VALUES ('%s', '%s')" % (name, password))
    conn.commit()
    cur.close()
    conn.close()

    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Список пользователей', callback_data='users')
    markup.add(btn1)
    bot.send_message(message.chat.id, "Супер👍, Пользователь зарегестрирован!", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    conn = sqlite3.connect('database.sql')
    cur = conn.cursor()

    cur.execute('SELECT * FROM users')
    users = cur.fetchall()
    info = ''
    for elem in users:
        info += f'Имя: {elem[1]}, Пароль: {elem[2]}\n'

    cur.close()
    conn.close()

    bot.send_message(call.message.chat.id, info)


@bot.message_handler(commands=['help'])
def questions(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Поздороваться 👋")
    markup.row(btn1)
    btn2 = types.KeyboardButton("Узнать погоду по городу")
    btn3 = types.KeyboardButton("Вопрос 2")
    markup.row(btn2, btn3)
    bot.send_message(message.from_user.id, f"Привет {message.from_user.first_name}! Я твой бот-помощник",
                     reply_markup=markup)
    bot.register_next_step_handler(message, on_click)


def on_click(message):
    if message.text == 'Поздороваться 👋':
        bot.send_message(message.chat.id, 'Чем я могу тебе помоч?')
    elif message.text == 'Узнать погоду по городу':
        bot.send_message(message.chat.id, 'Хорошо👌, просто впиши город!')
        bot.register_next_step_handler(message, get_weather)
    elif message.text == 'Вопрос 2':
        bot.send_message(message.chat.id, 'Ответ 2')


# @bot.message_handler(commands=['help'])
# def start(message):
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     btn1 = types.KeyboardButton("Нужна помощь")
#     markup.add(btn1)
#     bot.send_message(message.from_user.id, "<b>Привет</b>! <em>Чем я могу тебе помоч</em>", parse_mode='html')


@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    if res.status_code == 200:
        data = json.loads(res.text)
        temp = data["main"]["temp"]
        weather = data["weather"][0]["main"]

        bot.reply_to(message, f'Погода сейчас: {temp}°C')

        if weather == "Clouds":
            image = 'Clouds.png'
        elif weather == "Rain":
            image = "rain.jpg"
        elif weather == "Snow":
            image = 'snow.jpg'
        elif weather == "Clear":
            image = 'Clear.jpg'

        file = open('image/' + image, 'rb')
        bot.send_photo(message.chat.id, file)
    else:
        bot.reply_to(message, f'Город указан неверно!')


@bot.message_handler(commands=['site', 'website'])
def get_site(message):
    webbrowser.open('https://google.com')


@bot.message_handler(content_types=['photo', 'video', 'audio'])
def get_media(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Перейти на сайт', url='https://google.com')
    markup.row(btn1)
    btn2 = types.InlineKeyboardButton('Удалить файл', callback_data='delete')
    btn3 = types.InlineKeyboardButton('Редоктировать текст', callback_data='edit')
    markup.row(btn2, btn3)
    bot.reply_to(message, 'Спасибо я получил твой файл', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_message(call):
    if call.data == 'delete':
        bot.delete_message(call.message.chat.id, call.message.message_id - 1)
        bot.delete_message(call.message.chat.id, call.message.message_id)
    elif callback.data == 'edit':
        new_text = "This is the updated text."
        bot.edit_message_text(new_text, call.message.chat.id, call.message.message_id)


@bot.message_handler(content_types=['text'])
def get_text_message(message):
    if message.text == 'Поздороваться 👋':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Тема1 👌')
        btn2 = types.KeyboardButton('Тема2 👍')
        btn3 = types.KeyboardButton('Тема3 😎')
        markup.add(btn1, btn2, btn3)
        bot.send_message(message.from_user.id, "Задай интересующий вопрос", reply_markup=markup)

    elif message.text == 'Тема1 👌':
        bot.send_message(message.from_user.id, 'Мой ответ 1')

    elif message.text == 'Тема2 👍':
        bot.send_message(message.from_user.id, 'Мой ответ 2')

    elif message.text == 'Тема3 😎':
        bot.send_message(message.from_user.id, 'Мой ответ 3')


bot.infinity_polling()
