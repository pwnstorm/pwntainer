import requests
from pprint import pprint
import json

class Containers(object):
	"""
	Defines the remote container objects
	"""
	def __init__(self, host, endp, token):
		self.bearer = 'Bearer {}'.format(token)
	 	self.headers = {"Authorization": self.bearer,  "Content-Type": "application/json"}
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
			"Image":"sethmwabe/pwntainer",
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

	def exec_cmd(self, cmd):
		command = {
			"AttachStdin": True,
			"AttachStdout": True,
			"AttachStderr": True,
			"Tty": True,
			"Cmd": cmd,
		}

		exc_cmd = requests.post(self.docker_endp+"/docker/containers/"+self.name+"/exec", data=json.dumps(command), headers=self.headers)
		print(exc_cmd.status_code)
		print(exc_cmd.text)
		self.start_exec_cmd(exc_cmd.json()['Id'])

	def start_exec_cmd(self, cmd_instance_id):
		cmd = requests.post(self.docker_endp+"/docker/exec/"+str(cmd_instance_id)+"/start", data=json.dumps({"Detach":False, "Tty":True}), headers=self.headers)
		print(cmd.status_code)
		print(cmd.text)