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

WF=1056	# largeur image
HF=800	# hauteur image

y_h=19
y_b=HF-20
y_c=HF//2
x_g=19
x_d=WF-20
x_c=WF//2




#cv2.namedWindow("Capture_exp", cv2.WINDOW_NORMAL)				# cree une fenetre redimensionnable

#cv2.resizeWindow("Capture_exp", WF, HF)	# retaille la fenetre

# Période de l'expérience

periode=15.00 #en secondes

# Paramètres constants de textes et couleurs
Texte = "+"
if args.point_pos=='mid':
    Position_c = (x_c,y_c)
    Position_g = (x_g,y_c)
    Position_d = (x_d,y_c)

elif args.pos_point=='up':
    Position_c = (x_c,y_h)
    Position_g = (x_g,y_h)
    Position_d = (x_d,y_h)

elif args.pos_point=='down':
    Position_c = (x_c,y_b)
    Position_g = (x_g,y_b)
    Position_d = (x_d,y_b)  

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
    # releve dimensions de l'image de la webcam
   

    
    # Créer une image avec des bandes de couleur sur les côtés
    bordered_frame = np.zeros((HF, WF, 3), dtype=np.uint8)
		# height hauteur webcam redimensionnee
		# largeur largeur ecran

    # Ajouter couleur commande envoyee a gauche
    bordered_frame[:, :] = [0,0,0]	
		#  [hauteur , largeur]
		# : toutes les lignes
		# :LargeurBandes       les colonnes depuis le début (:) jusqu'à LargeurBandes

    
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
            Position_c=(x_c, y_c)
            cv2.putText(bordered_frame, Texte, Position_c, Police, TaillePolice, CouleurTexte, EpaisseurTexte)

        # point haut gauche
        if t>1*periode and t<=2*periode:
            marker_bg=t
            Position_hg=(x_g,y_h)
            cv2.putText(bordered_frame, Texte, Position_hg, Police, TaillePolice, CouleurTexte, EpaisseurTexte) 

        # point de bas gauche
        if t>2*periode and t<=3*periode:
            marker_bd=t
            Position_bg=(x_g,y_b)
            cv2.putText(bordered_frame, Texte, Position_bg, Police, TaillePolice, CouleurTexte, EpaisseurTexte)

        # point bas droit
        if t>3*periode and t<=4*periode:
            marker_hd=t
            Position_bd=(x_d, y_b)
            cv2.putText(bordered_frame, Texte, Position_bd, Police, TaillePolice, CouleurTexte, EpaisseurTexte)
        
        # point haut droit
        if t>4*periode:
            Position_hd=(x_d, y_h)
            cv2.putText(bordered_frame, Texte, Position_hd, Police, TaillePolice, CouleurTexte, EpaisseurTexte)

        if t>5*periode:
            break


    

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
