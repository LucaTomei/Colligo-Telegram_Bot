import json, requests, telepot, time
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove

from utils import Utils

class TeleBot(object):
	def __init__(self):	
		self.Utils_obj = Utils()
		self.bot_token = self.Utils_obj.getToken()	# contiene il token del bot

		self.bot = telepot.Bot(self.bot_token)

		self.main_keyboard = [["Categoria"],["Posizione"]]
		categories_list = self.Utils_obj.getAllMerchantCategories()
		self.categories_keyboard = self.makeAKeyboard(categories_list, 6)


		self.base_step = 0

		self.is_set_categoria = False
		self.is_set_location = False

		
	def makeAKeyboard(self,alist, parti):
	    length = len(alist)
	    keyboard =  [alist[i*length // parti: (i+1)*length // parti] for i in range(parti)]
	    keyboard.append(["Altra Categoria"])
	    return keyboard


	def main_handler(self, msg):
		try:
			content_type, chat_type, chat_id = telepot.glance(msg)
			print(content_type)
			chat_id = msg['chat']['id']
			first_name = msg['from']['first_name']
			last_name = msg['from']['last_name']
			group_title = msg['chat']['title']
			if 'chat' in msg and 'group' in chat_type:	# si tratta di un commerciante che è in un gruppo
				if content_type == 'text':
					chat_message = msg['text']
					if chat_message == 'Categoria':
						toSend = "Inserisci la categoria di negozio che più ti si addice"
						self.bot.sendMessage(chat_id, text=toSend, reply_markup={'keyboard': self.categories_keyboard},parse_mode= 'Markdown')
					elif chat_message in [j for i in self.categories_keyboard for j in i]:
						if chat_message == "Altra Categoria":
							self.bot.sendMessage(chat_id, text="Inserisci la categoria a cui appartieni", reply_markup = ReplyKeyboardRemove(),parse_mode= 'Markdown')
							self.base_step = 1
						else:
							self.bot.sendMessage(chat_id, text="Ok, registro la tua categoria di " + chat_message, reply_markup={'keyboard': self.main_keyboard},parse_mode= 'Markdown')
							self.base_step = 0
							self.is_set_categoria = True
					elif self.base_step == 1:
						self.bot.sendMessage(chat_id, text="Ok, registro la tua categoria di " + chat_message, reply_markup={'keyboard': self.main_keyboard},parse_mode= 'Markdown')
						self.base_step = 0	
					elif chat_message == "Posizione":
						self.bot.sendMessage(chat_id, text="Inviami la posizione",parse_mode= 'Markdown', reply_markup = ReplyKeyboardRemove())
					elif self.is_set_categoria and self.is_set_location:
						self.bot.sendMessage(chat_id, text="Tutto settato, non devi fare nient'altro", reply_markup = ReplyKeyboardRemove())
					else:
						toSend = "Utilizza la tastiera sottostante"
						self.bot.sendMessage(chat_id, text=toSend, reply_markup={'keyboard': self.main_keyboard},parse_mode= 'Markdown')
				elif content_type == 'location':
					location = (latitude, longitude) = (msg['location']['latitude'], msg['location']['longitude'])
					toSend = "Posizione Inviata: [" + str(latitude) + ", " + str(longitude) + "]"
					self.bot.sendMessage(chat_id, text=toSend,parse_mode= 'Markdown', reply_markup={'keyboard': self.main_keyboard})
					self.is_set_location = True
			if content_type == 'new_chat_member':	# Messaggio di benvenuto appena si accede al bot
				toSend = "Ciao " + first_name + " " + last_name + " del gruppo " + group_title + " utilizza la tastiera sottostante per eseguire le azioni sul bot"
				self.bot.sendMessage(chat_id, text=toSend, reply_markup={'keyboard': self.main_keyboard},parse_mode= 'Markdown')
		except telepot.exception.BotWasKickedError as e:
			print("Sei stato buttato fuori dal gruppo")
		except Exception as e:
			if "No suggested keys" in str(e):
				chat_id = msg['id']
				print(msg)
				#self.bot.sendMessage(chat_id, text="ciao" )
			elif 'from' in str(e):	# test in canale
				print(msg)
			else:
				print("Eccezione non gestita: "  + str(e))
			
			


	def main(self):
		MessageLoop(self.bot, self.main_handler).run_as_thread()
		
		while True:	time.sleep(1)


if __name__ == '__main__':
	TeleBotOBJ = TeleBot()
	TeleBotOBJ.main()