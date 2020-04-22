import requests, json, geopy, googlemaps, re
from geopy.geocoders import Nominatim


class Utility(object):
	def __init__(self):
		self.base_request_url = "https://api.colligo.shop/"

	def is_really_a_website(self, url):
	    regex = re.compile(
	        r'^https?://'  # http:// or https://
	        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
	        r'localhost|'  # localhost...
	        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
	        r'(?::\d+)?'  # optional port
	        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
	    return url is not None and regex.search(url)
	#---------[CATEGORIES FUNCTIONS]---------
	def retrieve_merchant_categories(self):
		url = self.base_request_url + '/categories'
		response = requests.get(url = url)
		return response.json()
	
	def get_all_merchant_categories(self):
		json_content = self.retrieve_merchant_categories()
		return [item['name'] for item in json_content]

	def from_category_name_to_ids(self, categoriesNamesList):
		toRet = []
		for item in self.retrieve_merchant_categories():
			if item['name'] in categoriesNamesList:	toRet.append(item['id'])
		return list(set(toRet))

	def get_all_categories_ids(self, categoy_list):
		toRet = []
		for item in self.retrieve_merchant_categories():
			if item['name'] in categoy_list:	toRet.append(item['id'])
		return list(set(toRet))
	#---------[END CATEGORIES FUNCTIONS]---------
	

	#---------[CONTEXT_USER_DATA_HANDLERS]---------
	def set_user_data(self, chat_id, context, main_keyboard, group_title):
		if not chat_id in context.user_data:
			context.user_data[chat_id] = {
				"group_title": group_title,
				"telegram_link":'',
				"main_keyboard":main_keyboard, 
				"is_set_location":False, 
				"is_set_categories":False, 
				"categories_list":[],
				"tmp_category":None,
				"user_location":(None, None), 
				"user_website":"",
				"all_done":False
			}

	def get_user_data(self, chat_id, context):
		return context.user_data[chat_id]

	def get_main_keyboard_by_chat_id(self, chat_id, context):
		return context.user_data[chat_id]['main_keyboard']
	def set_main_keyboard_by_chat_id(self, chat_id, main_keyboard, context):
		context.user_data[chat_id]['main_keyboard'] = main_keyboard

	def get_user_categories(self, chat_id, context):
		return list(set(context.user_data[chat_id]['categories_list']))
	def set_user_category(self, chat_id, category, context):
		context.user_data[chat_id]['categories_list'].append(category)

	def get_tmp_category(self, chat_id, context):
		return context.user_data[chat_id]['tmp_category']
	def set_tmp_category(self, chat_id, category, context):
		context.user_data[chat_id]['tmp_category'] = category

	def get_telegram_link(self, context, chat_id):
		return context.user_data[chat_id]['telegram_link']

	def set_telegram_link(self, update, context):
		chat_id = update.message.chat.id
		telegram_link = ''
		if self.get_telegram_link(context, chat_id) == '':
			try:	telegram_link = context.user_data[chat_id]['telegram_link'] = context.bot.exportChatInviteLink(chat_id)
			except Exception as e:	pass
		return telegram_link



	def set_user_website(self, chat_id, website, context):
		context.user_data[chat_id]['user_website'] = website
	def get_user_website(self, chat_id, context):
		return context.user_data[chat_id]['user_website']


	def get_user_location(self, chat_id, context):	return context.user_data[chat_id]['user_location']
	def set_user_location(self, chat_id, tupla_location, context):
		context.user_data[chat_id]['user_location'] = tupla_location

	def set_location_done(self, chat_id, context):
		context.user_data[chat_id]['is_set_location'] = True
	def has_done_location(self, chat_id, context):	return context.user_data[chat_id]['is_set_location']


	def set_categories_done(self, chat_id, context):
		context.user_data[chat_id]['is_set_categories'] = True
	def has_done_categories(self, chat_id, context):	return context.user_data[chat_id]['is_set_categories']

	def remove_user_in_context(self, chat_id, context):
		del context.user_data[chat_id]


	def check_if_user_has_done(self, chat_id, context):
		return context.user_data[chat_id]['all_done']

	def set_all_done(self, chat_id, context):
		context.user_data[chat_id]['all_done'] = True
	#---------[END CONTEXT_USER_DATA_HANDLERS]---------
	

	#---------[SAVING DATA TO BACKAND]---------
	
	def reverse_location(self, latitude, longitude):
		try:
			api_key = 'AIzaSyANBKTnUtFUgYga3F-gzM6qwdNFaUul8Gg'
			geolocator = Nominatim(user_agent='ColliGoBot')
			gmaps = googlemaps.Client(key=api_key)
			reverse_geocode_result = gmaps.reverse_geocode((latitude, longitude)) #("22.5757344, 88.4048656")
			location = geolocator.reverse(str(latitude) + ',' + str(longitude))
			raw_location = location.raw['address']


			formatted_address = reverse_geocode_result[0]['formatted_address']
			tupla_location = (address, num_address, cap_and_city, country)  = formatted_address.split(',')
			address = address + " " + str(num_address)
			#print(tupla_location)
			cap = raw_location['postcode']
			#print(cap)
			
			try:	city = raw_location['town'].capitalize() if 'town' in raw_location else raw_location['village'].capitalize()
			except:	cyty = cap_and_city.split(' ')[1]

			return city, address, cap
		except:	return None, None, None

	def post_shop_details(self, chat_id, context):
		context_to_set = context
		context = context.user_data[chat_id]
		try:
			latitude, longitude = context['user_location']
			#print(latitude, longitude)
			(city, address, cap) = self.reverse_location(latitude, longitude)
		except:
			address, cap, city = context['user_location']

		to_post = {
				'name':context['group_title'],
				"city":city ,
				"address": address, 
				"cap":cap,
				"description":context['group_title'], 
				"telegram":context['telegram_link'] if context['telegram_link'] != '' else 'https://'+context['group_title'],
				'categories_ids': self.from_category_name_to_ids(context['categories_list']), 
				"accepts_terms_and_conditions":True
			}
		
		website = context['user_website']	# if you have a website
		if website != '':	to_post.update({'website':website})
		
		#print("to_post", to_post)
		post_url = self.base_request_url + '/shops' #"http://localhost:5000/shops" for test
		response = requests.post(url = post_url, json = to_post)
		#print(response.status_code, response.text)
		self.set_all_done(chat_id, context_to_set)
		return response.status_code

	#---------[END SAVING DATA TO BACKAND]---------


if __name__ == '__main__':
	Utility_Obj = Utility()
	Utility_Obj.post_shop_details("1221", {})