import json, requests, telepot, time
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove

from utils import Utils

# 	Dopo aver inviato la roba tramite rest devo resettare le variabili locali -----|
#	self.resetAllVariables()	<--------------------------------------------------|

# Check se negozio è già presente
 
class Bot(object):
	def __init__(self):
		self.Utils_obj = Utils()
		self.bot_token = self.Utils_obj.getToken()	# contiene il token del bot

		self.bot = telepot.Bot(self.bot_token)

		# Definizione Bottoni tastiera
		self.button_location = "📍 Posizione 📍"
		self.button_categoty = "🥐 Categoria 🍷"
		self.stop_button = "Fine"
		self.other_categories_button = "Altro"
		self.yes_button = "👍 SI 👍"
		self.no_button = "👎 NO 👎"

		categories_list = self.Utils_obj.getAllMerchantCategories()
		self.categories_keyboard = self.makeAKeyboard(categories_list, 6)
		
		self.main_keyboard = [[self.button_categoty],[self.button_location]]

		self.yes_no_keyboard = [[self.yes_button],[self.no_button]]
		

		self.category_message = "Seleziona a quale categoria appartiene il tuo negozio.(Max 3)\n*[Premere il pulsante Fine per terminare la selezione]*"
		self.position_message = "Inviami la posizione(clicca sulla spilla e seleziona *Posizione*, quindi seleziona *Invia posizione corrente*)"
		self.main_message = "Utilizza la tastiera sottostante"
		self.category_error_message = "Inserire almeno una tra le categorie elencate"

		self.description_message =  "Attraverso i pannelli sottostanti potrai selezionare le categorie che descrivono il tuo negozio e condividere la tua posizione con i clienti."
		
		self.error_message = "Qualcosa è andato storto con la registrazione del tuo negozio\nRicominciamo la registrazione dall'inizio."

		self.location_error_message =  "Non è stato possibile salvare la posizione del tuo negozio.\nInseriscila manualmente attenendoti al seguente formato: *via*, *CAP*, *città*.\nEsempio: *Via corcolle 30, 00123, Roma*"

		self.resetAllVariables()
		
	def makeAKeyboard(self,alist, parti):
	    length = len(alist)
	    keyboard =  [alist[i*length // parti: (i+1)*length // parti] for i in range(parti)]
	    keyboard.append([self.stop_button])
	    return keyboard

	def resetAllVariables(self):
		self.main_keyboard = [[self.button_categoty],[self.button_location]]
		self.group_title = ''
		self.username = ''

		self.added_categories = []
		self.myLocation = (None, None)
		self.is_super_group_flag = False
		self.max_categories = 3
		self.count_categories = 0
		self.is_set_categoria = False
		self.is_set_location = False
		self.i_can_send_location = False
		self.myLocation = (None, None)
		self.yes_no_step = (False, None)
		self.webSiteName = ""
		self.webSiteStep = 0
		self.location_error_step = 0

	def send_welcome_message(self, chat_id, first_name, group_title):
		self.group_title = group_title
		toSend = "Benvenuto *" + first_name + "*  del negozio *" + group_title + "* sono ColliGo, il bot che ti accompagnerà nella vendita online della tua attività.\nHai un sito web del negozio?"
		self.bot.sendMessage(chat_id, text=toSend, reply_markup={'keyboard': self.yes_no_keyboard},parse_mode= 'Markdown')
		self.webSiteStep = 1

	def main_keyboard_handler(self, chat_id ,chat_message):
		if chat_message == self.button_categoty:
			self.bot.sendMessage(chat_id, text=self.category_message, reply_markup={'keyboard': self.categories_keyboard},parse_mode= 'Markdown')
		elif chat_message == self.button_location:
			self.bot.sendMessage(chat_id, text=self.position_message,parse_mode= 'Markdown', reply_markup = ReplyKeyboardRemove())
			self.i_can_send_location = True

	def yes_no_handler(self, chat_id, chat_message):
		category = self.yes_no_step[1]
		if chat_message == self.yes_button:
			self.added_categories.append(category)
			self.count_categories += 1
			# rimozione bottone categoria dalla tastiera principale
			if self.count_categories == self.max_categories:
				self.main_keyboard = [[self.button_location]]
				self.is_set_categoria = True
				toSend = "Ecco le categorie che hai impostato\n*" + str(self.added_categories) + "*"
				if self.is_set_location:
					toSend = toSend + ", questa è la posizione del tuo negozio " + str(self.myLocation[1])
					self.bot.sendMessage(chat_id, text=toSend, reply_markup={'keyboard': self.main_keyboard},parse_mode= 'Markdown')
				else:
					self.bot.sendMessage(chat_id, text=toSend, reply_markup={'keyboard': self.main_keyboard},parse_mode= 'Markdown')
			else:
				self.bot.sendMessage(chat_id, text="Categoria *" + category +"* aggiunta con successo.\n*[Premere il pulsante Fine per terminare la selezione]*", reply_markup={'keyboard': self.categories_keyboard},parse_mode= 'Markdown')
		elif chat_message == self.no_button:
			self.bot.sendMessage(chat_id, text="Inserire nuovamente la categoria", reply_markup={'keyboard': self.categories_keyboard},parse_mode= 'Markdown')
		self.yes_no_step = (False, None)

	def category_handler(self, chat_id, chat_message):
		if chat_message == self.stop_button:
			if len(self.added_categories) > 0:
				self.is_set_categoria = True
				if not self.is_set_location:
					self.main_keyboard = [[self.button_location]]
					toSend = "Ecco le categorie che hai impostato\n*" + str(self.added_categories) + "*"
					self.bot.sendMessage(chat_id, text= toSend, reply_markup = {'keyboard': self.main_keyboard},parse_mode= 'Markdown')
				else:
					lat, lng = self.myLocation
					status_code = self.Utils_obj.post_shop_details(self.group_title, self.added_categories, self.webSiteName,self.username,lat, lng)
					if status_code == 200: 
						toSend = "Tutto impostato con successo:\nCategorie del negozio: *" + str(self.added_categories) + "*\nPosizione del negozio: *" + str(self.myLocation) + "*."
						self.bot.sendMessage(chat_id, text= toSend, reply_markup = ReplyKeyboardRemove(),parse_mode= 'Markdown')
						self.resetAllVariables()
						self.Utils_obj.stop_user(chat_id)
					else:
						self.bot.sendMessage(chat_id, text= self.location_error_message, reply_markup = ReplyKeyboardRemove(),parse_mode= 'Markdown')
						self.location_error_step = 1

			else:
				self.bot.sendMessage(chat_id, text=self.category_error_message, reply_markup = {'keyboard': self.main_keyboard},parse_mode= 'Markdown')
		if not self.is_set_categoria:
			if chat_message not in self.added_categories:
				if chat_message != self.stop_button:
					self.bot.sendMessage(chat_id, text="Sei sicuro di voler aggiungere la categoria *" + chat_message + "*?", reply_markup={'keyboard': self.yes_no_keyboard},parse_mode= 'Markdown')
					self.yes_no_step = (True, chat_message)
			else:
				self.bot.sendMessage(chat_id, text="Categoria di " + chat_message + " già aggiunta.", reply_markup={'keyboard': self.main_keyboard},parse_mode= 'Markdown')

	def location_handler(self, chat_id, msg):
		self.myLocation = (latitude, longitude) = (msg['location']['latitude'], msg['location']['longitude'])
		toSend = "Posizione Registrata: *[" + str(latitude) + ", " + str(longitude) + "]*"
		if not self.is_set_categoria:
			self.main_keyboard = [[self.button_categoty]]
			self.bot.sendMessage(chat_id, text=toSend,parse_mode= 'Markdown', reply_markup={'keyboard': self.main_keyboard})
			self.is_set_location = True
		else:
			status_code = self.Utils_obj.post_shop_details(self.group_title, self.added_categories, self.webSiteName,self.username, latitude, longitude)
			if status_code == 200: 
				toSend = "Tutto impostato con successo:\nCategorie del negozio: *" + str(self.added_categories) + "*\nPosizione del negozio: *" + str(self.myLocation) + "*."
				self.bot.sendMessage(chat_id, text= toSend, reply_markup = ReplyKeyboardRemove(),parse_mode= 'Markdown')
				self.resetAllVariables()
				self.Utils_obj.stop_user(chat_id)
			else:
				self.bot.sendMessage(chat_id, text= self.location_error_message, reply_markup = ReplyKeyboardRemove(),parse_mode= 'Markdown')
				self.location_error_step = 1
			
			

	def main_handler(self, msg):
		try:
			#print(msg)
			#print(self.is_set_categoria, self.is_set_location)
			content_type, chat_type, chat_id = telepot.glance(msg)
			
			if not self.Utils_obj.is_user_just_in_db(chat_id):	self.Utils_obj.registerAnUser(chat_id)
			print(self.Utils_obj.user_has_done(chat_id))
			# Per ora si gestisce solo l'accesso al bot in un gruppo o supergruppo
			if 'chat' in msg and 'group' in chat_type and not self.Utils_obj.user_has_done(chat_id):
				# se supergruppo passo come descrizione l'username del gruppo
				if chat_type == 'supergroup':
					self.is_super_group_flag = True
					self.username = msg['chat']['username']

				(first_name, group_title) = (msg['from']['first_name'], msg['chat']['title'])
				self.group_title = group_title
				if not self.is_set_location or not self.is_set_categoria:
					
					# Si tratta di messaggio testuale
					if content_type == 'text':
						chat_message = msg['text']
						# hai premuto uno dei bottoni della tastiera principale
						if chat_message in [j for i in self.main_keyboard for j in i]:
							self.main_keyboard_handler(chat_id, chat_message)
						elif self.location_error_step == 1:
							try:
								address , city , postcode = chat_message.split(',')
								self.Utils_obj.post_shop_details(self.group_title, self.added_categories, self.webSiteName,self.username,address = address, city = city, postcode = postcode)
								toSend = "Tutto impostato con successo:\nCategorie del negozio: *" + str(self.added_categories) + "*\nPosizione del negozio: *" + str(chat_message) + "*."
								self.bot.sendMessage(chat_id, text= toSend, reply_markup = ReplyKeyboardRemove(),parse_mode= 'Markdown')
								self.resetAllVariables()
								self.Utils_obj.stop_user(chat_id)
								self.location_error_step = 0
							except:
								self.bot.sendMessage(chat_id, text= self.location_error_message, reply_markup = ReplyKeyboardRemove(),parse_mode= 'Markdown')
								self.location_error_step = 1
						elif chat_message in [j for i in self.yes_no_keyboard for j in i] and self.webSiteStep == 1:
							if chat_message == self.yes_button:
								self.webSiteStep = 2
								self.bot.sendMessage(chat_id, text="Inserisci il link al tuo sito web", reply_markup = ReplyKeyboardRemove(),parse_mode= 'Markdown')
							else:
								self.bot.sendMessage(chat_id, text = self.description_message, reply_markup={'keyboard': self.main_keyboard}, parse_mode = 'Markdown')
								self.webSiteStep = 0
						elif self.webSiteStep == 2:
							self.webSiteName = chat_message
							self.bot.sendMessage(chat_id, text = "*Sito Web impostato con successo*\n"+self.description_message, reply_markup={'keyboard': self.main_keyboard}, parse_mode = 'Markdown')
							self.webSiteStep = 0
						elif chat_message in [j for i in self.yes_no_keyboard for j in i]:
							self.yes_no_handler(chat_id, chat_message)
						elif chat_message in [j for i in self.categories_keyboard for j in i]:
							self.category_handler(chat_id, chat_message)
						else:
							self.bot.sendMessage(chat_id, text=self.main_message, reply_markup={'keyboard': self.main_keyboard},parse_mode= 'Markdown')

					# mi hai inviato la posizione
					elif content_type == 'location' and self.i_can_send_location and not self.is_set_location:
						self.location_handler(chat_id, msg)
						self.i_can_send_location = False
					#  Messaggio di benvenuto appena si accede al bot
					elif content_type == 'group_chat_created':
						self.send_welcome_message(chat_id, first_name, group_title)
					elif content_type == 'new_chat_member':	pass
					elif content_type == 'new_chat_photo':	pass

					#  Per qualsiasi altro caso inviami la tastiera principale
					else:
						self.bot.sendMessage(chat_id, text=self.main_message, reply_markup={'keyboard': self.main_keyboard},parse_mode= 'Markdown')

				elif self.is_set_categoria and self.is_set_location:
					lat, lng = self.myLocation
					status_code = self.Utils_obj.post_shop_details(self.group_title, self.added_categories, self.webSiteName,self.username, lat, lng)
					if status_code == 200: 
						toSend = "Tutto impostato con successo:\nCategorie del negozio: *" + str(self.added_categories) + "*\nPosizione del negozio: *" + str(self.myLocation) + "*."
						self.bot.sendMessage(chat_id, text= toSend, reply_markup = ReplyKeyboardRemove(),parse_mode= 'Markdown')
						self.resetAllVariables()
						self.Utils_obj.stop_user(chat_id)
					else:
						self.bot.sendMessage(chat_id, text= self.location_error_message, reply_markup = ReplyKeyboardRemove(),parse_mode= 'Markdown')
						self.location_error_step = 1
				
				
		except telepot.exception.BotWasKickedError as e:
			print("Sei stato buttato fuori dal gruppo")
		except Exception as e:
			if "No suggested keys" in str(e):	pass
			elif "title" in str(e):	pass
			elif 'supergroup' in str(e):	pass
			print("Eccezione non gestita: " + str(e))

	def main(self):
		print("In Loop...")
		MessageLoop(self.bot, self.main_handler).run_as_thread()
		
		while True:	time.sleep(1)



if __name__ == '__main__':
	Bot = Bot()
	Bot.main()



