import telebot
from telebot import types
import const
from geopy.distance import geodesic

bot = telebot.TeleBot(const.API_TOKEN)

markup_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
btn_address = types.KeyboardButton('Ближайший офис', request_location=True)
btn_payment = types.KeyboardButton('Способ оплаты')
btn_delivery = types.KeyboardButton('Способ доставки')
markup_menu.add(btn_address, btn_payment, btn_delivery)

markup_inline_payment = types.InlineKeyboardMarkup()
btn_in_cash = types.InlineKeyboardButton('Наличные', callback_data='cash')
btn_in_invoice = types.InlineKeyboardButton('Безналичные', callback_data='invoice')

markup_inline_payment.add(btn_in_cash, btn_in_invoice)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет я бот сайта!", reply_markup=markup_menu)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text == 'Способ оплаты':
        bot.reply_to(message, 'Можно оплатить так:', reply_markup=markup_inline_payment)
    elif message.text == 'Способ доставки':
        bot.reply_to(message, 'Доставка курьером, такси, почта России.', reply_markup=markup_menu)
    else:
        bot.reply_to(message, message.text, reply_markup=markup_menu)


@bot.message_handler(func=lambda message: True, content_types=['location'])
def magazin_location(message):
    lon = message.location.longitude
    lat = message.location.latitude

    print(lat, lon)

    distance = []
    for m in const.MAGAZINS:
        result = geodesic((m['latm'], m['lonm']), (lat, lon))
        distance.append(result)
    index = distance.index(min(distance))
    bot.send_message(message.chat.id, 'Ближайший к вам офис')
    bot.send_venue(message.chat.id,
                   const.MAGAZINS[index]['latm'],
                   const.MAGAZINS[index]['lonm'],
                   const.MAGAZINS[index]['title'],
                   const.MAGAZINS[index]['address']
                   )

@bot.callback_query_handler(func=lambda call:True)
def call_back_payment(call):
    if call.data == 'cash':
        bot.send_message(call.message.chat.id, text="""
        Наличная оплата производится в рублях, в кассе магазина
        """, reply_markup=markup_inline_payment)



bot.infinity_polling()
