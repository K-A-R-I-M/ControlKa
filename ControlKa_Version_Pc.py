from pynput.keyboard import Key, Controller
from pynput.mouse import Button
from pynput import mouse

import time

import socket

clavier = Controller()
souris = mouse.Controller()

'''---- procedure inportante ----'''

def tappe(touche):
    clavier.press(touche)
    clavier.release(touche)
    
def tappe_2(t1, t2):
    clavier.press(t1)
    clavier.press(t2)
    clavier.release(t2)
    clavier.release(t1)
    
def tappe_txt(txt):
    for i in txt:
        tappe(i)

        
'''---- fonctions generales ----'''

def check_texte_non_codifier(code):
    if len(code) != 0:
        if code[0] != "#":
            return True
        else:
            return False
    else:
        return False
        
'''---- menu ----'''

def menu(code):
    #tappe un texte
    if check_texte_non_codifier(code):
        tappe_txt(code)
    #espace pause play
    elif code == "#181902":
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
    #suppr
    elif code == "#-300":
        tappe(Key.backspace)
    # 4 fleche
    elif code == "#555":
        souris.click(Button.right, 1)
    elif code == "#-555":
        souris.click(Button.left, 1)
    elif code == "#999":
        tappe(Key.up)
    elif code == "#-999":
        tappe(Key.down)
    #entrer
    elif code == "#222":
        tappe(Key.enter)
    #autre
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
