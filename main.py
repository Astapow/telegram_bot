import telebot
from telebot import types

bot = telebot.TeleBot('5668453655:AAEl60su5kExMONljwa1_4y8rBdYjHggO0U')


@bot.message_handler(commands=['start'])
def url(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Мой сайт', url='http://127.0.0.1:8000')
    markup.add(btn1)
    bot.send_message(message.from_user.id, "По этой кнопке можно перейти на сайт")


# @bot.message_handler(commands=['start'])
# def start(message):
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     btn1 = types.KeyboardButton('Украінський')
#     btn2 = types.KeyboardButton('Русский')
#     btn3 = types.KeyboardButton('English')
#     markup.add(btn1, btn2, btn3)
#     bot.send_message(message.from_user.id, "Выберите язык / Оберіть мову / Choose your language", reply_markup=markup)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Поздороваться")
    markup.add(btn1)
    bot.send_message(message.from_user.id, "Привет! Я твой бот-помощник", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_text_message(message):
    if message.text == 'Поздороваться':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Тема1')
        btn2 = types.KeyboardButton('Тема2')
        btn3 = types.KeyboardButton('Тема3')
        markup.add(btn1, btn2, btn3)
        bot.send_message(message.from_user.id, "Задай интересующий вопрос", reply_markup=markup)

    elif message.text == 'Тема1':
        bot.send_message(message.from_user.id, 'Мой ответ 1')

    elif message.text == 'Тема2':
        bot.send_message(message.from_user.id, 'Мой ответ 2')

    elif message.text == 'Тема3':
        bot.send_message(message.from_user.id, 'Мой ответ 3')


bot.polling(none_stop=True, interval=0)
