import requests
from pprint import pprint


class Image(object):
	"""
	This object has got the behaviors of a docker image i.e. pulling an image and listing existing images
	"""
	
	def __init__(self, host, endp):
		self.headers = {"Authorization": 'Bearer '+ open("../data/auth.token").read()}
		self.docker_endp = "http://"+host+"/api/endpoints/"+str(endp)

	def list_images(self):
		images = requests.get(self.docker_endp+"/docker/images/json", headers=self.headers).json()
		pprint(images)