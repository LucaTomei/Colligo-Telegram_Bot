import requests, json, geopy
from geopy.geocoders import Nominatim
import googlemaps

class Utility(object):
	def __init__(self):
		self.base_request_url = "https://api.colligo.shop/"

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
	def set_user_data(self, chat_id, context, main_keyboard, telegram_link, group_title):
		if not chat_id in context.user_data:
			context.user_data[chat_id] = {
				"group_title": group_title,
				"telegram_link":telegram_link,
				"main_keyboard":main_keyboard, 
				"is_set_location":False, 
				"is_set_categories":False, 
				"categories_list":[],
				"tmp_category":None,
				"user_location":(None, None), 
				"user_website":""
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
	#---------[END CONTEXT_USER_DATA_HANDLERS]---------
	

	#---------[SAVING DATA TO BACKAND]---------
	
	def reverse_location(self, latitude, longitude):
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

	def post_shop_details(self, chat_id, context):
		context = {
			"group_title": "sono un bel gruppo1",
			"telegram_link":"https://t.me/joinchat/Q_pELBor7z2Txw5q5j-eOw",
			"main_keyboard":"main_keyboard", 
			"is_set_location":True, 
			"is_set_categories":True, 
			"categories_list":[151, 161, 131],
			"tmp_category":None,
			"user_location":(41.956258, 12.721122), 
			"user_website":""
		}

		latitude, longitude = context['user_location']
		(city, address, cap) = self.reverse_location(latitude, longitude)
		
		to_post = {'name':context['group_title'],
			"city":city ,
			"address": address, 
			"cap":cap,
			"description":context['group_title'], 
			"telegram":context['telegram_link'],
			'categories_ids': self.from_category_name_to_ids(context['categories_list']), 
			"accepts_terms_and_conditions":True
		}
		post_url = "http://localhost:5000/shops"#self.base_request_url + '/shops'
		response = requests.post(url = post_url, json = to_post)
		print(response.status_code, response.text)

	#---------[END SAVING DATA TO BACKAND]---------


if __name__ == '__main__':
	Utility_Obj = Utility()
	Utility_Obj.post_shop_details("1221", {})