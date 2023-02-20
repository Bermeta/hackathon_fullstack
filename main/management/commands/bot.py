from django.core.management.base import BaseCommand

from category.models import Category
from main import settings
from telebot import types
import telebot
from product.models import Product


bot = telebot.TeleBot(settings.TELEGRAM_BOT_API_KEY, threaded=False)

bot.set_my_commands(([
    telebot.types.BotCommand("/start", "старт"),
    telebot.types.BotCommand("/all", "все товары")
]))

inline_keyboard = types.InlineKeyboardMarkup()
btn1 = types.InlineKeyboardButton('Бренд одежд', callback_data='brand')
btn2 = types.InlineKeyboardButton('Категории', callback_data='categories')
inline_keyboard.add(btn1, btn2)


@bot.message_handler(commands=['start'])
def get_message(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, text="Привет, {0.first_name}! Я бот для RENTIK! Cделайте выбор:".format(message.from_user),
                     reply_markup=inline_keyboard)


@bot.message_handler(content_types=['text'])
def send_message(message):
    chat_id = message.chat.id
    if message.text == 'Показать все товары от RENTIK!':
        data = Product.objects.all()
        for dict_ in data:
            bot.send_message(
                chat_id, f"\nTitle: {dict_.title}\n"
                         f"Description: {dict_.description}\n"
                         f"Category: {dict_.category}\n"
                         f"Brand: {dict_.brand}\n"
                         f"SEX: {dict_.sex}\n"
                         f"Price: {dict_.price}\n"
                         f"Stock: {dict_.stock}\n"
                         f"Preview: http://127.0.0.1:8000/media/{dict_.preview}\n"
            )



@bot.callback_query_handler(func=lambda c: True)
def inline(c):
    if c.data == 'brand':
        chat_id = c.message.chat.id
        brand_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        key1 = types.KeyboardButton('PUMA')
        key2 = types.KeyboardButton('adidas')
        key3 = types.KeyboardButton('Reebok')
        key4 = types.KeyboardButton('Timberland')
        key5 = types.KeyboardButton('Nike')
        brand_keyboard.add(key1, key2, key3, key4, key5)
        msg = bot.send_message(chat_id,
                         text='Выберие бренд одежды:', reply_markup=brand_keyboard)
        bot.register_next_step_handler(msg, get_brand)
    if c.data == 'categories':
        chat_id = c.message.chat.id
        brand_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        k1 = types.KeyboardButton('Sport')
        k2 = types.KeyboardButton('T-Shirt')
        k3 = types.KeyboardButton('Shoes')
        brand_keyboard.add(k1, k2, k3)
        msg1 = bot.send_message(chat_id,
                         text='Выберите категории:', reply_markup=brand_keyboard)
        bot.register_next_step_handler(msg1, get_category)


def get_brand(message):
    chat_id = message.chat.id
    print(message.text)
    if message.text == 'PUMA':
        data = Product.objects.filter(brand='PUMA')
        for i in data:
            bot.send_message(chat_id, i)
    elif message.text == 'Nike':
        data = Product.objects.filter(brand='Nike')
        for i in data:
            bot.send_message(chat_id, i)
    elif message.text == 'adidas':
        data = Product.objects.filter(brand='adidas')
        for i in data:
            bot.send_message(chat_id, i)
    elif message.text == 'Reebok':
        data = Product.objects.filter(brand='Rebook')
        for i in data:
            bot.send_message(chat_id, i)
    elif message.text == 'Timberland':
        data = Product.objects.filter(brand='Timberland')
        for i in data:
            bot.send_message(chat_id, i)


def get_category(message):
    chat_id = message.chat.id
    if message.text == 'T-shirt':
        data = Category.objects.filter(category='T-shirt')
        for i in data:
            bot.send_message(chat_id, i)
    elif message.text == 'Sport':
        data = Product.objects.filter(brand='trousers')
        for i in data:
            bot.send_message(chat_id, i)
    elif message.text == 'Shoes':
        data = Product.objects.filter(brand='sneakers')
        for i in data:
            bot.send_message(chat_id, i)

@bot.message_handler(commands=['all'])
def get_message(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Показать все товары от RENTIK!')
    markup.add(btn1)
    bot.send_message(chat_id, text="Нажав на кнопку можно посмотреть все товары от RENTIK!".format(message.from_user),

                     reply_markup=markup)


# @bot.message_handler(commands=['start'])
# def get_message(message):
#     chat_id = message.chat.id
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     btn1 = types.KeyboardButton('Показать все товары от RENTIK!')
#     btn2 = types.KeyboardButton('Categories!')
#     btn3 = types.KeyboardButton('Brands!')
#     markup.add(btn1, btn2, btn3)
#     bot.send_message(chat_id, text="Привет, {0.first_name}! Я бот для RENTIK!".format(message.from_user),
#                      reply_markup=markup)


# @bot.message_handler(content_types=['text'])
# def send_message(message):
#     chat_id = message.chat.id
#     if message.text == 'Показать все товары от RENTIK!':
#         data = Product.objects.all()
#         for dict_ in data:
#             bot.send_message(
#                 chat_id, f"\nTitle: {dict_.title}\n"
#                          f"Description: {dict_.description}\n"
#                          f"Category: {dict_.category}\n"
#                          f"Brand: {dict_.brand}\n"
#                          f"SEX: {dict_.sex}\n"
#                          f"Price: {dict_.price}\n"
#                          f"Stock: {dict_.stock}\n"
#                          f"Preview: http://127.0.0.1:8000/media/{dict_.preview}\n"
#             )
#     elif message.text == 'Categories!':
#         data = Product.objects.all()
#         for dict_ in data:
#             bot.send_message(
#                 chat_id, f"Category: {dict_.category}\n"
#                          f"\nTitle: {dict_.title}\n"
#                          f"Description: {dict_.description}\n"
#                          f"Preview: http://127.0.0.1:8000/media/{dict_.preview}\n"
#             )
#     elif message.text == 'Brands!':
#         data = Product.objects.all()
#         for dict_ in data:
#             bot.send_message(
#                 chat_id,  f"Brand: {dict_.brand}\n"
#                          f"\nTitle: {dict_.title}\n"
#                          f"Description: {dict_.description}\n"
#                          f"Preview: http://127.0.0.1:8000/media/{dict_.preview}\n"
#             )
#     else:
#         markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#         btn4 = types.KeyboardButton('Показать все товары от RENTIK!')
#         markup.add(btn4)
#         bot.send_message(chat_id, 'Я не знаю такой команды! Введите правильный ID', reply_markup=markup)


class Command(BaseCommand):
    help = 'Implemented to Django application telegram bot setup command'

    def handle(self, *args, **kwargs):
        bot.enable_save_next_step_handlers(delay=2)
        bot.load_next_step_handlers()
        bot.infinity_polling()
