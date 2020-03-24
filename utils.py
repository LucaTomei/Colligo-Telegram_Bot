import json

class Utils(object):
	def __init__(self):
		self.settings_file_name = "settings.json"


	def getContentOfSettings(self):	
		file = open(self.settings_file_name)
		content = json.loads(file.read())
		file.close()
		return content

	def getToken(self):	return self.getContentOfSettings()['botToken']
