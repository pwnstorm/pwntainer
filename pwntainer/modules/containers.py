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
		return containers

	def create_container(self, name, mnt_array):
		pwntainer = {
			"AttachStdin": True,
			"AttachStdout": True,
			"AttachStderr": True,
			"Tty": True,
			"Image":"ubuntu:18.04",
			"Volumes": {
				"/etc/passwd": {} 
			},
			"HostConfig": {
				"Binds": mnt_array
			}
		}

		new_container = requests.post(self.docker_endp+"/docker/containers/create?name="+name, data=json.loads(str(pwntainer)), headers=self.headers)
		pprint(new_container.json())