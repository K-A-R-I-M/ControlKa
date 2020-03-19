from pynput.keyboard import Key, Controller
import time

import socket

clavier = Controller()

''' procedure inportante '''
def tappe(touche):
    clavier.press(touche)
    clavier.release(touche)
def tappe_2(t1, t2):
    clavier.press(t1)
    clavier.press(t2)
    clavier.release(t2)
    clavier.release(t1)
''' menu '''
def menu(code):
    #espace pause play
    if code == "#181902":
        tappe(Key.space)
    #plein ecran yt
    elif code == "#2582":
        tappe('f')
    #son ++
    elif code == "#1800":
        tappe(Key.media_volume_up)
    #son --
    elif code == "#1815":
        tappe(Key.media_volume_down)
    #droite
    elif code == "#100":
        tappe(Key.right)
    #gauche
    elif code == "#-100":
        tappe(Key.left)
    else:
        print("ce n'est pas une action prise en charge (ou arret d'ecoute)")

    
'''------------fonction main---------------'''
def prog():

    #permet ecoute du port 4005 en broadcast
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.bind(("", 4005))
    print("Lancement de l'ecoute...")
    #boucle ecoute
    
    while True:

        #recup message est ip
        
        m=s.recvfrom(1024)
        code = m[0].decode('utf-8')
        ip = m[1]
        print(code)
        print(ip[0])
        
        #appel fonction menu de choix
        menu(code)
        if code == "#123":
            print("Fin de l'ecoute...\nAu Revoir")
            break
    s.close()
prog()
