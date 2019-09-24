from modules import auth
from multiprocessing import Pool
import sys

# Initialize the authentication object and supply host address and positional argument
a = auth.Auth(sys.argv[1])


def bruteforce(pw_list):
	with open(pw_list) as pass_list:
		passwords = pass_list.readlines()

	with Pool(4) as pool:
		results = pool.map(a.login, passwords)
		print(results)
		

def main():
	#print("[*] Starting pwntainer bruteforce")
	#bruteforce("./data/wordlist.txt")
	
	creds = a.login("screature") #currently uses hardcoded crendential to test different endpoints.
	with open("./data/auth.token", 'w') as token:
		token.write(a.get_jwt())
	


if __name__=="__main__":
	main()