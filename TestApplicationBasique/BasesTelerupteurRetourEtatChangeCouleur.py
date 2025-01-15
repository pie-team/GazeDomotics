# le thread est execute toutes les 2 secondes et met a jour variable1
# le programme principal met a jour variable2 et a une attente de 1 seconde
# donc variable2 est mis a jour 2 fois plus souvent que variable1

import threading    # pip install ?
import time
import queue    # pip install ?
# ~ import keyboard  # pip install keyboard
import cv2
from gaze_tracking import GazeTracking
import time
import numpy as np
from openpyxl import Workbook
import pandas as pd
import pyautogui
from Commandes import Commande
import subprocess

# ~ ##############################################
# ~ WF=640  # largeur image
# ~ HF=480  # hauteur image
# ~ erreur_relative=100 # init
# ~ WEcran=1920 #1600ok #1920ok
# ~ width=WF
# ~ height=HF
# ~ RatiosDefinis=0     # ratio des bornes gauche et droite definis 0:aucun 1:gauche 2:droite 3:gauche et droite 
# ~ FPSpourStabilisationRegard = 30 # Nb d'itérations pour considérer le regard stable si FPS=25 alors duree=(1/FPS)*NbIterations=(1/25)*30=1,2 seconde
# ~ liste_horizontal_ratio=[]   # pour enregistrement ratio
# ~ liste_erreur_relative=[]    # pour enregistrement erreur relative
# ~ liste_pupilles_detectees=[] # pour enregistrement detection pupilles
# ~ liste_oeil_ferme=[]         # pour enregistrement oeil ferme

# ~ largeur_nouvelle = WF*1 # nouvelle largeur image 1920pb 3200ok  x2pb  x3pb  x4pb  x5ok
# ~ hauteur_nouvelle = HF*1 # nouvelle hauteur image   x2pb   x3pb   x4pb  x5pb
# ~ ratio_horizontal = 0.0
# ~ erreur_relative = 0.0

# ~ webcam = cv2.VideoCapture(0)                    # cree objet webcam
# ~ time.sleep(1)                                   # attente
# ~ webcam.set(cv2.CAP_PROP_FRAME_WIDTH,WF)         # defini largeur capture video
# ~ webcam.set(cv2.CAP_PROP_FRAME_HEIGHT,HF)        # defini hauteur capture video
# ~ time.sleep(1)                                   # attente

# ~ RegardDroite = 0            # init
# ~ RegardGauche = 0            # init
# ~ commandeKNX = Commande()    # cree objet commandeKNX
couleur_SAM = [255, 255, 255]     # init couleur noire
couleur_centre_salon = [0, 0, 0]            # init couleur noire
couleur_texte_SAM = [0, 255, 255]           # init couleur jaune
couleur_texte_centre_salon = [0, 255, 255]  # init couleur jaune

# ~ retour_etat_SAM = 0             # init
# ~ retour_etat_centre_salon = 0    #init
# ~ ##################################################

# Fonction executee dans le thread
# ~ def CommandeDuThread(retour_etat_SAM, couleur_SAM, retour_etat_centre_salon, couleur_centre_salon):
def CommandeDuThread(FilePartagee):

    print("dans le thread")
    retour_etat_SAM = int(subprocess.getoutput('knxtool read ip: 6/0/209'))     # releve etat lampe
    if retour_etat_SAM == 0:        # si eteinte
        couleur_SAM = [0, 255, 255]     # couleur de fond jaune
        print("couleur_SAM eteinte thread:", couleur_SAM)
        couleur_texte_SAM = [0, 0, 0]   # texte en noir
    else:                           # sinon
        couleur_SAM = [0, 0, 0]     # couleur de fond noir
        print("couleur_SAM allumee thread:", couleur_SAM)
        couleur_texte_centre = [0, 255, 255]    #texte en jaune
        
    retour_etat_centre_salon = int(subprocess.getoutput('knxtool read ip: 6/0/208'))    # releve etat lampe
    if retour_etat_centre_salon == 0:       # si eteinte
        couleur_centre_salon = [0, 255, 255]    # couleur jaune
        couleur_texte_SAM = [0, 0, 0]   # texte en noir
    else:
        couleur_centre_salon = [0, 0, 0]    # couleur noire 
        couleur_texte_centre = [0, 255, 255]    # texte en jaune


# Fonction executee periodiquement (thread)
# ~ def ExecutionPeriodique(PeriodeExecutionThread, ConditionArretThread, retour_etat_SAM, couleur_SAM, retour_etat_centre_salon, couleur_centre_salon):
def ExecutionPeriodique(PeriodeExecutionThread, ConditionArretThread, FilePartagee):

        # PeriodeExecutionThread : periode execution en secondes
        # ConditionArretThread : evenement a definir pour arret le thread
        # FilePartagee : file d'attente entre le thread et le programme principal
    while not ConditionArretThread.is_set():    # tant que la condition d'arret n'existe pas
        CommandeDuThread(FilePartagee)          # execute la fonction CommandeDuThread
        time.sleep(PeriodeExecutionThread)      # mise en attente de duree PeriodeExecutionThread

################### Initialisation des variables du programme principal ici? #############
WF=640  # largeur image
HF=480  # hauteur image
erreur_relative=100 # init
WEcran=1920 #1600ok #1920ok
width=WF
height=HF
RatiosDefinis=0     # ratio des bornes gauche et droite definis 0:aucun 1:gauche 2:droite 3:gauche et droite 
FPSpourStabilisationRegard = 30 # Nb d'itérations pour considérer le regard stable si FPS=25 alors duree=(1/FPS)*NbIterations=(1/25)*30=1,2 seconde
liste_horizontal_ratio=[]   # pour enregistrement ratio
liste_erreur_relative=[]    # pour enregistrement erreur relative
liste_pupilles_detectees=[] # pour enregistrement detection pupilles
liste_oeil_ferme=[]         # pour enregistrement oeil ferme

largeur_nouvelle = WF*1 # nouvelle largeur image 1920pb 3200ok  x2pb  x3pb  x4pb  x5ok
hauteur_nouvelle = HF*1 # nouvelle hauteur image   x2pb   x3pb   x4pb  x5pb
ratio_horizontal = 0.0
erreur_relative = 0.0

webcam = cv2.VideoCapture(0)                    # cree objet webcam
time.sleep(1)                                   # attente
webcam.set(cv2.CAP_PROP_FRAME_WIDTH,WF)         # defini largeur capture video
webcam.set(cv2.CAP_PROP_FRAME_HEIGHT,HF)        # defini hauteur capture video
time.sleep(1)                                   # attente

RegardDroite = 0            # init
RegardGauche = 0            # init
commandeKNX = Commande()    # cree objet commandeKNX
# ~ couleur_SAM = [255, 255, 255]     # init couleur noire
# ~ couleur_centre_salon = [0, 0, 0]            # init couleur noire
# ~ couleur_texte_SAM = [0, 255, 255]           # init couleur jaune
# ~ couleur_texte_centre_salon = [0, 255, 255]  # init couleur jaune

retour_etat_SAM = 0             # init
retour_etat_centre_salon = 0    #init
###############################"

# Créer une file pour partager les résultats entre le thread et le programme principal
FilePartagee = queue.Queue()

# Intervalle en secondes pour executer commande du thread
PeriodeExecutionThread = 2

# Cree un objet evenement pour arrêter le thread initialement de valeur non definie 
ConditionArretThread = threading.Event()    # mecanisme de synchro 

# Création du thread
# ~ thread = threading.Thread(target=ExecutionPeriodique, args=(PeriodeExecutionThread, ConditionArretThread, retour_etat_SAM, couleur_SAM, retour_etat_centre_salon, couleur_centre_salon))
thread = threading.Thread(target=ExecutionPeriodique, args=(PeriodeExecutionThread, ConditionArretThread, FilePartagee))

        # thread : objet de type threading
        # target=ExecutionPeriodique : fonction execute par l'objet thread
        # args=(PeriodeExecutionThread, ConditionArretThread, FilePartagee) : arguments de la fonction execute par l'objet thread
        #       PeriodeExecutionThread : periode en secondes
        #       ConditionArretThread : condition d'arret du thread
        #       FilePartagee : file d'attente pour echange entre thread et programme principal
        
# Démarrer le thread
thread.start()

# Code principal
try:
    gaze = GazeTracking()       # cree  objet gaze
    
        ############## AFFICHAGE ####################   
    screen_width, screen_heigth = pyautogui.size()                  # relever les dimensions de l'écran
    window_height = HF                                              # definir la hauteur de la fenêtre 
    cv2.namedWindow("Chez Gérard", cv2.WINDOW_NORMAL)               # cree une fenetre redimensionnable
    cv2.setWindowProperty("Chez Gérard", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)  # passe en plein ecran
    cv2.resizeWindow("Chez Gérard", screen_width, window_height)    # retaille la fenetre
        ############## AFFICHAGE ####################   
        
        

    while True:
        # Capture d'une image
        _, frame = webcam.read()
   
        # Analyse de l'image
        gaze.refresh(frame)
    
        # Place croix sur pupilles
        frame = gaze.annotated_frame()

        # Rotation image selon axe vertical pour retour utilisateur
        frame=cv2.flip(frame,1)
    
        # Analyse du regard
        # ~ if gaze.is_blinking():
            # ~ print("Clignotement")
 
        if gaze.is_left():          
            RegardDroite = 0                    # RAZ RegardDroite
            RegardGauche = RegardGauche + 1     # incremente compteur
            # ~ print("Nb iterations regard gauche:", RegardGauche)     # affiche info dans terminal
        
            # mode telerupteur   
            if RegardGauche >= 17:              # il faut maintenir le regard pendant au moins 30 iterations
                if retour_etat_SAM == 0:            # si eteinte
                    commandeKNX.SAM_allumer()       # allume
                else:
                    commandeKNX.SAM_allumer()
                RegardGauche = 0                    # RAZ compteur 
        
        elif gaze.is_right():
            RegardGauche = 0                    # RAZ RegardGauche
            RegardDroite = RegardDroite + 1     # incremente compteur
            # ~ print("Nb iterations regard droite:", RegardDroite)     # affiche info dans terminal
                               
            # mode telerupteur   
            if RegardDroite >= 17:              # il faut maintenir le regard pendant au moins 30 iterations
                if retour_etat_centre_salon == 0:       # si eteinte
                    commandeKNX.Centre_allumer()    # allume
                else:                           # sinon
                    commandeKNX.Centre_eteindre()   # eteint
                RegardDroite = 0                    # RAZ compteur
         
        elif gaze.is_center():
            # ~ print("Regard au centre")
            RegardDroite = 0                    # RAZ Regardroite
            RegardGauche = 0                    # RAZ RegardGauche
        
    ############## AFFICHAGE ####################    
        print("dans affichage")
        print("couleur_SAM affichage", couleur_SAM)
        frame_redimensionnee = cv2.resize(frame, (largeur_nouvelle, hauteur_nouvelle))
        height, width, _ = frame_redimensionnee.shape       # releve dimensions de l'image de la webcam

        # Définir la place dispo pour les bandes
        WDispo = WEcran - width
        LargeurBandes = int(WDispo/2)
    
        # Créer une image avec des bandes de couleur sur les côtés
        bordered_frame = np.zeros((height, WEcran, 3), dtype=np.uint8)
            # height hauteur webcam redimensionnee
            # largeur largeur ecran

        # Ajouter couleur commande envoyee a gauche
        bordered_frame[:, :LargeurBandes] = couleur_SAM     # Couleur SaM
            #  [hauteur , largeur]
            # : toutes les lignes
            # :LargeurBandes       les colonnes depuis le début (:) jusqu'à LargeurBandes
        # Ajouter nom de la pièce
        Texte = "Salle a manger"
        Position = (160,100)
        Police = cv2.FONT_HERSHEY_SIMPLEX
        TaillePolice = 1
        CouleurTexte = couleur_texte_SAM
        EpaisseurTexte = 2
        cv2.putText(bordered_frame, Texte, Position, Police, TaillePolice, CouleurTexte, EpaisseurTexte)
    
        # Ajouter couleur commande envoyee a droite
        bordered_frame[:, -LargeurBandes:] = couleur_centre_salon  # Couleur centre
            #  [hauteur , largeur]    
            # : toutes les lignes
            # -LargeurBandes:       les colonnes depuis la fin (:) en remontant de LargeurBandes
        # Ajouter nom de la pièce
        Texte = "Centre salon"
        Position = (1500,100)
        Police = cv2.FONT_HERSHEY_SIMPLEX
        TaillePolice = 1
        CouleurTexte = couleur_texte_centre_salon
        EpaisseurTexte = 2
        cv2.putText(bordered_frame, Texte, Position, Police, TaillePolice, CouleurTexte, EpaisseurTexte)
        
        # Copier le flux vidéo au centre de l'image
        bordered_frame[:, LargeurBandes:LargeurBandes + width] = frame
            #  [hauteur , largeur]    
            # : toutes les lignes
            # LargeurBandes:            colonne de départ
            # :LargeurBandes + width    colonne de fin
    
        # Afficher l'image
        cv2.imshow("Chez Gérard", bordered_frame)  
    ############## AFFICHAGE ####################             
        ###############  A VERIFIER  ###################
        # ~ if keyboard.is_pressed('esc'):
            # ~ ConditionArretThread.set()  # defini evenement d'arret
            # ~ break
        ###############  A VERIFIER  ###################

except KeyboardInterrupt:
    # Arrêter le thread lors d'une interruption (par exemple, Ctrl+C)
    ConditionArretThread.set()  # indique que l'evenement est defini provoquera arret thread
    thread.join()       # attendre que le thread se termine avant de quitter le programme principal

print("Fin du programme principal")
