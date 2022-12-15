from GoogleNews import GoogleNews
import telebot
import sqlite3 as sl
from multiprocessing import Lock
import os
import asyncio
from datetime import datetime

mutex = Lock()


NEWS_LIMIT = 3

with open('bot_token.txt', 'r') as f:
    token = f.readline().strip()
bot = telebot.TeleBot(token)


database_name = 'database.db'
existed = os.path.exists(database_name)

con = sl.connect(database_name, check_same_thread=False)
if not existed:
    print('No database found, create...')
    with con:
        con.execute("""
                CREATE TABLE USER (
                id INTEGER,
                topic TEXT
            );
        """)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Чтобы узнать последние новости, введите то о чем вы хотите узнать")


@bot.message_handler(commands=['ping'])
def ping(message):
    bot.send_message(message.chat.id, "Pong")


def send_google_news(chat_id, query):
    googlenews = GoogleNews(lang='ru')
    googlenews.get_news(query)
    results = googlenews.results()
    for i in range(NEWS_LIMIT):
        answer = results[i]
        bot.send_message(chat_id, '*' + answer['title'] + '*', parse_mode='Markdown')
        bot.send_message(chat_id, answer['link'])


@bot.message_handler(commands=['google'])
def google_news(message):
    send_google_news(message.chat.id, message.text)


@bot.message_handler(commands=['subscribe'])
def subscribe(message):
    with mutex:
        sql = 'INSERT INTO USER (id, topic) values(?, ?)'
        query = message.text
        prefix = '/subscribe '
        if query.startswith(prefix):
            query = query[len(prefix):]
        data = [
            (message.chat.id, query),
        ]
        with con:
            con.executemany(sql, data)


@bot.message_handler(commands=['remind'])
def remind_subscriptions(message):
    with con:
        data = con.execute(f"SELECT * FROM USER WHERE id == {message.chat.id}")
        send_something = False
        for row in data:
            bot.send_message(message.chat.id, str(row[1]))
            send_something = True
        if not send_something:
            bot.send_message(message.chat.id, 'Нет подписок!:')


bot.infinity_polling()
