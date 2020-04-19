import requests, json

class Utility(object):
	def __init__(self):
		self.base_request_url = "https://api.colligo.shop/"

	#---------[CATEGORIES FUNCTIONS]---------
	def retrieve_merchant_categories(self):
		url = self.base_request_url + '/categories'
		response = requests.get(url = url)
		return response.json()

	def get_all_merchant_categories(self):
		#json_content = self.retrieve_merchant_categories()
		return ["Altro", "Pescivendolo", "Macelleria", "Salumenria", "Dio", "Porco"] #[item['name'] for item in json_content]

	def from_category_name_to_ids(self, categoriesNamesList):
		toRet = []
		for item in self.retrieveMerchantCategories():
			if item['name'] in categoriesNamesList:	toRet.append(item['id'])
		return list(set(toRet))
	#---------[END CATEGORIES FUNCTIONS]---------
	
	def set_user_data(self, chat_id, context,main_keyboard):
		if not chat_id in context.user_data:
			context.user_data[chat_id] = {"main_keyboard":main_keyboard, 
			"is_set_location":False, 
			"is_set_categories":False, 
			"categories_list":[],
			"tmp_category":None,
			"user_location":(None, None), 
			"user_website":""}

	def get_user_data(self, chat_id, context):
		return context.user_data[chat_id]

	def get_main_keyboard_by_chat_id(self, chat_id, context):
		return context.user_data[chat_id]['main_keyboard']
	def set_main_keyboard_by_chat_id(self, chat_id, main_keyboard, context):
		context.user_data[chat_id]['main_keyboard'] = main_keyboard

	def get_user_categories(self, chat_id, context):
		return context.user_data[chat_id]['categories_list']
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

