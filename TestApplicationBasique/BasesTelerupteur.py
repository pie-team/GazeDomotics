# mode telerupteur
# a droite lampe centre salon
# a gauche lampe salle a manger


import cv2
from gaze_tracking import GazeTracking
import time
import numpy as np
from openpyxl import Workbook
import pandas as pd
import pyautogui
from Commandes import Commande
import subprocess


WF=640	# largeur image
HF=480	# hauteur image
erreur_relative=100	# init
WEcran=1920 #1600ok #1920ok
width=WF
height=HF
RatiosDefinis=0		# ratio des bornes gauche et droite definis 0:aucun 1:gauche 2:droite 3:gauche et droite 
FPSpourStabilisationRegard = 30	# Nb d'itérations pour considérer le regard stable si FPS=25 alors duree=(1/FPS)*NbIterations=(1/25)*30=1,2 seconde
liste_horizontal_ratio=[]	# pour enregistrement ratio
liste_erreur_relative=[]	# pour enregistrement erreur relative
liste_pupilles_detectees=[]	# pour enregistrement detection pupilles
liste_oeil_ferme=[]			# pour enregistrement oeil ferme

largeur_nouvelle = WF*1	# nouvelle largeur image 1920pb 3200ok  x2pb  x3pb  x4pb  x5ok
hauteur_nouvelle = HF*1	# nouvelle hauteur image   x2pb   x3pb   x4pb  x5pb
ratio_horizontal = 0.0
erreur_relative = 0.0

webcam = cv2.VideoCapture(0)					# cree objet webcam
time.sleep(1)									# attente
webcam.set(cv2.CAP_PROP_FRAME_WIDTH,WF)			# defini largeur capture video
webcam.set(cv2.CAP_PROP_FRAME_HEIGHT,HF)		# defini hauteur capture video
time.sleep(1)									# attente

RegardDroite = 0				# init
RegardGauche = 0
commandeKNX = Commande()		# cree objet commandeKNX

gaze = GazeTracking()		# cree  objet gaze

############## AFFICHAGE ####################   
screen_width, screen_height = pyautogui.size()				# relever les dimensions de l'écran
window_height = HF											# definir la hauteur de la fenêtre 
# ~ cv2.namedWindow("Chez Gérard", cv2.WND_PROP_FULLSCREEN)		# cree une fenetre
cv2.namedWindow("Chez Gérard", cv2.WINDOW_NORMAL)				# cree une fenetre redimensionnable
cv2.setWindowProperty("Chez Gérard", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)  # passe en plein ecran
cv2.resizeWindow("Chez Gérard", screen_width, window_height)	# retaille la fenetre
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

############# TRAITEMENT REGARD ##################
    if gaze.is_left():       
        RegardDroite = 0  					# RAZ RegardDroite
        RegardGauche = RegardGauche + 1		# incremente compteur
        # ~ print("Nb iterations regard gauche:", RegardGauche)		# affiche info dans terminal
        
		# mode telerupteur   
        if RegardGauche >= 17:				# il faut maintenir le regard pendant au moins 4 iterations
            retour_etat_SaM = int(subprocess.getoutput('knxtool read ip: 6/0/209'))	# releve etat lampe
            print("retour etat SAM:", retour_etat_SaM)
            if retour_etat_SaM == 0:		# si eteinte
                commandeKNX.SAM_allumer()	# allume
            else:							# sinon
                commandeKNX.SAM_eteindre()	# eteint
            RegardGauche = 0				# RAZ compteur
         
    elif gaze.is_right():
        RegardGauche = 0					# RAZ RegardGauche
        RegardDroite = RegardDroite + 1		# incremente compteur
        # ~ print("Nb iterations regard droite:", RegardDroite)		# affiche info dans terminal
                               
        # mode telerupteur   
        if RegardDroite >= 17:				# il faut maintenir le regard pendant au moins 4 iterations
            retour_etat_centre = int(subprocess.getoutput('knxtool read ip: 6/0/208'))	# releve etat lampe
            print("retour etat centre:", retour_etat_centre)
            if retour_etat_centre == 0:		# si eteinte
                commandeKNX.Centre_allumer()	# allume
            else:							# sinon
                commandeKNX.Centre_eteindre()	# eteint
            RegardDroite = 0					# RAZ compteur
      
    elif gaze.is_center():
        print("Regard au centre")
        RegardDroite = 0					# RAZ Regardroite
        RegardGauche = 0					# RAZ RegardGauche
############# TRAITEMENT REGARD ##################
        
############## AFFICHAGE ####################    
    frame_redimensionnee = cv2.resize(frame, (largeur_nouvelle, hauteur_nouvelle))
    height, width, _ = frame_redimensionnee.shape 		# releve dimensions de l'image de la webcam

    # Définir la place dispo pour les bandes
    WDispo = WEcran - width
    LargeurBandes = int(WDispo/2)
    
    # Créer une image avec des bandes de couleur sur les côtés
    bordered_frame = np.zeros((height, WEcran, 3), dtype=np.uint8)
		# height hauteur webcam redimensionnee
		# largeur largeur ecran

    # Ajouter la bande bleue à gauche
    bordered_frame[:, :LargeurBandes] = [255, 0, 0]  # Couleur bleue (BGR)
		#  [hauteur , largeur]
		# : toutes les lignes
		# :LargeurBandes       les colonnes depuis le début (:) jusqu'à LargeurBandes

    # Ajouter la bande rouge à droite
    bordered_frame[:, -LargeurBandes:] = [0, 0, 255]  # Couleur rouge (BGR)
		#  [hauteur , largeur]    
		# : toutes les lignes
		# -LargeurBandes:       les colonnes depuis la fin (:) en remontant de LargeurBandes
    
    # Copier le flux vidéo au centre de l'image
    bordered_frame[:, LargeurBandes:LargeurBandes + width] = frame
		#  [hauteur , largeur]    
		# : toutes les lignes
		# LargeurBandes:            colonne de départ
		# :LargeurBandes + width    colonne de fin
    
    # Afficher l'image
    cv2.imshow("Chez Gérard", bordered_frame)  
############## AFFICHAGE ####################         
        
    # Quitter    
    if cv2.waitKey(1) == 27:
        break
   
webcam.release()			# Liberation camera
cv2.destroyAllWindows()		# Liberation memoire
