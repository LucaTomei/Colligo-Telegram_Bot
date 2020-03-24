from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler
from telegram.parsemode import ParseMode


from utils import Utils


class EasyCollect_Bot(object):
	def __init__(self):
		self.Utils_obj = Utils()
		self.bot_token = self.Utils_obj.getToken()
		self.main_keyboard = [[InlineKeyboardButton("Bottone 1", callback_data='rBottone_1'), InlineKeyboardButton("Bottone 2", callback_data='rBottone_2')]]
		self.main_keyboard_message = "Benvenuto nel bot, cosa desideri effettuare?"

	""" Handler per l'esecuzione del comando /start"""
	def start(self, update, context):
	    reply_markup = InlineKeyboardMarkup(self.main_keyboard)
	    update.message.reply_text(self.main_keyboard_message, reply_markup=reply_markup)

	def main_handler(self, update, context):
		query = update.callback_query
		first_name = query['message']['chat']['first_name']
		last_name = query['message']['chat']['last_name']
		data = query.data.split('r', 1)[1]
		
		toSend = "Bravo **" + first_name + " " + last_name + "**, hai premuto " + data
		query.edit_message_text(text=toSend)
		

	"""Funzione di ausilio per registrare ogni handler e renderli disponibili per l'utilizzo nel main"""
	def registerAllHandlers(self):
		self.updater = Updater(self.bot_token, use_context=True)
		
		main_handler = CallbackQueryHandler(self.main_handler, pattern='^r')
		
		self.updater.dispatcher.add_handler(CommandHandler('start', self.start))
		self.updater.dispatcher.add_handler(main_handler)


	def main(self):
		self.registerAllHandlers()
		self.updater.start_polling()
		self.updater.idle()



if __name__ == '__main__':
	botInstance = EasyCollect_Bot()
	botInstance.main()
		