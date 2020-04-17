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
		json_content = self.retrieve_merchant_categories()
		return [item['name'] for item in json_content]

	def from_category_name_to_ids(self, categoriesNamesList):
		toRet = []
		for item in self.retrieveMerchantCategories():
			if item['name'] in categoriesNamesList:	toRet.append(item['id'])
		return list(set(toRet))
	#---------[END CATEGORIES FUNCTIONS]---------
	