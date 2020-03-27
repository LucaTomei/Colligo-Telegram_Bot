import json, requests
from geopy.geocoders import Nominatim
class Utils(object):
	def __init__(self):
		self.root_file_folder = "files/"
		self.settings_file_name = self.root_file_folder + "settings.json"

		self.db_file = self.root_file_folder + "db.json"

		self.base_request_url = "https://evening-plateau-32926.herokuapp.com"

	def is_user_just_in_db(self, chat_id):
		contentOfFile = self.getContentOfFile(self.db_file)['users']
		for item in contentOfFile:
			if item['chat_id'] == chat_id: return True
		return False

	def user_has_done(self, chat_id):
		contentOfFile = self.getContentOfFile(self.db_file)['users']
		for item in contentOfFile:
			if item['chat_id'] == chat_id and item['has_done'] == True:	return True
		return False

	def getIdxOfUserInFile(self, chat_id):
		contentOfFile = self.getContentOfFile(self.db_file)['users']
		for i in range(len(contentOfFile)):
			if contentOfFile[i]['chat_id'] == chat_id: return i
		return -1
	
	def stop_user(self, chat_id):
		contentOfFile = self.getContentOfFile(self.db_file)
		idx_of_user = self.getIdxOfUserInFile(chat_id)
		contentOfFile['users'][idx_of_user]['has_done'] = True
		self.write_json_file(self.db_file, contentOfFile)



	def registerAnUser(self, chat_id):
		contentOfFile = self.getContentOfFile(self.db_file)
		if not self.is_user_just_in_db(chat_id):
			contentOfFile['users'].append({"chat_id":chat_id, "has_done":False})
			self.write_json_file(self.db_file, contentOfFile)

	def write_json_file(self, filename, content):
		file = open(filename, 'w')
		json.dump(content, file, indent = 4)
		file.close()


	def getContentOfFile(self, filename):	
		file = open(filename)
		content = json.loads(file.read())
		file.close()
		return content

	def getToken(self):
		return self.getContentOfFile(self.settings_file_name)['botToken']

	""" Ritorna una lista di tutte le categorie di negozio"""

	def getAllMerchantCategories(self):
		json_content = self.retrieveMerchantCategories()
		return [item['name'] for item in json_content]

	def retrieveMerchantCategories(self):
		url = self.base_request_url + '/categories'
		response = requests.get(url = url)
		return response.json()

	def from_lat_lng_to_address(self, lat, lng):
		geolocator = Nominatim(user_agent="EasyCollectBot")
		lat_lng_str = str(lat) + "," + str(lng)
		location = geolocator.reverse(lat_lng_str)
		return location.address

	def from_category_name_to_ids(self, categoriesNamesList):
		toRet = []
		for item in self.retrieveMerchantCategories():
			if item['name'] in categoriesNamesList:	toRet.append(item['id'])
		print("Lista:", toRet)
		return list(set(toRet))

	def post_shop_details(self, group_title,lat, lng, categories, username = ''):
		if username == '':	username = group_title
		url = self.base_request_url + '/shops'
		to_post = {'name':group_title + "_" + str(lat) + "_" + str(lng), "address":self.from_lat_lng_to_address(lat, lng), "description":group_title, "telegram":"@"+username, 'categories_ids': self.from_category_name_to_ids(categories)}
		response = requests.post(url = url, data = to_post)
		print(response.json())
		return response.status_code


if __name__ == '__main__':
	Utils = Utils()
	
	lat = 41.8814
	lng = 12.5669
	address = Utils.from_lat_lng_to_address(lat, lng)


	categories = ['Alimentari']
	print(Utils.from_category_name_to_ids(categories))
	# group_title = "test124_"+str(lat) +"_" + str(lng)
	# categories = [{
 #            "id":81,
 #            "natural_key":"formaggeria",
 #            "name":"Formaggeria"
 #         },
 #         {
 #            "id":151,
 #            "natural_key":"alimentari",
 #            "name":"Alimentari"
 #         }]
	# Utils.post_shop_details(group_title, lat, lng, address,categories)
