# mode telerupteur
# a droite lampe centre salon
# a gauche lampe salle a manger


import cv2
import keyboard
from gaze_tracking import GazeTracking
import time
import numpy as np
import argparse
#from openpyxl import Workbook
#import pandas as pd
import pyautogui
from Commandes import Commande
import subprocess
from matplotlib import pyplot as plt

# Arguments
parser=argparse.ArgumentParser()
parser.add_argument('--mode', type=str, default='h', help='h, v, hv')
parser.add_argument('--ratio', type=str, default='hv', help='h v or hv')
parser.add_argument('--video', type=str, default='no', help='yes for video feedback no is default')
parser.add_argument('--point_pos', type=str, default='mid', help='point position up mid down/ doesn t match well with video feedback ')
parser.add_argument('--axes', type=str, default='yes', help='axes instead of points')

args=parser.parse_args()

# Paramètres image
WF=640	# largeur image
HF=480	# hauteur image
erreur_relative=100	# init
WEcran=1920 #1600ok #1920ok
width=WF
height=HF
largeur_nouvelle = WF*1	# nouvelle largeur image 1920pb 3200ok  x2pb  x3pb  x4pb  x5ok
hauteur_nouvelle = HF*1	# nouvelle hauteur image   x2pb   x3pb   x4pb  x5pb

# Paramètes exp
RatiosDefinis=0		# ratio des bornes gauche et droite definis 0:aucun 1:gauche 2:droite 3:gauche et droite 
FPSpourStabilisationRegard = 30	# Nb d'itérations pour considérer le regard stable si FPS=25 alors duree=(1/FPS)*NbIterations=(1/25)*30=1,2 seconde
liste_horizontal_ratio=[]
liste_vertical_ratio=[]	# pour enregistrement ratio
liste_erreur_relative=[]	# pour enregistrement erreur relative
liste_temps=[]              # pour enregistrement de t


ratio_horizontal = 0.0
erreur_relative = 0.0
periode=5.00 #en secondes

#FPS=1000000/40000=25
webcam=cv2.VideoCapture(0)
time.sleep(1)									# attente
webcam.set(cv2.CAP_PROP_FRAME_WIDTH,WF)
webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, HF)
time.sleep(1)

RegardDroite = 0			# init
RegardGauche = 0			# init


NbImages = 0				# Nb images capturees
PeriodeRafraichissementInterface = 15		# PeriodeRafraichissementInterface = 1/FPS   si FPS=30 images/s avec PeriodeRafraichissementInterface = 15 MaJ interface toutes les 500ms

gaze = GazeTracking()		# cree  objet gaze

############## AFFICHAGE ####################   
screen_width, screen_height = pyautogui.size()				# relever les dimensions de l'écran
window_height = 2*HF											# definir la hauteur de la fenêtre 
# ~ cv2.namedWindow("Chez Gérard", cv2.WND_PROP_FULLSCREEN)		# cree une fenetre
cv2.namedWindow("Test", cv2.WINDOW_NORMAL)				# cree une fenetre redimensionnable
cv2.setWindowProperty("Test", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)  # passe en plein ecran
cv2.resizeWindow("Test", screen_width, window_height)	# retaille la fenetre

# Paramètres constants de textes et couleurs
Texte = "+"
if args.point_pos=='mid':
    Position_c = (WEcran//2,480)
    Position_g = (20,480)
    Position_d = (WEcran-22,480)

elif args.pos_point=='up':
    Position_c = (WEcran//2,50)
    Position_g = (20,480)
    Position_d = (WEcran-22,50)

elif args.pos_point=='down':
    Position_c = (WEcran//2,940)
    Position_g = (20,810)
    Position_d = (WEcran-22,940)   

Police = cv2.FONT_HERSHEY_SIMPLEX
TaillePolice = 1
CouleurTexte = [255,255,255]
EpaisseurTexte = 2
############## AFFICHAGE ####################   
start=time.time()
while True:
    # Capture d'une image
    ret,frame=webcam.read()
    assert(ret)

    # Calcul et enregistrement du temps
    t=time.time()-start
    liste_temps.append(t)

    # Analyse de l'image
    gaze.refresh(frame)
    
	# Place croix sur pupilles
    frame = gaze.annotated_frame()

	# Rotation image selon axe vertical pour retour utilisateur
    frame=cv2.flip(frame,1)
    
    # Enregistrement du ratio
    if gaze.horizontal_ratio()!=10:
        liste_horizontal_ratio.append(gaze.horizontal_ratio())
    else:
        liste_horizontal_ratio.append(None)
    
    if gaze.vertical_ratio()!=10:
        liste_vertical_ratio.append(gaze.vertical_ratio())
    else:
        liste_vertical_ratio.append(None)
   
    """
	# traitement du regard
		# si regard a gauche
    Regard=None
    if gaze.is_left():  
        Regard="gauche"       				# si regard a gauche
        RegardDroite = 0  					# RAZ RegardDroite
        RegardGauche = RegardGauche + 1		# incremente compteur
        # ~ print("Nb iterations regard gauche:", RegardGauche)		# affiche info dans terminal
        

            
        # si regard a droite
    elif gaze.is_right():	
        Regard="droite"				# si regard a droite
        RegardGauche = 0					# RAZ RegardGauche
        RegardDroite = RegardDroite + 1		# incremente compteur
        # ~ print("Nb iterations regard droite:", RegardDroite)		# affiche info dans terminal
                               


        # si regard au centre         
    elif gaze.is_center():
        #print("Regard au centre")
        RegardDroite = 0					# RAZ Regardroite
        RegardGauche = 0
        Regard="centre"					# RAZ RegardGauche
    """
############## AFFICHAGE ####################    
    frame_redimensionnee = cv2.resize(frame, (largeur_nouvelle, hauteur_nouvelle))
    height, width, _ = frame_redimensionnee.shape 		# releve dimensions de l'image de la webcam
   
    # Définir la place dispo pour les bandes
    WDispo = WEcran - width
    LargeurBandes = int(WDispo/2)
    
    # Créer une image avec des bandes de couleur sur les côtés
    bordered_frame = np.zeros((2*height, WEcran, 3), dtype=np.uint8)
		# height hauteur webcam redimensionnee
		# largeur largeur ecran

    # Ajouter couleur commande envoyee a gauche
    bordered_frame[:, :] = [0,0,0]	
		#  [hauteur , largeur]
		# : toutes les lignes
		# :LargeurBandes       les colonnes depuis le début (:) jusqu'à LargeurBandes
    

    """
    #Ajouter le regard
    Texte = Regard
    Position =(670,70)
    Police = cv2.FONT_HERSHEY_SIMPLEX
    TaillePolice = 1
    CouleurTexte = [0,0,0]
    EpaisseurTexte = 2
    cv2.putText(bordered_frame, Texte, Position, Police, TaillePolice, CouleurTexte, EpaisseurTexte)
    """
    if args.mode=='h':
        # point de gauche
        if t<=1*periode:
            marker_g=t
            cv2.putText(bordered_frame, Texte, Position_c, Police, TaillePolice, CouleurTexte, EpaisseurTexte)
        
        # point de droite
        if t>2*periode:

            cv2.putText(bordered_frame, Texte, Position_d, Police, TaillePolice, CouleurTexte, EpaisseurTexte)

        #point central
        if t>1*periode and t<=2*periode:
            marker_d=t

            cv2.putText(bordered_frame, Texte, Position_g, Police, TaillePolice, CouleurTexte, EpaisseurTexte)

        
        if t>3*periode:

            break
    if args.mode=='hv':

        # point central
        if t<=1*periode:
            marker_hg=t
            Position_c=(WEcran//2, 480)
            cv2.putText(bordered_frame, Texte, Position_c, Police, TaillePolice, CouleurTexte, EpaisseurTexte)

        # point haut gauche
        if t>1*periode and t<=2*periode:
            marker_bg=t
            Position_hg=(20,50)
            cv2.putText(bordered_frame, Texte, Position_hg, Police, TaillePolice, CouleurTexte, EpaisseurTexte) 

        # point de bas gauche
        if t>2*periode and t<=3*periode:
            marker_bd=t
            Position_bg=(20,940)
            cv2.putText(bordered_frame, Texte, Position_bg, Police, TaillePolice, CouleurTexte, EpaisseurTexte)

        # point bas droit
        if t>3*periode and t<=4*periode:
            marker_hd=t
            Position_bd=(WEcran-22, 940)
            cv2.putText(bordered_frame, Texte, Position_bd, Police, TaillePolice, CouleurTexte, EpaisseurTexte)
        
        # point haut droit
        if t>4*periode:
            Position_hd=(WEcran-22, 50)
            cv2.putText(bordered_frame, Texte, Position_hd, Police, TaillePolice, CouleurTexte, EpaisseurTexte)

        if t>5*periode:
            break

    if args.video=='yes':

        # Copier le flux vidéo au centre de l'image
        bordered_frame[height-1:2*height-1, LargeurBandes:LargeurBandes + width] = frame
            #  [hauteur , largeur]    
            # : toutes les lignes
            # LargeurBandes:            colonne de départ
            # :LargeurBandes + width    colonne de fin


    """
    #Ajouter le chrono
    Texte = str(int(100*t)/100)
    Position =(LargeurBandes+width//2,50)
    
    Police = cv2.FONT_HERSHEY_SIMPLEX
    TaillePolice = 1
    CouleurTexte = [255,255,255]
    EpaisseurTexte = 2
    cv2.putText(bordered_frame, Texte, Position, Police, TaillePolice, CouleurTexte, EpaisseurTexte)
    """

    #Ajouter le ratio 
    ratio_showed = str(int(gaze.horizontal_ratio()*100)/100)
    Position =(WEcran//2,150)
    Police = cv2.FONT_HERSHEY_SIMPLEX
    TaillePolice = 1
    CouleurTexte = (255,255,255)
    EpaisseurTexte = 2
    cv2.putText(bordered_frame, ratio_showed, Position, Police, TaillePolice, CouleurTexte, EpaisseurTexte)

    # Afficher l'image
    cv2.imshow ("Test",bordered_frame)  
############## AFFICHAGE ####################         
        
    # Quitter    
    if cv2.waitKey(1) == 27:
        break
    if keyboard.is_pressed("q"):
        break
   
webcam.release()			# Liberation camera
cv2.destroyAllWindows()		# Liberation memoire

# Affichage des courbes

if args.ratio=='h' or args.ratio=='hv':
    plt.plot(liste_temps, liste_horizontal_ratio, label='horizontal ratio')
if args.ratio=='v' or args.ratio=='hv':
    plt.plot(liste_temps, liste_vertical_ratio, label='vertical ratio')
if args.mode=='h':
    plt.axvline(marker_g, color='r', label='regard à gauche' )
    plt.axvline(marker_d, color='b', label="regard à droite" )
if args.mode=='hv':
    plt.axvline(marker_hg, color='r', label='haut gauche')
    plt.axvline(marker_bg, color='b', label='bas gauche')
    plt.axvline(marker_bd, color='cyan', label='bas droit')
    plt.axvline(marker_hd, color='g', label='haut droit')

plt.xlabel('time')
plt.ylim(0,1)
plt.legend()


# Sauvegarde en pdf
plt.savefig('Test.'+ args.mode +'.pdf')

plt.show()
plt.close()