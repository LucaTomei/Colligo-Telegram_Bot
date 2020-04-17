from bot_replies import *

class Bot(object):
	def __init__(self):
		pass

	def start(self, update, context):
		first_name = update.message.chat.first_name
		group_title = update.message.chat.title
		if 'group' in update.message.chat.type:
			context.bot.send_message(chat_id=update.effective_chat.id, text = bot_replies['dealer_welcome_message'] % (first_name, group_title), reply_markup=yes_no_keyboard,  parse_mode = ParseMode.MARKDOWN)
		else:
			context.bot.send_message(chat_id=update.effective_chat.id, text = bot_replies['no_access_here'], reply_markup=ReplyKeyboardRemove(),  parse_mode = ParseMode.MARKDOWN)
		

	#---------[Check if bot was added to a group or supergroup or to a channel]---------
	def status_update(self, update, context):
		if update.message.group_chat_created or update.message.supergroup_chat_created or update.message.channel_chat_created:
			return self.start(update, context)
		else:
			return unknown_function(update, context)
		

	#---------[You have pressed YES WEBSITE BUTTON]---------
	def you_have_website(self, update, context):
		update.message.reply_text(bot_replies['insert_website'], parse_mode=ParseMode.MARKDOWN, reply_markup=ReplyKeyboardRemove(), disable_web_page_preview=True)
		return 1
	
	def register_website_handler(self, update, context):
		context.user_data['website'] = update.message.text 	# Save user website in user_data
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
		update.message.reply_text("Sono qui con " + update.message.text, parse_mode=ParseMode.MARKDOWN, reply_markup=categories_keyboard, disable_web_page_preview=True)
		pass


	def location_main_handler(self, update, context):
		pass
	
	def main_conversation_handler(self):
		main_conversation_handler = ConversationHandler(
            [	# Entry Points
            	MessageHandler(Filters.regex('^' + bot_buttons['category'] +'$'),self.category_main_handler),
            	MessageHandler(Filters.regex('^' + bot_buttons['location'] +'$'),self.location_main_handler),
        		MessageHandler(Filters.text,unknown_function),
            ], 
            {
            	0: [	# Starting main handler
            		# Bisogna verificare anche la pressione del tasto fine e quindi se ha inserito almeno una categoria
            		MessageHandler(Filters.text, self.filter_categories_handler),
            	],
            	
            	# 1:[
            	# 	PrefixHandler(bot_buttons['back'][0], bot_buttons['back'][1:], self.downloader_main_handler),
            	# 	MessageHandler(Filters.regex('^' + bot_buttons['top_chart'] +'$'),self.download_chart_handler),
            	# 	MessageHandler(Filters.regex('^' + bot_buttons['single_track'] +'$'),self.search_for_result_handler),
            	# 	MessageHandler(Filters.regex('^' + bot_buttons['playlist'] +'$'),self.search_for_result_handler),
            	# 	MessageHandler(Filters.regex('^' + bot_buttons['album'] +'$'),self.search_for_result_handler),
            	# 	MessageHandler(Filters.text,self.downloader_main_handler)
            	# ],
            	# 2:[
            	# 	PrefixHandler(bot_buttons['back'][0], bot_buttons['back'][1:], self.back_to_music_menu),
            	# 	MessageHandler(Filters.text,self.chart_downloader_handler)
            	# ],
            	# 3: [
            	# 	MessageHandler(Filters.text,self.choice_track_handler)
            	# ],
            	# 4: [
            	# 	PrefixHandler(bot_buttons['back'][0], bot_buttons['back'][1:], self.back_to_music_menu),
            	# 	MessageHandler(Filters.text,self.download_track_album_playlist_handler)
            	# ]            	
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
		dp.add_handler(MessageHandler(Filters.status_update, self.status_update))
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