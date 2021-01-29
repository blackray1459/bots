# My test bot for Telegram

import telebot
import config
import random

from telebot import types

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    parrot = open('stickers/parrot_glasses.tgs', 'rb')
    bot.send_sticker(message.chat.id, parrot)

    #keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_random = types.KeyboardButton("Рандомное число")
    button_howisit = types.KeyboardButton("Как дела?")
    button_changeletter = types.KeyboardButton("Поменять раскладку")

    markup.row(button_random, button_howisit).add(button_changeletter)

    bot.send_message(message.chat.id, "Приветствую в тестовом боте, {0.first_name}!\nТут проводятся тесты функций для "
                                      "ботов в Телеграм.\nМеня зовут <b>{1.first_name}</b>".format(message.from_user,
                                                                                                   bot.get_me()),
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(commands=['help'])
def help_me(message):
    bot.send_message(message.chat.id, "Здесь появится помощь! The bot is under construction...")


@bot.message_handler(commands=['stop'])
def goodbye(message):
    remove_keys = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, "Было приятно! Возвращайтесь!", reply_markup=remove_keys)


@bot.message_handler(content_types=['text'])
def chatting(message):
    if message.chat.type == 'private':
        if message.text == 'Рандомное число':
            bot.send_message(message.chat.id, str(random.randint(0, 100)))
        elif message.text == 'Как дела?':
            markup = types.InlineKeyboardMarkup(row_width=3)
            item1 = types.InlineKeyboardButton("Отлично", callback_data='perfect')
            item2 = types.InlineKeyboardButton("Нормально", callback_data='good')
            item3 = types.InlineKeyboardButton("Не очень", callback_data='bad')
            markup.add(item1, item2, item3)
            bot.send_message(message.chat.id, "Пока не родила. 😂\nА у тебя?", reply_markup=markup)
        elif message.text == "Поменять раскладку":
            markup = types.InlineKeyboardMarkup(row_width=1)
            item1 = types.InlineKeyboardButton("Русский -> Английский", callback_data='to_english')
            item2 = types.InlineKeyboardButton("Английский -> Русский", callback_data='to_russian')
            markup.add(item1).add(item2)

            bot.send_message(message.chat.id, "Как мне поменять раскладку?", reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "Не знаю что сказать. The bot is under construction...")


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
            if call.data == 'perfect':
                bot.send_message(call.message.chat.id, "И это прекрасно!")
            elif call.data == 'good':
                bot.send_message(call.message.chat.id, "А будет супер!")
            elif call.data == 'bad':
                bot.send_message(call.message.chat.id, "Ну что ж такое 😩")
            elif call.data == 'to_english':
                bot.send_message(call.message.chat.id, "Скоро тут будет смена раскладки С РУССКОГО НА АНГЛИЙСКИЙ")
            elif call.data == 'to_russian':
                bot.send_message(call.message.chat.id, "Скоро тут будет смена раскладки С АНГЛИЙСКОГО НА РУССКИЙ")
            # show alert
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Тестовое уведомление!")
    except Exception as e:
        print(repr(e))


# RUN
bot.polling(none_stop=True)
