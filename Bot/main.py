#!/usr/bin/python
# -*- coding: utf-8 -*-

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler
from telegram.parsemode import ParseMode

from utils import Utils


class EasyCollect_Bot(object):
	def __init__(self):
		self.Utils_obj = Utils()
		self.bot_token = self.Utils_obj.getToken()
		self.key_text_dict = {
			'main' : {
				'keyboard' : [[InlineKeyboardButton("Cliente", callback_data='s1-cliente')], [InlineKeyboardButton("Commerciante", callback_data='s1-commerciante')]],
				'text' : "Benvenuto nel bot, cosa desideri effettuare?"
			},
			'commerciante' : {
				'keyboard' : [[InlineKeyboardButton("Aggiungi attività", callback_data='s2-add-activity')], [InlineKeyboardButton("Indietro", callback_data='back')]],
				'text' : "Vuoi aggiungere una tua attività?"
			},
   			'cliente' : {
				'keyboard' : [[InlineKeyboardButton("Lista attività", callback_data='s2-list-activity')], [InlineKeyboardButton("Indietro", callback_data='back')]],
				'text' : "Cosa desideri fare?"
			},
			'list-activity' : {
				'keyboard' : [[InlineKeyboardButton("Indietro", callback_data='back')]],
				'text' : "Non implementato"
			},
   			'add-activity' : {
				'keyboard' : [[InlineKeyboardButton("Indietro", callback_data='back')]],
				'text' : "Non implementato"
			}
		}

	""" Handler per l'esecuzione del comando /start"""
	def start(self, update, context):
		reply_markup = InlineKeyboardMarkup(self.key_text_dict['main']['keyboard'])
		update.message.reply_text(self.key_text_dict['main']['text'], reply_markup=reply_markup)

	""" Handler per l'esecuzione della callback_query che inzia con 's1-' (State 1) """
	""" Lista opzioni per cliente/commerciante """
	def main_handler(self, update, context):
		query = update.callback_query
		data = query.data.split('s1-', 1)[1]

		reply_markup = InlineKeyboardMarkup(self.key_text_dict[data.lower()]['keyboard'])
		toSend = self.key_text_dict[data.lower()]['text']

		query.edit_message_text(text=toSend, reply_markup=reply_markup)

	""" Handler per l'esecuzione della callback_query che inzia con 's2-' (State 2) """
	""" Lista opzioni per cliente/commerciante """
	def add_comm(self, update, context):
		query = update.callback_query
		data = query.data.split('s2-', 1)[1]

		reply_markup = InlineKeyboardMarkup(self.key_text_dict[data.lower()]['keyboard'])
		toSend = self.key_text_dict[data.lower()]['text']

		query.edit_message_text(text=toSend, reply_markup=reply_markup)
	
	""" Handler per l'esecuzione della callback_query 'back' """
	""" Ristampa i dati iniziali """
	def back(self, update, context):
		query = update.callback_query
		reply_markup = InlineKeyboardMarkup(self.key_text_dict['main']['keyboard'])
		query.edit_message_text(self.key_text_dict['main']['text'], reply_markup=reply_markup)

	"""Funzione di ausilio per registrare ogni handler e renderli disponibili per l'utilizzo nel main"""
	def registerAllHandlers(self):
		self.updater = Updater(self.bot_token, use_context=True)
		
		main_handler = CallbackQueryHandler(self.main_handler, pattern='^s1-')
		second_handler = CallbackQueryHandler(self.add_comm, pattern='^s2-')
		back_handler = CallbackQueryHandler(self.back, pattern='^back$')
		
		self.updater.dispatcher.add_handler(CommandHandler('start', self.start))
		self.updater.dispatcher.add_handler(main_handler)
		self.updater.dispatcher.add_handler(second_handler)
		self.updater.dispatcher.add_handler(back_handler)


	def main(self):
		self.registerAllHandlers()
		self.updater.start_polling()
		print("Polling...")
		self.updater.idle()

if __name__ == '__main__':
	botInstance = EasyCollect_Bot()
	botInstance.main()