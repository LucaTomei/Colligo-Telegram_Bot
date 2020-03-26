import json, requests, telepot, time
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove

from utils import Utils

class Bot(object):
	def __init__(self):
		self.Utils_obj = Utils()
		self.bot_token = self.Utils_obj.getToken()	# contiene il token del bot

		self.bot = telepot.Bot(self.bot_token)

		# Definizione Bottoni tastiera
		self.button_location = "📍 Posizione 📍"
		self.button_categoty = "🥐 Categoria 🍷"
		self.stop_button = "Stop"
		self.other_categories_button = "Altra Categoria"

		categories_list = self.Utils_obj.getAllMerchantCategories()
		self.categories_keyboard = self.makeAKeyboard(categories_list, 6)
		
		self.main_keyboard = [[self.button_categoty],[self.button_location]]


		self.category_message = "Inserisci la categoria di negozio che più ti si addice.\nPuoi inserire fino ad un massimo di tre categorie.\n[Premere il pulsante Stop per terminare l'aggiunta]"
		self.position_message = "Inviami la posizione"
		self.main_message = "Utilizza la tastiera sottostante"
		self.category_error_message = "Inserire almeno una tra le categorie elencate"
		self.category_ok_message = "Categorie aggiunte con successo. Il tuo negozio rispecchia le seguenti categorie: "
		self.base_step = 0

		self.added_categories = []
		self.myLocation = (None, None)

		self.max_categories = 3
		self.count_categories = 0

		self.is_set_categoria = False
		self.is_set_location = False
		self.i_can_send_location = False

	def makeAKeyboard(self,alist, parti):
	    length = len(alist)
	    keyboard =  [alist[i*length // parti: (i+1)*length // parti] for i in range(parti)]
	    keyboard.append([self.other_categories_button, self.stop_button])
	    return keyboard

	def main_handler(self, msg):
		try:
			content_type, chat_type, chat_id = telepot.glance(msg)
			print("Tipo contenuto: " + content_type + " - Tipo Chat: " + chat_type)
			chat_id = msg['chat']['id']
			first_name = msg['from']['first_name']
			last_name = msg['from']['last_name']
			group_title = msg['chat']['title']

			# si tratta di un commerciante che è in un gruppo
			if 'chat' in msg and 'group' in chat_type:	# per gruppi e supergruppi
				if not self.is_set_location or not self.is_set_categoria:
					# Si tratta di messaggio testuale
					if content_type == 'text':
						chat_message = msg['text']
						# hai premuto uno dei bottoni della tastiera principale
						if chat_message in [j for i in self.main_keyboard for j in i]:
							if chat_message == self.button_categoty:
								self.bot.sendMessage(chat_id, text=self.category_message, reply_markup={'keyboard': self.categories_keyboard},parse_mode= 'Markdown')
							elif chat_message == self.button_location:
								self.bot.sendMessage(chat_id, text=self.position_message,parse_mode= 'Markdown', reply_markup = ReplyKeyboardRemove())
								self.i_can_send_location = True
						
						elif self.base_step == 1:
							self.bot.sendMessage(chat_id, text="Ok, registro la tua categoria di " + chat_message, reply_markup={'keyboard': self.main_keyboard},parse_mode= 'Markdown')
							self.count_categories +=1
							self.added_categories.append(chat_message)
							self.base_step = 0
							# rimozione bottone categoria dalla tastiera principale
							if self.count_categories == self.max_categories:
								self.main_keyboard = [[self.button_location]]
								self.is_set_categoria = True

						elif chat_message in [j for i in self.categories_keyboard for j in i]:
							if chat_message == "Altra Categoria":
								self.bot.sendMessage(chat_id, text=self.category_message, reply_markup = ReplyKeyboardRemove(),parse_mode= 'Markdown')
								self.base_step = 1
							elif chat_message == self.stop_button:
								if len(self.added_categories) > 0:
									self.is_set_categoria = True
								else:
									self.bot.sendMessage(chat_id, text=self.category_error_message, reply_markup = {'keyboard': self.main_keyboard},parse_mode= 'Markdown')
							if not self.is_set_categoria:
								if self.base_step != 1:
									self.base_step = 0
									if chat_message not in self.added_categories:
										if chat_message != self.stop_button:
											self.bot.sendMessage(chat_id, text="Ok, registro la tua categoria di " + chat_message, reply_markup={'keyboard': self.main_keyboard},parse_mode= 'Markdown')
											self.added_categories.append(chat_message)
											self.count_categories += 1
											# rimozione bottone categoria dalla tastiera principale
											if self.count_categories == self.max_categories:
												self.main_keyboard = [[self.button_location]]
												self.is_set_categoria = True
									else:
										self.bot.sendMessage(chat_id, text="Categoria di " + chat_message + " già aggiunta.", reply_markup={'keyboard': self.main_keyboard},parse_mode= 'Markdown')
							else:
								toSend = "Le Categorie sono già settate *" + str(self.added_categories) + "*"
								if not self.is_set_location:
									toSend = toSend + ", ti manca solo l'invio della posizione"
									self.main_keyboard = [[self.button_location]]
								else:
									toSend = toSend + ", la tua posizione è " + str(self.myLocation) 
								self.bot.sendMessage(chat_id, text= toSend, reply_markup={'keyboard': self.main_keyboard},parse_mode= 'Markdown')
						else:
							self.bot.sendMessage(chat_id, text=self.main_message, reply_markup={'keyboard': self.main_keyboard},parse_mode= 'Markdown')

					# mi hai inviato la posizione
					elif content_type == 'location' and self.i_can_send_location and not self.is_set_location:
						self.myLocation = (latitude, longitude) = (msg['location']['latitude'], msg['location']['longitude'])
						toSend = "Posizione Inviata: [" + str(latitude) + ", " + str(longitude) + "]"
						
						if not self.is_set_categoria:
							self.main_keyboard = [[self.button_categoty]]

						self.bot.sendMessage(chat_id, text=toSend,parse_mode= 'Markdown', reply_markup={'keyboard': self.main_keyboard})
						self.is_set_location = True
					#  Messaggio di benvenuto appena si accede al bot
					elif content_type == 'new_chat_member':
						toSend = "Ciao " + first_name + " " + last_name + " del gruppo " + group_title + " utilizza la tastiera sottostante per eseguire le azioni sul bot"
						self.bot.sendMessage(chat_id, text=toSend, reply_markup={'keyboard': self.main_keyboard},parse_mode= 'Markdown')
					#  Per qualsiasi altro caso inviami la tastiera
					else:
						self.bot.sendMessage(chat_id, text=self.main_message, reply_markup={'keyboard': self.main_keyboard},parse_mode= 'Markdown')
				elif self.is_set_categoria and self.is_set_location:
					toSend = "Tutto impostato con successo:\nCategorie del negozio: *" + str(self.added_categories) + "*\nPosizione del nezio: *" + str(self.myLocation) + "*."
					self.bot.sendMessage(chat_id, text=toSend, reply_markup = ReplyKeyboardRemove(),parse_mode= 'Markdown')

		except telepot.exception.BotWasKickedError as e:
			print("Sei stato buttato fuori dal gruppo")
		except Exception as e:
			print("Eccezzione: " + str(e))

	def main(self):
		print("In Loop...")
		MessageLoop(self.bot, self.main_handler).run_as_thread()
		
		while True:	time.sleep(1)



if __name__ == '__main__':
	Bot = Bot()
	Bot.main()



