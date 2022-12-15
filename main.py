from GoogleNews import GoogleNews
import telebot
import sqlite3 as sl

NEWS_LIMIT = 3

with open('bot_token.txt', 'r') as f:
    token = f.readline().strip()
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Чтобы узнать последние новости, введите то о чем вы хотите узнать")


@bot.message_handler(commands=['ping'])
def ping(message):
    bot.send_message(message.chat.id, "Pong")


@bot.message_handler(commands=['google'])
def echo_all(message):
    googlenews = GoogleNews(lang='ru')
    googlenews.get_news(message.text)
    results = googlenews.results()
    for i in range(NEWS_LIMIT):
        answer = results[i]
        bot.send_message(message.chat.id, '*' + answer['title'] + '*', parse_mode='Markdown')
        bot.send_message(message.chat.id, answer['link'])


bot.infinity_polling()
