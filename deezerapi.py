# -*-coding:UTF-8 -*
# Auteur : AlzoxX76
# Date : 12/11/2018
# Version : 0.5

import requests
import json


URLcookies = "http://www.deezer.com"
URLlogin = "http://www.deezer.com//ajax/action.php"



def getMethodUrlWithToken(method, token=""):
	return "http://www.deezer.com/ajax/gw-light.php?method=" + method + "&input=3&api_version=1.0&api_token=" + token

def loginTest(email, mdp, proxy=dict()):
	r = requests.post(URLlogin, data=dict(type="login", mail=email, password=mdp), proxies=proxy, timeout=5)
	if r.text != "error" and r.text != "success":
		raise Exception("Unknow return value for login")
	if r.text == "success":
		return True
	return False

class DeezerClient:

	def __init__(self):
		return
		

	def login(self, email, mdp, proxy=dict()):
		self.reset()
		r = self.client.post(getMethodUrlWithToken("deezer.getUserData"), proxies=proxy, timeout=5) # Get user data (API token)
		try:
			self.checkFormLogin = json.loads(r.text)['results']["checkFormLogin"]
		except:
			pass
		r = self.client.post(URLlogin, data=dict(type="login", mail=email, password=mdp, checkFormLogin=self.checkFormLogin), cookies=self.client.cookies, proxies=proxy, timeout=2)

		if r.text != "error" and r.text != "success":
			raise Exception("Unknow return value for login")
		if r.text == "success":
			self.getDeezerApiToken()
			self.password = mdp
			return True
		return False

	def getDeezerApiToken(self):
		r = self.client.post(getMethodUrlWithToken("deezer.getUserData"), cookies=self.client.cookies) # Get user data (API token)

		userInfo = json.loads(r.text)['results']


		self.deezerAPITOKEN = userInfo['checkForm'] # checkForm key is the API key

	def reset(self):

		self.client = requests.session() # Create session

		self.password = "" # Reset password

		self.client.get(URLcookies) # Get cookies for session

		r = self.client.post(getMethodUrlWithToken("deezer.getUserData"), cookies=self.client.cookies) # Get user data (API token)

		userInfo = json.loads(r.text)['results']


		self.deezerAPITOKEN = userInfo['checkForm'] # checkForm key is the API key

	def getMethodDeezerAPI(self, method, dataRequest=str(), proxy=dict()):
		return self.client.post(getMethodUrlWithToken(method, self.deezerAPITOKEN), data=dataRequest, cookies=self.client.cookies, proxies=proxy, timeout=2) # Deezer API request

	def changePassword(self, newpassword):
		response = self.getMethodDeezerAPI("deezer.updatePassword", json.dumps({"old_password":self.password, "password":newpassword}))
		if json.loads(response.text)["results"]:
			self.password = newpassword
			return True
		return False



if __name__ == "__main__":
	test = DeezerClient()
	email = input("EMAIL : ")
	mdp = input("MDP : ")
	if test.login(email, mdp):
		print("success")
		print(test.changePassword(input("new password : ")))
	else:
		print("error")
	input()
