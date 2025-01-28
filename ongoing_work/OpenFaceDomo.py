# -*- coding: utf-8 -*-

# Gaze data analyser for OpenFace csv output

import time
import numpy as np
import pandas as pd
import os
import cv2
from Commandes import Commande
import subprocess as sp
import multiprocessing as mp


WF=640	# largeur image
HF=480	# hauteur image
width=WF
height=HF
largeur_nouvelle = WF*1	# nouvelle largeur image 1920pb 3200ok  x2pb  x3pb  x4pb  x5ok
hauteur_nouvelle = HF*1	# nouvelle hauteur image   x2pb   x3pb   x4pb  x5pb

RegardDroite = 0			# init
RegardGauche = 0			# init
RegardHaut = 0				# init
RegardBas = 0				# init
commandeKNX = Commande()	# cree objet commandeKNX
couleur_SAM = [0, 0, 0]		# init couleur noire
couleur_centre_salon = [0, 0, 0]			# init couleur noire
couleur_chambre = [0, 0, 0]			# init couleur noire
couleur_toilettes = [0, 0, 0]			# init couleur noire
couleur_texte_SAM = [0, 255, 255]			# init couleur jaune
couleur_texte_centre_salon = [0, 255, 255]	# init couleur jaune
couleur_texte_toilettes = [0, 255, 255]	# init couleur jaune
couleur_texte_chambre = [0, 255, 255]		# init couleur jaune
retour_etat_SaM=0
retour_etat_centre=0
retour_etat_toilettes=0
retour_etat_chambre=0

NbImages = 0				# Nb images capturees
PeriodeRafraichissementInterface = 10		# PeriodeRafraichissementInterface = 1/FPS   si FPS=30 images/s avec PeriodeRafraichissementInterface = 15 MaJ interface toutes les 500ms


# Screen dimensions
screen_width, screen_height = 1920, 1200

# Create a black image
frame = np.zeros((screen_height, screen_width, 3), dtype=np.uint8)

# Define the text and its properties
text = "Regardez la croix qui va apparaitre"
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1
color = (128, 128, 128)  # Grey color
thickness = 2
text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
text_x = (frame.shape[1] - text_size[0]) // 2
text_y = (frame.shape[0] + text_size[1]) // 2

# Put the text on the image
cv2.putText(frame, text, (text_x, text_y), font, font_scale, color, thickness)

# Create a window and display the image
cv2.namedWindow("Chez Gérard", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("Chez Gérard", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)  # passe en plein ecran
cv2.imshow("Chez Gérard", frame)

# Wait for 3 seconds
cv2.waitKey(3000)

# Close the window
cv2.destroyAllWindows()


# ############## AFFICHAGE ####################   

# Create a black image
frame = np.zeros((screen_height, screen_width, 3), dtype=np.uint8)

# Define the text and its properties
text = "+"
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1
color = (128, 128, 128)  # Grey color
thickness = 2
text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
text_x = (frame.shape[1] - text_size[0]) // 2
text_y = (frame.shape[0] + text_size[1]) // 2

# Put the text on the image
cv2.putText(frame, text, (text_x, text_y), font, font_scale, color, thickness)

# Create a window and display the image
cv2.namedWindow("Chez Gérard", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("Chez Gérard", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)  # passe en plein ecran
cv2.imshow("Chez Gérard", frame)

pool = mp.Pool(2)
OpenFace = pool.map_async(sp.call, ['./OpenFace_runner.sh'])

# Wait for 10 seconds
cv2.waitKey(10500)

# Close the window
cv2.destroyAllWindows()

calibration_data = pd.read_csv("./Data_OpenFace/Test.csv")
calibration_data = calibration_data[['gaze_angle_x', 'gaze_angle_y',]]
calibration_data = calibration_data.mean()

# Create a black image
frame = np.zeros((screen_height, screen_width, 3), dtype=np.uint8)

# Define the text and its properties
text = "Calibration terminee"
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1
color = (128, 128, 128)  # Grey color
thickness = 2
text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
text_x = (frame.shape[1] - text_size[0]) // 2
text_y = (frame.shape[0] + text_size[1]) // 2

# Put the text on the image
cv2.putText(frame, text, (text_x, text_y), font, font_scale, color, thickness)

# Create a window and display the image
cv2.namedWindow("Chez Gérard", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("Chez Gérard", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)  # passe en plein ecran
cv2.imshow("Chez Gérard", frame)

# Wait for 3 seconds
cv2.waitKey(3000)

# Close the window
cv2.destroyAllWindows()


while True :
    data = pd.read_csv("./Data_OpenFace/Test.csv")
    gaze_data = data[['gaze_angle_x', 'gaze_angle_y']]
    gaze_data = gaze_data.tail(1)
    gaze_data = gaze_data - np.asarray([calibration_data['gaze_angle_x'], calibration_data['gaze_angle_y']])

    # Releve periodique etat installation et mise a jour interface graphique
    NbImages = NbImages + 1															# incremente NbImages prises
    if NbImages >= PeriodeRafraichissementInterface:								# si delai atteint
		# releve etat installation
        # retour_etat_SaM = 0  #int(subprocess.getoutput('knxtool read ip: 6/0/209'))		# releve etat lampe	SAM
        # retour_etat_centre = 1  #int(subprocess.getoutput('knxtool read ip: 6/0/208'))	# releve etat lampe centre salon
        # NbImages = 0																# RAZ compteur images prises
		# MAJ etat lampe SAM
        if retour_etat_SaM == 0:				# si eteinte
            couleur_SAM = [0, 0, 0]				# couleur de fond noir
            couleur_texte_SAM = [128, 128, 128]	# texte gris moyen
        else:									# sinon
            couleur_SAM = [0, 50, 0]			# couleur de fond jaune
            couleur_texte_SAM = [128, 128, 128]	# texte gris moyen
		# MAJ etat lampe salon
        if retour_etat_centre == 0:							# si eteinte
            couleur_centre_salon = [0, 0, 0]				# couleur de fond noir
            couleur_texte_centre_salon = [128, 128, 128]	# texte gris moyen
        else:												# sinon
            couleur_centre_salon = [0, 50, 0]			# couleur de fond jaune
            couleur_texte_centre_salon = [128, 128, 128]	# texte gris moyen
        # MAJ etat toilettes
        if retour_etat_toilettes == 0:							# si eteinte
            couleur_toilettes = [0, 0, 0]				# couleur de fond noir
            couleur_texte_toilettes = [128, 128, 128]	# texte gris moyen
        else:												# sinon
            couleur_toilettes = [0, 50, 0]			# couleur de fond jaune
            couleur_texte_toilettes = [128, 128, 128]	# texte gris moyen
        # MAJ etat chambre
        if retour_etat_chambre == 0:							# si eteinte
            couleur_chambre = [0, 0, 0]				# couleur de fond noir
            couleur_texte_chambre = [128, 128, 128]	# texte gris moyen
        else:												# sinon
            couleur_chambre = [0, 50, 0]			# couleur de fond jaune
            couleur_texte_chambre = [128, 128, 128]	# texte gris moyen
				# (0,0,0) noir / (50,50,50) gris fonce / (128,128,128) gris moyen / (200,200,200) gris clair / (255,255,255) blanc


    # traitement du regard
	# si regard a gauche
    if gaze_data['gaze_angle_x'].values[0] > 0.06 and gaze_data['gaze_angle_y'].values[0] < 0.06 and gaze_data['gaze_angle_y'].values[0] > -0.06:	# si regard a gauche
        RegardDroite = 0  					# RAZ RegardDroite
        RegardGauche = RegardGauche + 1		# incremente compteur
        # ~ print("Nb iterations regard gauche:", RegardGauche)		# affiche info dans terminal
        
		# gestion envoi commande lampe SAM en mode telerupteur   
        if RegardGauche >= 17:				# il faut maintenir le regard pendant au moins 17 iterations
            if retour_etat_SaM == 0:		# si lampe eteinte
                retour_etat_SaM=1
                #commandeKNX.SAM_allumer()	# allume
            else:
                retour_etat_SaM=0							# sinon
                #commandeKNX.SAM_eteindre()	# eteint
            RegardGauche = 0				# RAZ compteur 
    
    # si regard a droite
    elif gaze_data['gaze_angle_x'].values[0] < -0.06 and gaze_data['gaze_angle_y'].values[0] < 0.06 and gaze_data['gaze_angle_y'].values[0] > -0.06:				# si regard a droite
        RegardGauche = 0					# RAZ RegardGauche
        RegardDroite = RegardDroite + 1		# incremente compteur
        # ~ print("Nb iterations regard droite:", RegardDroite)		# affiche info dans terminal
                               
        # gestion envoi commande lampe centre salon en mode telerupteur   
        if RegardDroite >= 17:					# il faut maintenir le regard pendant au moins 17 iterations
            if retour_etat_centre == 0:			# si eteinte
                retour_etat_centre=1
                #commandeKNX.Centre_allumer()	# allume
            else:
                retour_etat_centre=0								# sinon
                #commandeKNX.Centre_eteindre()	# eteint
            RegardDroite = 0					# RAZ compteur
    
    # si regard en haut
    elif gaze_data['gaze_angle_x'].values[0] < 0.06 and gaze_data['gaze_angle_x'].values[0] > -0.06 and gaze_data['gaze_angle_y'].values[0] > 0.06:				# si regard en haut
        RegardBas = 0					# RAZ RegardGauche
        RegardHaut = RegardHaut + 1		# incremente compteur
        # ~ print("Nb iterations regard Haut:", RegardHaut)		# affiche info dans terminal
                               
        # gestion envoi commande lampe centre salon en mode telerupteur   
        if RegardHaut >= 17:					# il faut maintenir le regard pendant au moins 17 iterations
            if retour_etat_toilettes == 0:			# si eteinte
                retour_etat_toilettes=1
                #commandeKNX.Centre_allumer()	# allume
            else:
                retour_etat_toilettes=0								# sinon
                #commandeKNX.Centre_eteindre()	# eteint
            RegardHaut = 0					# RAZ compteur
    
    # si regard en bas
    elif gaze_data['gaze_angle_x'].values[0] < 0.06 and gaze_data['gaze_angle_x'].values[0] > -0.06 and gaze_data['gaze_angle_y'].values[0] < -0.06:				# si regard en bas
        RegardHaut = 0					# RAZ RegardGauche
        RegardBas = RegardBas + 1		# incremente compteur
        # ~ print("Nb iterations regard Haut:", RegardHaut)		# affiche info dans terminal
                               
        # gestion envoi commande lampe centre salon en mode telerupteur   
        if RegardBas >= 17:					# il faut maintenir le regard pendant au moins 17 iterations
            if retour_etat_chambre == 0:			# si eteinte
                retour_etat_chambre=1
                #commandeKNX.Centre_allumer()	# allume
            else:
                retour_etat_chambre=0								# sinon
                #commandeKNX.Centre_eteindre()	# eteint
            RegardBas = 0					# RAZ compteur

    # si regard au centre         
    elif gaze_data['gaze_angle_x'].values[0] < 0.06 and gaze_data['gaze_angle_x'].values[0] > -0.06 and gaze_data['gaze_angle_y'].values[0] < 0.06 and gaze_data['gaze_angle_y'].values[0] > -0.06:				# si regard au centre
        # ~ print("Regard au centre")
        RegardDroite = 0					# RAZ Regardroite
        RegardGauche = 0					# RAZ RegardGauche
        RegardHaut = 0					# RAZ Regardhaut
        RegardBas = 0					# RAZ Regardbas

############## AFFICHAGE ####################  
    frame = cv2.imread("2025-01-22-121530.jpg")
    frame_redimensionnee = cv2.resize(frame, (largeur_nouvelle, hauteur_nouvelle))
    height, width, _ = frame_redimensionnee.shape 		# releve dimensions de l'image de la webcam

    # Définir la place dispo pour les bandes
    WDispo = screen_width - width
    LargeurBandes = int(WDispo/2)

    HDispo = screen_height - height
    HauteurBandes = int(HDispo/2)
    
    # Créer une image avec des bandes de couleur sur les côtés
    bordered_frame = np.zeros((screen_height, screen_width, 3), dtype=np.uint8)
		# height hauteur webcam redimensionnee
		# largeur largeur ecran

    # Ajouter couleur commande envoyee a gauche
    bordered_frame[HauteurBandes:screen_height-HauteurBandes, :LargeurBandes] = couleur_SAM		# Couleur SaM
		#  [hauteur , largeur]
		# : toutes les lignes
		# :LargeurBandes       les colonnes depuis le début (:) jusqu'à LargeurBandes
	# Ajouter nom de la pièce
    Texte = "Salle a manger"
    Position = (160,600)
    Police = cv2.FONT_HERSHEY_SIMPLEX
    TaillePolice = 1
    CouleurTexte = couleur_texte_SAM
    EpaisseurTexte = 2
    cv2.putText(bordered_frame, Texte, Position, Police, TaillePolice, CouleurTexte, EpaisseurTexte)
  
    # Ajouter couleur commande envoyee a droite
    bordered_frame[HauteurBandes:screen_height-HauteurBandes, -LargeurBandes:] = couleur_centre_salon  # Couleur centre salon
		#  [hauteur , largeur]    
		# : toutes les lignes
		# -LargeurBandes:       les colonnes depuis la fin (:) en remontant de LargeurBandes
	# Ajouter nom de la pièce
    Texte = "Centre salon"
    Position = (1500,600)
    Police = cv2.FONT_HERSHEY_SIMPLEX
    TaillePolice = 1
    CouleurTexte = couleur_texte_centre_salon
    EpaisseurTexte = 2
    cv2.putText(bordered_frame, Texte, Position, Police, TaillePolice, CouleurTexte, EpaisseurTexte)

    # Ajouter couleur commande envoyee en haut
    bordered_frame[:HauteurBandes, LargeurBandes:screen_width-LargeurBandes] = couleur_toilettes		# Couleur SaM
		#  [hauteur , largeur]
		# : toutes les lignes
		# :HauteurBandes       les colonnes depuis le début (:) jusqu'à HauteurBandes
	# Ajouter nom de la pièce
    Texte = "Toilettes"
    Position = (800,50)
    Police = cv2.FONT_HERSHEY_SIMPLEX
    TaillePolice = 1
    CouleurTexte = couleur_texte_toilettes
    EpaisseurTexte = 2
    cv2.putText(bordered_frame, Texte, Position, Police, TaillePolice, CouleurTexte, EpaisseurTexte)

    # Ajouter couleur commande envoyee en bas
    bordered_frame[-HauteurBandes:, LargeurBandes:screen_width-LargeurBandes] = couleur_chambre		# Couleur SaM
		#  [hauteur , largeur]
		# : toutes les lignes
		# :HauteurBandes      les colonnes depuis la fin (:) en remontant de HauteurBandes
	# Ajouter nom de la pièce
    Texte = "Chambre"
    Position = (800,1100)
    Police = cv2.FONT_HERSHEY_SIMPLEX
    TaillePolice = 1
    CouleurTexte = couleur_texte_chambre
    EpaisseurTexte = 2
    cv2.putText(bordered_frame, Texte, Position, Police, TaillePolice, CouleurTexte, EpaisseurTexte)

    # Copier le flux vidéo au centre de l'image
    bordered_frame[HauteurBandes:HauteurBandes + height, LargeurBandes:LargeurBandes + width] = frame
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
    