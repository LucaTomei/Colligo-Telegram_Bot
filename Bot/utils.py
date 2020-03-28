import json, requests
from geopy.geocoders import Nominatim
class Utils(object):
	def __init__(self):
		self.root_file_folder = "files/"
		self.settings_file_name = self.root_file_folder + "settings.json"

		self.db_file = self.root_file_folder + "db.json"

		self.base_request_url = "https://boiling-beyond-07880.herokuapp.com/"

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
		url = 'https://geocode.xyz/'+str(lat) + ','+ str(lng) + '?geoit=json'
		raw_location = requests.get(url).json()
		if 'alt' in raw_location:
			city = raw_location['city'].capitalize()
			address = raw_location['alt']['loc'][0]['staddress'] + " " + raw_location['alt']['loc'][0]['stnumber']
			postcode =  raw_location['alt']['loc'][0]['postal']
		else:
			geolocator = Nominatim(user_agent='ColliGoBot')
			location = geolocator.reverse(str(lat) + ',' + str(lng))
			raw_location = location.raw['address']
			print(raw_location)
			if 'town' in raw_location:
				city = raw_location['town'].capitalize()
				address = raw_location['road']
				postcode =  raw_location['postcode']
		return (city, address, str(postcode))

	def from_category_name_to_ids(self, categoriesNamesList):
		toRet = []
		for item in self.retrieveMerchantCategories():
			if item['name'] in categoriesNamesList:	toRet.append(item['id'])
		print("Lista:", toRet)
		return list(set(toRet))

	def post_shop_details(self, group_title,lat, lng, categories, website,username = ''):
		if username == '':	username = group_title
		url = self.base_request_url + '/shops'
		(city, address, postcode) = self.from_lat_lng_to_address(lat, lng)
		if website == '':
			to_post = {'name':group_title + "_" + str(lat) + "_" + str(lng),"city":city ,"address": address, "cap":postcode,"description":group_title, "telegram":"@"+username,'categories_ids': self.from_category_name_to_ids(categories)}
		else:
			to_post = {'name':group_title + "_" + str(lat) + "_" + str(lng),"city":city ,"address": address, "cap":postcode,"description":group_title, "telegram":"@"+username, "website":website,'categories_ids': self.from_category_name_to_ids(categories)}
		print(to_post)
		response = requests.post(url = url, json = to_post)
		#print(response.json(), response.status_code)
		return response.status_code


if __name__ == '__main__':
	Utils = Utils()
	lat, lng = (40.504873, 15.415253)
	lat, lng = (41.956221, 12.721205)	#casa
	lat, lng = (42.106315, 12.175018)
	x = Utils.from_lat_lng_to_address(lat, lng)
	print(x)
