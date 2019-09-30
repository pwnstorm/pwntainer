import requests
from pprint import pprint
import json

class Containers(object):
	"""
	Defines the remote container objects
	"""
	def __init__(self, host, endp):
	 	self.headers = {"Authorization": 'Bearer '+ open("./data/auth.token").read(), "Content-Type": "application/json"}
	 	self.docker_endp = "http://"+host+"/api/endpoints/"+str(endp)
	 	self.name = "eviltainer"

	def list_containers(self):
		containers = requests.get(self.docker_endp+"/docker/containers/json", headers=self.headers).json()
		return containers

	def create_container(self, name, mnt_array):
		vol = {}
		for v in mnt_array:
			vol.update({v.split(":")[0]: {}})
		pwntainer = {
			"Cmd": ["/bin/bash", "-c", "sleep 3000"],
			"OpenStdin": True,
			"Tty": True,
			"Image":"ubuntu:18.04",
			"Volumes": vol,
			"HostConfig": {
				"Binds": mnt_array,
				"AutoRemove": False
			}
		}

		new_container = requests.post(self.docker_endp+"/docker/containers/create?name="+name, data=json.dumps(pwntainer), headers=self.headers)
		pprint(new_container.json())

	def start_container(self):
		s_container = requests.post(self.docker_endp+"/docker/containers/"+self.name+"/start", headers=self.headers).text
		return True