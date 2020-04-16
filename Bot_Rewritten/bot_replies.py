from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode, ChatAction, MessageEntity, Bot
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters, PicklePersistence, PrefixHandler, CallbackQueryHandler

import re, os, requests, sys, time, json

from datetime import datetime




BOT_TOKEN = "990488789:AAFwcnMKXMwJd-GnwSgryCWwZome0Ebz1XQ"
Bot_Obj = Bot(BOT_TOKEN)

#---------[Some Strings]---------
bot_replies = {
	"main_message": "*Utilizza la tastiera sottostante*",
	"category_message" : "Seleziona a quale categoria appartiene il tuo negozio.(Max 3)\n*[Premere il pulsante Fine per terminare la selezione]*",
	"position_message": "Inviami la posizione(clicca sulla spilla e seleziona *Posizione*, quindi seleziona *Invia posizione corrente*)",

	"category_error_message": "*Inserire almeno una tra le categorie elencate*",
	"registration_error_message": "*Qualcosa è andato storto con la registrazione del tuo negozio\nRicominciamo la registrazione dall'inizio.*",
	"location_error_message" : "Non è stato possibile salvare la posizione del tuo negozio.\nInseriscila manualmente attenendoti al seguente formato: *via*, *CAP*, *città*.\nEsempio: *Via corcolle 30, 00131, Roma*",
	
	"description_message": "*Attraverso i pannelli sottostanti potrai selezionare le categorie che descrivono il tuo negozio e condividere la tua posizione con i clienti.*",
	"dealer_welcome_message": "Benvenuto *%s*  del negozio *%s* sono ColliGo, il bot che ti accompagnerà nella vendita online della tua attività.\nHai un sito web del negozio?",

	"catagories_done": "Ecco le categorie che hai impostato\n*%s*",
	"catagory_added": "Categoria *%s* aggiunta con successo.\n*[Premere il pulsante Fine per terminare la selezione]*",
	"category_yes_no": "Sei sicuro di voler aggiungere la categoria *%s*?",

	"location_done": "Posizione Registrata: *[%s, %s]*",
	"website_added": "*Sito Web %s impostato con successo*\n",


	"all_done": "Tutto impostato con successo:\nCategorie del negozio: *%s*\nPosizione del negozio: *%s*.",

	"no_access_here": "*Mi dispiace ma il bot può essere utilizzato solamente all'interno di gruppi o supergruppi*"

}


#---------[Keyboard Buttons]---------
bot_buttons = {
	"category": "🥐 Categoria 🍷",
	"location": "📍 Posizione 📍",

	"yes": "👍 SI 👍",
	"no": "👎 NO 👎",
}

main_keyboard = ReplyKeyboardMarkup([
	[bot_buttons['category']],
	[bot_buttons['location']]
])

yes_no_keyboard = ReplyKeyboardMarkup([
	[bot_buttons['yes']],
	[bot_buttons['no']]
])

#---------[Useful Functions]---------
def unknown_function(update, context):
	try:
		first_name = update.message.chat.first_name
		group_title = update.message.chat.title
		if 'group' in update.message.chat.type:
			context.bot.send_message(chat_id=update.effective_chat.id, text = bot_replies['dealer_welcome_message'] % (first_name, group_title), reply_markup=main_keyboard,  parse_mode = ParseMode.MARKDOWN)
		else:
			context.bot.send_message(chat_id=update.effective_chat.id, text = bot_replies['no_access_here'], reply_markup=ReplyKeyboardRemove(),  parse_mode = ParseMode.MARKDOWN)
		context.user_data.clear()
	except Exception as e:print(str(e))
	return ConversationHandler.END

def debug(con=None):
	message = "Sono qui con " + str(con) if con != None else "Sono qui"
	os.system("echo " + message)

def makeAKeyboard(self,alist, parti):
    length = len(alist)
    keyboard =  [alist[i*length // parti: (i+1)*length // parti] for i in range(parti)]
    keyboard.append([self.stop_button])
    return keyboard