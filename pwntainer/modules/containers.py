import requests
from pprint import pprint
import json

class Containers(object):
	"""
	Defines the remote container objects
	"""
	def __init__(self, host, endp):
	 	self.headers = {"Authorization": 'Bearer '+ open("./data/auth.token").read()}
	 	self.docker_endp = "http://"+host+"/api/endpoints/"+str(endp)

	def list_containers(self):
		containers = requests.get(self.docker_endp+"/docker/containers/json", headers=self.headers).json()
		pprint(containers)
		return containers

	