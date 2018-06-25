# -*-coding:UTF-8 -*
# Auteur : AlzoxX76
# Date : 23/06/2018
# Version : 0.2

import requests
import json


URLcookies = "https://www.deezer.com"

def getMethodUrlWithToken(method, token=""):
	return "https://www.deezer.com/ajax/gw-light.php?method=" + method + "&input=3&api_version=1.0&api_token=" + token


class DeezerClient:

	def __init__(self):
		self.client = requests.session() # Create session

		self.client.get(URLcookies) # Get cookies for session

		# Save cookies
		self.sessionID = self.client.cookies['sid']
		self.deezerID = self.client.cookies['dzr_uniq_id']

		r = self.client.post(getMethodUrlWithToken("deezer.getUserData"), headers=self.createHeader()) # Get user data (API token)

		userInfo = json.loads(r.text)['results']


		self.deezerAPITOKEN = userInfo['checkForm'] # checkForm key is the API key

	def createHeader(self):
		return {"Cookie": "dzr_uniq_id=" + self.deezerID + "; sid=" + self.sessionID} # Create the header with the cookies info

	def getMethodDeezerAPI(self, method, dataRequest=str()):
		return self.client.post(getMethodUrlWithToken(method, self.deezerAPITOKEN), data=dataRequest, headers=self.createHeader()) # Deezer API request





if __name__ == "__main__":

	client = DeezerClient() # Create the deezer client

	searching = input("Searching for artist : ")

	dataRequest = json.dumps({"QUERY":searching, "TYPES":{"ARTIST":True}}) # Create the body request

	r = client.getMethodDeezerAPI("deezer.suggest", dataRequest) # Ask for suggest
	r = json.loads(r.text)['results'] # Convert in json
	print("Number of suggest : " + str(len(r['ARTIST']))) # Nb of suggest

	print("TOP : " + r['TOP_RESULT'][0]['ART_NAME']) # Top result

	# List all suggest
	for i in range(len(r['ARTIST'])):
		buf = r['ARTIST'][i]
		print(str(i) + " : " + buf['ART_NAME'])