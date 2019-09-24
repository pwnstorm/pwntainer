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

	def login(self, password):
		username = 'admin'
		data = {
				"username": username,
				"password": password
			}
		
		#print("[*] Attempting to login as %s ===> %s" %(username, password))
		jwt = requests.post(self.host+"/auth", data=json.dumps(data)).json()
		if "jwt" in jwt.keys():
			self.jwt_token = jwt['jwt']
			return "success"

		elif "err" in jwt.keys():
			return "failed"
		else:
			print("[-] An unknown error occured!")

	def get_jwt(self):
		return self.jwt_token

"""
	def bruteforce(self, pw_list)
"""