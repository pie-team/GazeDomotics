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
from Basic_Window_Displayer import Basic_Window_Displayer as bwd
import picamera2
import pyautogui
import requests


### VARIABLES GLOBALES ###
height_cam = 480
width_cam = 640
screen_width, screen_height = pyautogui.size()
center_counter = 0
right_counter = 0
left_counter = 0
up_counter = 0
down_counter = 0
retour_etat_centre = 0
retour_etat_droite = 0
retour_etat_gauche = 0
retour_etat_haut = 0
retour_etat_bas = 0
noir = (0, 0, 0)
blanc = (255, 255, 255)
vert = (0, 255, 0)
jaune = (255, 255, 0)
gris = (128, 128, 128)
EpaisseurTexte = 2
Police = cv2.FONT_HERSHEY_SIMPLEX
TaillePolice = 1
frame_counter = 0
delay = 2


def gaze(img):
    url = "http://127.0.0.1:8000/upload-photo/"
    ret, buffer = cv2.imencode('.jpg', img)
    if not ret:
        raise Exception("cv2.imencode failed")
    frame = buffer.tobytes()
    file = {'file': ('image.jpg', frame, "image/jpeg")}
    r = requests.post(url, files=file)
    df = r.json()[0]
    for e in list(df.keys()) : 
        df[e] = float(df[e])
    return df


def GazeIsCenter(data, threshold):

    if abs(data["gaze_angle_x"]) < threshold and abs(data["gaze_angle_y"]) < threshold:
        return True
    else:
        return False

def GazeIsRight(data, threshold):

    if data["gaze_angle_x"] < -threshold:
        return True
    else:
        return False

def GazeIsLeft(data, threshold):

    if data["gaze_angle_x"] > threshold:
        return True
    else:
        return False

def GazeIsUp(data, threshold):

    if data["gaze_angle_y"] < -threshold:
        return True
    else:
        return False
    
def GazeIsDown(data, threshold):

    if data["gaze_angle_y"] > threshold:
        return True
    else:
        return False





if __name__ == "__main__":
    
    picam = picamera2.Picamera2()
    picam.start()
    
    bwd(screen_height, screen_width, "Test", "Regardez la croix qui va apparaitre", blanc, 3000, "center")
    
    data_calib = {"gaze_angle_x": [], "gaze_angle_y": []}
    start_time = time.time()
    
    while time.time() - start_time < 10:
        
        # Create a black image
        frame = np.zeros((screen_height, screen_width, 3), dtype=np.uint8)

        # Define the text and its properties
        text = '+'
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        text_color = blanc
        thickness = 2
        text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
    
        text_x = (frame.shape[1] - text_size[0]) // 2
        text_y = (frame.shape[0] + text_size[1]) // 2

        # Put the text on the image
        cv2.putText(frame, text, (text_x, text_y), font, font_scale, text_color, thickness)
        cv2.putText(frame, str(int(time.time() - start_time )), (text_x, text_y-250), font, font_scale, text_color, thickness)
        # Create a window and display the image
        cv2.namedWindow("Calibration", cv2.WINDOW_NORMAL)
        cv2.setWindowProperty("Calibration", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)  # passe en plein ecran
        cv2.imshow("Calibration", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        img_to_process = picam.capture_array()
        current_data = gaze(img_to_process[:,:,:3])
        print(current_data)
        data_calib["gaze_angle_x"].append(float(current_data["gaze_angle_x"]))
        data_calib["gaze_angle_y"].append(float(current_data["gaze_angle_y"]))
        

    cv2.destroyAllWindows()
    data_calib["gaze_angle_x"] = np.mean(np.array(data_calib["gaze_angle_x"]))
    data_calib["gaze_angle_y"] = np.mean(np.array(data_calib["gaze_angle_y"]))

    bwd(screen_height, screen_width, "Test", "Calibration terminee", blanc, 3000, "center")

    current_action = "center"

    while True:

        last_action=current_action

        if last_action == "center":
            center_counter = 0
        if last_action == "right":
            right_counter = 0
        if last_action == "left":
            left_counter = 0
        if last_action == "up":
            up_counter = 0
        if last_action == "down":
            down_counter = 0

        img_to_process = picam.capture_array()

        gaze_data = gaze(img_to_process[:,:,:3])
        gaze_data["gaze_angle_x"] -= data_calib['gaze_angle_x']
        gaze_data["gaze_angle_y"] -= data_calib['gaze_angle_y']
        
        print(gaze_data)
        
        if GazeIsCenter(gaze_data, 0.05):
            center_counter += 1
            right_counter = 0
            left_counter = 0
            up_counter = 0
            down_counter = 0
            if center_counter >= delay:
                center_counter = 0
                if retour_etat_centre == 0:
                    retour_etat_centre = 1
                    current_action = "center"
                else :
                    retour_etat_centre = 0
                    current_action = "center"

        elif GazeIsRight(gaze_data, 0.05):
            center_counter = 0
            right_counter += 1
            left_counter = 0
            up_counter = 0
            down_counter = 0
            if right_counter >= delay:
                right_counter = 0
                if retour_etat_droite == 0:
                    retour_etat_droite = 1
                    current_action = "right"
                else :
                    retour_etat_droite = 0
                    current_action = "right"
        
        elif GazeIsLeft(gaze_data, 0.05):
            center_counter = 0
            right_counter = 0
            left_counter += 1
            up_counter = 0
            down_counter = 0
            if left_counter >= delay:
                left_counter = 0
                if retour_etat_gauche == 0:
                    retour_etat_gauche = 1
                    current_action = "left"
                else :
                    retour_etat_gauche = 0
                    current_action = "left"
        
        elif GazeIsUp(gaze_data, 0.05):
            center_counter = 0
            right_counter = 0
            left_counter = 0
            up_counter += 1
            down_counter = 0
            if up_counter >= delay:
                up_counter = 0
                if retour_etat_haut == 0:
                    retour_etat_haut = 1
                    current_action = "up"
                else :
                    retour_etat_haut = 0
                    current_action = "up"
        
        elif GazeIsDown(gaze_data, 0.05):
            center_counter = 0
            right_counter = 0
            left_counter = 0
            up_counter = 0
            down_counter += 1
            if down_counter >= delay:
                down_counter = 0
                if retour_etat_bas == 0:
                    retour_etat_bas = 1
                    current_action = "down"
                else :
                    retour_etat_bas = 0
                    current_action = "down"

        if retour_etat_droite == 1:
            couleur_droite = vert
            couleur_texte_droite = jaune
        else:
            couleur_droite = noir
            couleur_texte_droite = gris
        
        if retour_etat_gauche == 1:
            couleur_gauche = vert
            couleur_texte_gauche = jaune
        else:
            couleur_gauche = noir
            couleur_texte_gauche = gris
        
        if retour_etat_haut == 1:
            couleur_haut = vert
            couleur_texte_haut = jaune
        else:
            couleur_haut = noir
            couleur_texte_haut = gris
        
        if retour_etat_bas == 1:
            couleur_bas = vert
            couleur_texte_bas = jaune
        else:
            couleur_bas = noir
            couleur_texte_bas = gris
            

        frame = np.zeros((height_cam, width_cam, 3), dtype=np.uint8)
        frame_redimensionnee = cv2.resize(frame, (screen_width, screen_height))
        # Create a window and display the image
        cv2.namedWindow("Chez Gerard", cv2.WINDOW_NORMAL)
        cv2.setWindowProperty("Chez Gerard", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)  # passe en plein ecran
        cv2.imshow("Chez Gerard", frame_redimensionnee)

        ### Définir la place dispo pour les bandes
        WDispo = screen_width - width_cam
        LargeurBandes = int(WDispo/2)

        HDispo = screen_height - height_cam
        HauteurBandes = int(HDispo/2)
        
        ### Créer une image avec des bandes de couleur sur les côtés

        # Initialisation
        bordered_frame = np.zeros((screen_height, screen_width, 3), dtype=np.uint8)

        # Ajouter couleur commande envoyee a gauche
        bordered_frame[HauteurBandes:screen_height-HauteurBandes, :LargeurBandes] = couleur_gauche
        Texte = "LEFT"
        CouleurTexte = couleur_texte_gauche
        text_size = cv2.getTextSize(Texte, Police, TaillePolice, EpaisseurTexte)[0]
        Position = ((LargeurBandes-text_size[0])//2, (screen_height+text_size[1])//2)
        cv2.putText(bordered_frame, Texte, Position, Police, TaillePolice, CouleurTexte, EpaisseurTexte)
        cv2.putText(bordered_frame, str(int(time.time()-start_time)), (480,150), Police, TaillePolice, CouleurTexte, EpaisseurTexte)
        # Ajouter couleur commande envoyee a droite
        bordered_frame[HauteurBandes:screen_height-HauteurBandes, -LargeurBandes:] = couleur_droite
        Texte = "RIGHT"
        CouleurTexte = couleur_texte_droite
        text_size = cv2.getTextSize(Texte, Police, TaillePolice, EpaisseurTexte)[0]
        Position = ((LargeurBandes-text_size[0])//2+LargeurBandes+width_cam, (screen_height+text_size[1])//2)
        cv2.putText(bordered_frame, Texte, Position, Police, TaillePolice, CouleurTexte, EpaisseurTexte)

        # Ajouter couleur commande envoyee en haut
        bordered_frame[:HauteurBandes, LargeurBandes:screen_width-LargeurBandes] = couleur_haut
        Texte = "UP"
        CouleurTexte = couleur_texte_haut
        text_size = cv2.getTextSize(Texte, Police, TaillePolice, EpaisseurTexte)[0]
        Position = ((screen_width-text_size[0])//2, (HauteurBandes+text_size[1])//2)
        cv2.putText(bordered_frame, Texte, Position, Police, TaillePolice, CouleurTexte, EpaisseurTexte)

        # Ajouter couleur commande envoyee en bas
        bordered_frame[-HauteurBandes:, LargeurBandes:screen_width-LargeurBandes] = couleur_bas
        Texte = "DOWN"
        CouleurTexte = couleur_texte_bas
        text_size = cv2.getTextSize(Texte, Police, TaillePolice, EpaisseurTexte)[0]
        Position = ((screen_width-text_size[0])//2, (HauteurBandes+text_size[1])//2+HauteurBandes+height_cam)
        cv2.putText(bordered_frame, Texte, Position, Police, TaillePolice, CouleurTexte, EpaisseurTexte)

        # Copier le flux vidéo au centre de l'image
        bordered_frame[HauteurBandes:HauteurBandes + height_cam, LargeurBandes:LargeurBandes + width_cam] = img_to_process[:,:,:3]
        
        # Afficher l'image
        cv2.imshow("Chez Gerard", bordered_frame)  

        ############## AFFICHAGE ####################         
            
        # Quitter    
        if cv2.waitKey(1) == 27:
            break
        
    cv2.destroyAllWindows() 
                


        



