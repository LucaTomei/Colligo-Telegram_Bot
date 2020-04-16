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
		update.message.reply_text("Hai un sito", parse_mode=ParseMode.MARKDOWN, reply_markup=main_keyboard, disable_web_page_preview=True)
		return 0

	#---------[You have pressed NO WEBSITE BUTTON]---------
	def yout_dont_have_website(self, update, context):
		update.message.reply_text("non hai un sito", parse_mode=ParseMode.MARKDOWN, reply_markup=main_keyboard, disable_web_page_preview=True)
		return 0

	def main_conversation_handler(self):
		main_conversation_handler = ConversationHandler(
            [	# Entry Points
            	MessageHandler(Filters.regex('^' + bot_buttons['yes'] +'$'),self.you_have_website),
            	MessageHandler(Filters.regex('^' + bot_buttons['no'] +'$'),self.yout_dont_have_website),
            ], 
            {
            	0:[
            		#PrefixHandler(bot_buttons['back'][0], bot_buttons['back'][1:], unknown_function),
            		MessageHandler(Filters.text,unknown_function),
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

	
	def register_all_handlers(self, dp):
		dp.add_handler(CommandHandler('start', self.start))
		dp.add_handler(MessageHandler(Filters.status_update, self.status_update))
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