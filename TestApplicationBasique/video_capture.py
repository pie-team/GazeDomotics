import cv2
import argparse
import pyautogui
import time
import numpy as np
# Arguments

parser=argparse.ArgumentParser()

parser.add_argument('name', type=str)
parser.add_argument('--mode', type=str, default='h', help='h, v, hv')
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
screen_width, screen_height = pyautogui.size()				# relever les dimensions de l'écran
window_height = 2*HF											# definir la hauteur de la fenêtre 
# ~ cv2.namedWindow("Chez Gérard", cv2.WND_PROP_FULLSCREEN)		# cree une fenetre
WEcran, screen_height = pyautogui.size()				# relever les dimensions de l'écran
											
cv2.namedWindow("Capture_exp", cv2.WND_PROP_FULLSCREEN)				# cree une fenetre redimensionnable
cv2.setWindowProperty("Capture_exp", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)  # passe en plein ecran
cv2.resizeWindow("Capture_exp", screen_width, screen_height)	# retaille la fenetre

# Période de l'expérience

periode=15.00 #en secondes

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

# Ouvrir la webcam (0 pour la première webcam, 1 pour une deuxième, etc.)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,WF)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HF)


# Vérifier si la webcam est accessible
if not cap.isOpened():
    print("Erreur : Impossible d'accéder à la webcam.")
    exit()

# Définir le codec et créer un objet VideoWriter
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec pour le format .avi
out = cv2.VideoWriter(args.name + '.mp4', fourcc, 25.0, (640, 480))



start=time.time()
while True:
    t=time.time()-start

    # Lire une frame de la webcam
    ret, frame = cap.read()
    
    if not ret:
        print("Erreur : Impossible de lire la vidéo.")
        break
    
    ############## AFFICHAGE ####################    
    frame_redimensionnee = cv2.resize(frame, (largeur_nouvelle, hauteur_nouvelle))
    height, width, _ = frame_redimensionnee.shape 		# releve dimensions de l'image de la webcam
   
    # Définir la place dispo pour les bandes
    WDispo = WEcran - width
    LargeurBandes = int(WDispo/2)
    
    # Créer une image avec des bandes de couleur sur les côtés
    bordered_frame = np.zeros((screen_height, WEcran, 3), dtype=np.uint8)
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

    '''   
     #Ajouter le chrono
    Chrono = str(int(100*t)/100)
    Position =(width//2, height//2)
    
    Police = cv2.FONT_HERSHEY_SIMPLEX
    TaillePolice = 1
    CouleurChrono = [0,0,0]
    EpaisseurTexte = 2
    cv2.putText(frame, Chrono, Position, Police, TaillePolice, CouleurChrono, EpaisseurTexte)
    '''

    # Écrire la frame dans le fichier de sortie
    out.write(frame)
    cv2.imshow("Capture expé", bordered_frame)
    # Quitter si l'utilisateur appuie sur 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libérer les ressources
cap.release()
out.release()
cv2.destroyAllWindows()
