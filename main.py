from GoogleNews import GoogleNews
import telebot

with open('bot_token.txt', 'r') as f:
	token = f.readline().strip()
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Привет! Чтобы узнать последние новости, введите то о чем вы хотите узнать")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
	googlenews = GoogleNews(lang='ru')
	googlenews.get_news(message.text)

	answer = googlenews.results()[0]
	bot.reply_to(message, answer['title'])


bot.infinity_polling()

