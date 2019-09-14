from multiprocessing import Pool
import requests
import json


class Auth(object):
	"""
	This class represets various authentication mechanisms i.e. login with provided credentials, bruteforce or network sniffer
	"""
	def __init__(self, host):
		self.host = "http://"+host+"/api"
		self.username = ""
		self.password = ""
		self.jwt_token = ""

	def login(self, username, password):
		data = {
				"username": username,
				"password": password
			}
		
		jwt = requests.post(self.host+"/auth", data=json.dumps(data)).json()['jwt']
		self.jwt_token = jwt
		print(jwt)
