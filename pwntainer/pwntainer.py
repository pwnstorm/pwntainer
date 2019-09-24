from multiprocessing import Pool
import sys
from pprint import pprint

from modules import auth
from modules import containers

# Initialize the authentication object and supply host address and positional argument
a = auth.Auth(sys.argv[1])


def bruteforce(pw_list):
	with open(pw_list) as pass_list:
		passwords = pass_list.readlines()

	with Pool(4) as pool:
		results = pool.map(a.login, passwords)
		print(results)

def fetch_containers():
	print("[+] Fetching a list of available containers")
	cont = containers.Containers(sys.argv[1], 1)
	return cont.get_containers()

def main():
	#print("[*] Starting pwntainer bruteforce")
	#bruteforce("./data/wordlist.txt")
	
	creds = a.login("screature") #currently uses hardcoded crendential to test different endpoints.
	with open("./data/auth.token", 'w') as token:
		token.write(a.get_jwt())
	pprint(fetch_containers())


if __name__=="__main__":
	main()