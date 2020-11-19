import socket
from time import sleep
from threading import Thread

from pynput.keyboard import Key, Controller
from pynput.mouse import Button
from pynput import mouse


"""---------------------------------------Variables----------------------------------------------"""

redemarrage = False

port = 4005
port_rep = 4006
port_com = 4010
ip_serv = None
motCO = "connexion formidable"
motCO_2 = "salut poto"
delimit_esp = "----------------------------------------------------------------"

nonCO = True
reception = True

z = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
z.connect(("8.8.8.8", 80))
IP = z.getsockname()[0]
z.close()

"""---------------------------------------Controlka----------------------------------------------"""
"""----------------------------------------------------------------------------------------------"""

clavier = Controller()
souris = mouse.Controller()

nom_app = "ControlKa"
version = "3.0"
dli = "------------------------------"
nom_utili = None

"""----------------------------------------------------------------------------------------------"""
"""----------------------------------------------------------------------------------------------"""



"""--------------------------Fonctions Utiles--------------------------------"""
def aff_spe(txt, mention, enc=False):
    chaine = "["+mention+"] "+txt
    if enc == False:
        print(chaine)
    else:
        return chaine

def aff_enc(txt):
    print(delimit_esp)
    print(txt)
    print(delimit_esp)

"""--------------------------Partie Ecoute Client--------------------------------"""
def ecoute_co():
    global nonCO
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.bind(("", port_rep))
    print("Lancement de l'ecoute...")
    while True:

        #recup message est ip

        m=s.recvfrom(1024)
        code = m[0].decode('utf-8')
        ip = m[1]
        if code == motCO_2:
            #print(code)
            #print(ip[0])
            sleep(2)
            nonCO = False
            break
    s.close()
"""--------------------------Partie Annonce global pour le Client--------------------------------"""
def dem_annonce():
    global nonCO
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.bind((str(IP), port))
        print("en attente de connexion !")
        aff_symb = "!"
        
        while nonCO:
                s.sendto(motCO.encode('utf-8'), ("255.255.255.255", port))
                
                aff_spe(aff_symb, "ATTENTE CONNEXION")
                if len(aff_symb) > 30:
                    aff_symb = "!"
                else:
                    aff_symb += "!"
                
                
                sleep(1)
        s.close()
    except Exception as e:
        print("ERREUR : envoie des données\n")
        print(e)

"""--------------------------Evenements--------------------------------"""
def co_client_fini():
    global redemarrage
    

    aff_enc(aff_spe("Le client a interrompue volontairement le connection !!!", "INFO", True))

    redemarrage = True

def co_client_fini_erreur():
    global redemarrage
    
    aff_enc(aff_spe("Le client ne repond plus le lien a donc été arreter !!!", "ERREUR", True))
    redemarrage = True
    
def co_client_eteint_serv():
    global redemarrage
    
    aff_enc(aff_spe("Le client vient d'envoyer l'ordre d'eteindre ce service !!!", "INFO", True))
    redemarrage = False

"""-------------------------------------------------------------------------------------"""
"""-------------------------------------------------------------------------------------"""
"""-------------------------------------------------------------------------------------"""
"""-------------------------------------------------------------------------------------"""
"""-----------------------------------CONTROLKA-----------------------------------------"""
"""-------------------------------------------------------------------------------------"""
"""-------------------------------------------------------------------------------------"""
"""-------------------------------------------------------------------------------------"""
"""-------------------------------------------------------------------------------------"""
"""-------------------------------------------------------------------------------------"""



'''---- procedure inportante ----'''

def tappe(touche):
    clavier.press(touche)
    clavier.release(touche)
    
def tappe_txt(txt):
    for i in txt:
        tappe(i)

        
'''---- fonctions generales ----'''
def commence_par(txt, mot):
    succes = True
    if(len(txt)<len(mot)):
	    succes = False
    else:
        for i in range(len(mot)):
            if txt[i] != mot[i]:
                succes = False
    return succes

def net_texte(txt):
    txt_propre = ""
    for i in range(len(txt)):
        if i > 4:
            txt_propre += txt[i]
    return txt_propre
        
def check_texte_codifier(code):
    if len(code) != 0:
        if commence_par(code, "text:"):
            return True
        else:
            return False
    else:
        return False
        
'''---- menu ----'''

def trad_code(code):
    global reception
    #tappe un texte
    if check_texte_codifier(code):
        tappe_txt(net_texte(code))
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
        co_client_fini_erreur()
        reception = False


"""-------------------------------------------------------------------------------------"""
"""-------------------------------------------------------------------------------------"""
"""-------------------------------------------------------------------------------------"""
"""-------------------------------------------------------------------------------------"""
"""-------------------------------------------------------------------------------------"""
"""-------------------------------------------------------------------------------------"""
"""-------------------------------------------------------------------------------------"""
"""-------------------------------------------------------------------------------------"""
"""-------------------------------------------------------------------------------------"""
"""-------------------------------------------------------------------------------------"""

   
"""--------------------------centre serveur--------------------------------"""
def main():
    print("[DEMARRAGE TOTAL] C PARTIE !!!")
    global port_com, nonCO, IP
    

    nonCO = True
    
    th1 = Thread(target=dem_annonce)
    th2 = Thread(target=ecoute_co)

    th1.start()
    th2.start()
    
    
    th1.join()
    th2.join()

    
    aff_spe(str(IP), "IP SERVER")
    addr = (IP, port_com)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(addr)

    def handle_client(conn, addr):
        global reception
        ip_client = addr[0]

        
        aff_spe(str(ip_client)+" s est connecter !!", "NOUVELLE CONNEXION")
        
        while reception:
            try:
                msg = conn.recv(1024)
            except Exception as e:
                print(e)
                co_client_fini_erreur()
                break

            msg = msg.decode('utf-8')

            aff_spe(msg, str(ip_client))

            trad_code(msg)
            if (msg == "#-123"):
                co_client_fini()
                break
            if (msg == "#123"):
                co_client_eteint_serv()
                break

        conn.close()
        s.close()
        reception = True

    def start():
        s.listen()
        aff_spe("ecoute de "+str(IP), "ECOUTE")
        conn, addr = s.accept()
        #aff_spe("un connexion a ete realise !!", "CONNEXION")
        handle_client(conn, addr)
        
            
    aff_spe("Demarrage du serveur...","DEMARRAGE")
    start()

main()
while redemarrage:
    main()
    
aff_enc(aff_spe("Au revoir...", "FIN DU SERVICE", enc=True))

