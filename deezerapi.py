# -*-coding:UTF-8 -*
# Auteur : AlzoxX76
# Date : 23/06/2018
# Version : 0.3

import requests
import json


URLcookies = "https://www.deezer.com"
URLlogin = "https://www.deezer.com//ajax/action.php"

def getMethodUrlWithToken(method, token=""):
	return "https://www.deezer.com/ajax/gw-light.php?method=" + method + "&input=3&api_version=1.0&api_token=" + token


class DeezerClient:

	def __init__(self):
		self.client = requests.session() # Create session

		self.client.get(URLcookies) # Get cookies for session

		r = self.client.post(getMethodUrlWithToken("deezer.getUserData"), cookies=self.client.cookies) # Get user data (API token)

		userInfo = json.loads(r.text)['results']


		self.deezerAPITOKEN = userInfo['checkForm'] # checkForm key is the API key

	def login(self, email, mdp):
		r = self.client.post(URLlogin, data=dict(type="login", mail=email, password=mdp), cookies=self.client.cookies)
		return r.text == "success"

	def getMethodDeezerAPI(self, method, dataRequest=str()):
		return self.client.post(getMethodUrlWithToken(method, self.deezerAPITOKEN), data=dataRequest, cookies=self.client.cookies) # Deezer API request





if __name__ == "__main__":

	client = DeezerClient() # Create the deezer client


	searching = input("Searching for artist : ")

	dataRequest = json.dumps({"QUERY":searching, "TYPES":{"ARTIST":True}}) # Create the body request

	r = client.getMethodDeezerAPI("deezer.suggest", dataRequest) # Ask for suggest
	r = json.loads(r.text)['results'] # Convert in json
	print("TOP : " + r['TOP_RESULT'][0]['ART_NAME']) # Top result

	# List all suggest
	for i in range(len(r['ARTIST'])):
		buf = r['ARTIST'][i]
		print(str(i) + " : " + buf['ART_NAME'])
