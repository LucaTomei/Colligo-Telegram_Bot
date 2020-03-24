from telepot.loop import MessageLoop
import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove


from utils import Utils


class EasyCollect_Bot(object):
	def __init__(self):
		self.Utils_obj = Utils()
		self.bot_token = self.Utils_obj.getToken()
		



if __name__ == '__main__':
	EasyCollect_Bot_OBJ = EasyCollect_Bot()

		