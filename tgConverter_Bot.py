import telebot
from config import keys, TOKEN
from extension import ConvertionException, Converter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Привет! :)\nЧтобы начать работу, тебе нужно написать команду боту в следующем формате:\n\n<имя валюты> \
<имя валюты, в которую нужно перевести> \
<количество первой валюты>\n\nчерез пробел, без точек и запятых — это важно!\n\nУвидеть список всех доступнных валют можно через команду: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:\n'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
        values = message.text.split(' ')

        if len(values) != 3:
               raise ConvertionException('Слишком много параметров!')

        quote, base, amount = values
        quote_ticker, base_ticker = keys[quote], keys[base]
        total_base = Converter.convert(quote, base, amount)

        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling()