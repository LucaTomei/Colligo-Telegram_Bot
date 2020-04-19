from bot_replies import *


class Bot(object):
	def __init__(self):
		pass


	def start(self, update, context):
		chat_id = update.message.chat_id
		Utility_Obj.set_user_data(chat_id, context,main_keyboard)
		first_name = update.message.chat.first_name
		first_name = first_name if first_name != None else update.message.from_user.first_name
		group_title = update.message.chat.title
		if 'group' in update.message.chat.type:
			context.bot.send_message(chat_id=update.effective_chat.id, text = bot_replies['dealer_welcome_message'] % (first_name, group_title), reply_markup=yes_no_keyboard,  parse_mode = ParseMode.MARKDOWN)
		else:
			context.bot.send_message(chat_id=update.effective_chat.id, text = bot_replies['no_access_here'], reply_markup=ReplyKeyboardRemove(),  parse_mode = ParseMode.MARKDOWN)
	
		

	#---------[You have pressed YES WEBSITE BUTTON]---------
	def you_have_website(self, update, context):
		update.message.reply_text(bot_replies['insert_website'], parse_mode=ParseMode.MARKDOWN, reply_markup=ReplyKeyboardRemove(), disable_web_page_preview=True)
		return 1
	
	def register_website_handler(self, update, context):
		chat_id = update.message.chat_id
		Utility_Obj.set_user_website(chat_id, update.message.text, context)	# Save user website in user_data
		update.message.reply_text(bot_replies['website_added'] % (update.message.text), parse_mode=ParseMode.MARKDOWN, reply_markup=main_keyboard, disable_web_page_preview=True)
		update.message.reply_text(bot_replies['description_message'], parse_mode=ParseMode.MARKDOWN, reply_markup=main_keyboard, disable_web_page_preview=True)
		return ConversationHandler.END


	#---------[You have pressed NO WEBSITE BUTTON]---------
	def yout_dont_have_website(self, update, context):	# if you don't have website return 2
		update.message.reply_text(bot_replies['description_message'], parse_mode=ParseMode.MARKDOWN, reply_markup=main_keyboard, disable_web_page_preview=True)
		return ConversationHandler.END


	def category_main_handler(self, update, context):
		update.message.reply_text(bot_replies['category_message'], parse_mode=ParseMode.MARKDOWN, reply_markup=categories_keyboard, disable_web_page_preview=True)
		return 0

	def filter_categories_handler(self, update, context):
		chat_message = update.message.text
		chat_id = update.message.chat_id
		user_categories = Utility_Obj.get_user_categories(chat_id, context)
		if len(user_categories) != 3:
			if chat_message in [j for i in categories_keyboard.keyboard for j in i]:
				Utility_Obj.set_tmp_category(update.message.chat_id, update.message.text, context)
				update.message.reply_text(bot_replies['category_yes_no'] % update.message.text, parse_mode=ParseMode.MARKDOWN, reply_markup=yes_no_categories_keyboard, disable_web_page_preview=True)
				return 1
			else:
				update.message.reply_text(bot_replies['category_error_message'], parse_mode=ParseMode.MARKDOWN, reply_markup=categories_keyboard, disable_web_page_preview=True)
				return 0
		else:
			if Utility_Obj.has_done_location(chat_id, context):
				Utility_Obj.set_main_keyboard_by_chat_id(chat_id, main_keyboard_empty, context)
			else:
				Utility_Obj.set_main_keyboard_by_chat_id(chat_id, main_keyboard_only_location, context)
			main_keyboard = Utility_Obj.get_main_keyboard_by_chat_id(chat_id, context)
			update.message.reply_text(bot_replies['catagories_done'] % (str(user_categories)), parse_mode=ParseMode.MARKDOWN, reply_markup=main_keyboard, disable_web_page_preview=True)
			return ConversationHandler.END


	def add_category_handler(self, update, context):
		chat_id = update.message.chat_id
		category = Utility_Obj.get_tmp_category(update.message.chat_id, context)
		Utility_Obj.set_user_category(chat_id, category, context)
		update.message.reply_text(bot_replies['catagory_added'] % category, parse_mode=ParseMode.MARKDOWN, reply_markup=categories_keyboard, disable_web_page_preview=True)
		return 0

	def check_user_categories_handler(self, update, context):
		chat_id = update.message.chat_id
		user_categories = Utility_Obj.get_user_categories(chat_id, context)
		if len(user_categories) != 0:
			if Utility_Obj.has_done_location(chat_id, context):
				Utility_Obj.set_main_keyboard_by_chat_id(chat_id, main_keyboard_empty, context)
			else:
				Utility_Obj.set_main_keyboard_by_chat_id(chat_id, main_keyboard_only_location, context)
			main_keyboard = Utility_Obj.get_main_keyboard_by_chat_id(chat_id, context)
			Utility_Obj.set_categories_done(chat_id, context)
			update.message.reply_text(bot_replies['catagories_done'] % str(user_categories), parse_mode=ParseMode.MARKDOWN, reply_markup=main_keyboard, disable_web_page_preview=True)
			if Utility_Obj.has_done_location(chat_id, context):
				user_location = Utility_Obj.get_user_location(chat_id, context)
				update.message.reply_text(bot_replies['all_done'] % (str(user_categories), str(user_location)), parse_mode=ParseMode.MARKDOWN, reply_markup=main_keyboard, disable_web_page_preview=True)
			return ConversationHandler.END
		else:
			update.message.reply_text(bot_replies['category_error_message'], parse_mode=ParseMode.MARKDOWN, reply_markup=categories_keyboard, disable_web_page_preview=True)
			return 0	

	def location_main_handler(self, update, context):
		update.message.reply_text(bot_replies['position_message'], parse_mode=ParseMode.MARKDOWN, reply_markup = ReplyKeyboardRemove(), disable_web_page_preview=True)
		return 2

	def set_user_location_handler(self, update, context):
		try:
			chat_id = update.message.chat_id
			location = update.message.location
			tupla_location = (latitude, longitude) = (location.latitude, location.longitude)
			Utility_Obj.set_user_location(chat_id, tupla_location, context)
			Utility_Obj.set_location_done(chat_id, context)

			if Utility_Obj.has_done_categories(chat_id, context):
				Utility_Obj.set_main_keyboard_by_chat_id(chat_id, main_keyboard_empty, context)
				user_categories = Utility_Obj.get_user_categories(chat_id, context)
				
				message_to_send = bot_replies['all_done'] % (str(user_categories), str(tupla_location))
			else:
				Utility_Obj.set_main_keyboard_by_chat_id(chat_id, main_keyboard_only_categories, context)
				message_to_send = bot_replies['main_message']
			main_keyboard = Utility_Obj.get_main_keyboard_by_chat_id(chat_id, context)
			
			update.message.reply_text(message_to_send, parse_mode=ParseMode.MARKDOWN, reply_markup = main_keyboard, disable_web_page_preview=True)
			return ConversationHandler.END
		except Exception as e:	print(str(e))
	
	def main_conversation_handler(self):
		main_conversation_handler = ConversationHandler(
            [	# Entry Points
            	MessageHandler(Filters.regex('^' + bot_buttons['category'] +'$'),self.category_main_handler),
            	MessageHandler(Filters.regex('^' + bot_buttons['location'] +'$'),self.location_main_handler),
        		MessageHandler(Filters.text,unknown_function),
            ], 
            {
            	0: [	# Starting main handler
            		MessageHandler(Filters.regex('^' + bot_buttons['stop_button'] +'$'), self.check_user_categories_handler),
            		MessageHandler(Filters.text, self.filter_categories_handler),
            	],
            	1: [	# category_yes_no
            		MessageHandler(Filters.regex('^' + bot_buttons['yes_category'] +'$'),self.add_category_handler),
            		MessageHandler(Filters.regex('^' + bot_buttons['no_category'] +'$'),self.category_main_handler),
            	],
            	2:[		# Location
            		MessageHandler(Filters.text,unknown_function),
            		MessageHandler(Filters.location,self.set_user_location_handler),
            	]      	
            },[])
		return main_conversation_handler



	def preamble_conversation_handler(self):
		preamble_conversation_handler = ConversationHandler(
            [	# Entry Points
            	MessageHandler(Filters.regex('^' + bot_buttons['yes'] +'$'),self.you_have_website),
            	MessageHandler(Filters.regex('^' + bot_buttons['no'] +'$'),self.yout_dont_have_website),
            ], 
            {
            	0:[	
            		MessageHandler(Filters.text,unknown_function),
            	],
            	1:[	# state for register website
            		MessageHandler(Filters.text,self.register_website_handler)
            	],         	
            },[])
		return preamble_conversation_handler

	
	def register_all_handlers(self, dp):
		dp.add_handler(CommandHandler('start', self.start))
		dp.add_handler(MessageHandler(Filters.status_update, self.start))
		dp.add_handler(self.preamble_conversation_handler())
		dp.add_handler(self.main_conversation_handler())
		dp.add_handler(MessageHandler(Filters.text, unknown_function))

	def main(self):
		updater = Updater(BOT_TOKEN,  use_context=True)
		dp = updater.dispatcher

		self.register_all_handlers(dp)
		
		print("In Loop")
		updater.start_polling()
		updater.idle()

if __name__ == '__main__':
	Bot().main()

#except Exception as e:print(str(e))