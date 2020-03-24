from telepot.loop import MessageLoop
import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove


from utils import Utils


class EasyCollect_Bot(object):
	def __init__(self):
		self.Utils_obj = Utils()
		self.bot_token = self.Utils_obj.getToken()
		self.bot = telepot.Bot(self.bot_token)
	

	def handler(self, msg):
		chat_id = msg['chat']['id']
		print(chat_id)



	def main(self):
		print("Bot in Loop...")
		MessageLoop(self.bot, self.handler).run_as_thread()

		while 1:
			time.sleep(1)



if __name__ == '__main__':
	botInstance = EasyCollect_Bot()
	botInstance.main()
		