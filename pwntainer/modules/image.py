import requests
from pprint import pprint
import json

class Image(object):
	"""
	This object has got the behaviors of a docker image i.e. pulling an image and listing existing images
	"""
	
	def __init__(self, host, endp, token):
                self.bearer = 'Bearer {}'.format(token)
		self.headers = {"Authorization": self.bearer}
		self.docker_endp = "http://"+host+"/api/endpoints/"+str(endp)

	def list_images(self):
		images = requests.get(self.docker_endp+"/docker/images/json", headers=self.headers).json()
		return images

	def pull_image(self, image_name):
		data = {
			"fromImage": image_name
		}
		result = requests.post(self.docker_endp+"/docker/images/create", data=data, headers=self.headers)
		if result.status_code == 200:
			return "success"
		else:
			return "result.text"

	def remove_image(self, image_name):
		rmi = requests.delete(self.docker_endp+"/docker/images/"+image_name, headers=self.headers)
		if rmi.status_code == 200:
			print("success")
		elif rmi.status_code == 404:
			print("no such image")
		else:
			print(rmi.text)
