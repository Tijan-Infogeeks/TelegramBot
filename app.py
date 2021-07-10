import re
from flask import Flask, request , render_template, send_file
import telegram
from telegram import ParseMode
from telebot.credentials import bot_token, bot_user_name,URL
from telebot.reader import read_data

global bot
global TOKEN
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

@app.route('/{}'.format(TOKEN), methods=['GET', 'POST'])
def respond():
	global text
	global chat_id
	# retrieve the message in JSON and then transform it to Telegram object
	update = telegram.Update.de_json(request.get_json(force=True), bot)

	chat_id = update.message.chat.id
	msg_id = update.message.message_id

	# Telegram understands UTF-8, so encode text for unicode compatibility
	text = update.message.text.encode('utf-8').decode()
	# for debugging purposes only
	print("got text message :", text)
	# the first time you chat with the bot AKA the welcoming message
	if text == "/start":
		# print the welcoming message
		bot_welcome = "<a href='https://www.google.com/'>Google</a>"
		bot.sendMessage(chat_id=chat_id, text=bot_welcome, parse_mode=ParseMode.HTML)
		#bot.delete_message(chat_id=chat_id, message_id=msg_id, timeout=None, api_kwargs=None)

	elif text == "/sites" or text =="/sites@InfoGekksbot":
		try:
			file = "files/sites"
			with open(file, 'r') as f:
				mylist = f.read()
		except Exception:
			print("erreur dans la commande site")
			
		bot.sendMessage(chat_id=chat_id, text=mylist, parse_mode=ParseMode.HTML,disable_web_page_preview=True)
		#bot.delete_message(chat_id=chat_id, message_id=msg_id, timeout=None, api_kwargs=None)

	else:
		sorry = "Désolé , cette commande n'est pas prise en charge ☹"
	
	return 'ok'

@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
	s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
	if s:
		return "webhook setup ok"
	else:
		return "webhook setup failed"


@app.route('/')
def index():
	return render_template('index.html')

@app.route('/apk')
def dwl():
	return send_file('man.apk',
	mimetype="application/vnd.android.package-archive",
	 as_attachment=True,
	  attachment_filename="man.apk",
	   add_etags=True, cache_timeout=None,
	    conditional=False)
if __name__ == '__main__':
	app.run()