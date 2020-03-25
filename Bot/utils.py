import json

class Utils(object):
	def __init__(self):
		self.root_file_folder = "files/"
		self.settings_file_name = self.root_file_folder + "settings.json"

		self.merchats_file_name = self.root_file_folder + "merchants.json"


	def getContentOfFile(self, filename):	
		file = open(filename)
		content = json.loads(file.read())
		file.close()
		return content

	def getToken(self):
		return self.getContentOfFile(self.settings_file_name)['botToken']

	""" Ritorna una lista di tutte le categorie di negozio"""
	def getAllMerchantCategories(self):
		return self.getContentOfFile(self.merchats_file_name)['availableCategories']

	

if __name__ == '__main__':
	Utils = Utils()
	print(Utils.getAllMerchantCategories())