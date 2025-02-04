import cv2
import imageio
import argparse
import pyautogui
import time
import numpy as np
# Arguments

parser=argparse.ArgumentParser()

parser.add_argument('name', type=str)
parser.add_argument('--mode', type=str, default='h', help='h, v, hv, h2')
parser.add_argument('--point_pos', type=str, default='mid', help='point position up mid down/ doesn t match well with video feedback ')
parser.add_argument('--axes', type=str, default='yes', help='axes instead of points')


args=parser.parse_args()

# Paramètres image
(WF,HF)=pyautogui.size()

'''
WF=1056	# largeur image
HF=800	# hauteur image
'''
y_h=19
y_b=HF-21
y_c=HF//2
x_g=19
x_d=WF-21
x_c=WF//2-1




cv2.namedWindow("Capture_exp", cv2.WINDOW_NORMAL)				# cree une fenetre redimensionnable
cv2.setWindowProperty("Capture_exp", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
#cv2.resizeWindow("Capture_exp", WF, HF)	# retaille la fenetre

# Période de l'expérience

periode=5.00 #en secondes

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


output=str(args.name + '.mp4')

out = imageio.get_writer(output, fps=20.0)





if args.mode=='h2': # mode 'point glissant' un point avance en ligne de step pixels toutes les T ms Rq: 0.01 deg (gaze_angle) ~ 64 pixels
    
    step=5 # idéalement diviseur de WF 
    T=8e-4 #période en ms
    
    start_points=[(x_c, y_b), (x_c, y_c), (x_c, y_h)]


    
    for j in range(len(start_points)):
        (x,y)=start_points[j]
        point=(x,y)

        for i in range(2):
            start=time.time()
            while True: # une itération pour le changement de direction
                t=time.time()-start
        
                
                bordered_frame = np.zeros((HF, WF, 3), dtype=np.uint8)
    
                bordered_frame[:, :] = [0,0,0]	# image noire
                if t>=2:
                    x+=step
                    point=(x, y)
                    if x>=WF-10: # quand le point arrive en bord droit on inverse la course
                        step=-step
                        x+=step
                        point=(x, y)
                    if x<=10: # quand le point arrive en bord gauche on réinverse
                        step=-step
                        x+=step
                        point=(x, y)
                    
                

                cv2.putText(bordered_frame, Texte, point, Police, TaillePolice, CouleurTexte, EpaisseurTexte)
                cv2.imshow("Capture_exp", bordered_frame)
                
                # Lire une frame de la webcam
                ret, frame = cap.read()
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                if not ret:
                    print("Erreur : Impossible de lire la vidéo.")
                    break
                            # Écrire la frame dans le fichier de sortie
                out.append_data(frame)
                
                
                # Quitter si l'utilisateur appuie sur 'q'
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                
                if x==x_c and t>=2:
                    break
                else:
                    time.sleep(T)
    
if args.mode in ['h', 'hv']:
    start=time.time()
    while True:
        t=time.time()-start

        # Lire une frame de la webcam
        ret, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
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
            out.append_data(frame)
            cv2.imshow("Capture_exp", bordered_frame)
            
            # Quitter si l'utilisateur appuie sur 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

# Libérer les ressources
cap.release()
out.close()
cv2.destroyAllWindows()
