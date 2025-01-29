# -*- coding: utf-8 -*-



import time
import numpy as np
import pandas as pd
import os
import cv2
from Commandes import Commande
import subprocess as sp
import multiprocessing as mp
import sys

mode = sys.argv[1] 


def Basic_Window_Displayer(height, width, title, text, text_color=(128,128,128), wait_time=0, mode="center"):

    # Create a black image
    frame = np.zeros((height, width, 3), dtype=np.uint8)

    # Define the text and its properties
    text = text
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    text_color = text_color
    thickness = 2
    text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
    
    if mode == "center":
        text_x = (frame.shape[1] - text_size[0]) // 2
        text_y = (frame.shape[0] + text_size[1]) // 2

    # Put the text on the image
    cv2.putText(frame, text, (text_x, text_y), font, font_scale, text_color, thickness)

    # Create a window and display the image
    cv2.namedWindow(title, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(title, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)  # passe en plein ecran
    cv2.imshow(title, frame)

    cv2.waitKey(wait_time)

if __name__ == "__main__":

    OpenFace = sp.Popen(["bash", "./OpenFace_runner.sh"])

    time.sleep(2)

    if mode == "center":
        Basic_Window_Displayer(1200, 1920, "GazeDomotics", "HEY", wait_time=3000)
        Basic_Window_Displayer(1200, 1920, "GazeDomotics", "SLT", wait_time=3000)
        Basic_Window_Displayer(1200, 1920, "GazeDomotics", "CV?", wait_time=3000)
        Basic_Window_Displayer(1200, 1920, "GazeDomotics", "READY?", wait_time=3000)
        Basic_Window_Displayer(1200, 1920, "GazeDomotics", "RETIENS", wait_time=3000)
        Basic_Window_Displayer(1200, 1920, "GazeDomotics", "LA", wait_time=3000)
        Basic_Window_Displayer(1200, 1920, "GazeDomotics", "SUITE", wait_time=3000)
        Basic_Window_Displayer(1200, 1920, "GazeDomotics", "DE", wait_time=3000)
        Basic_Window_Displayer(1200, 1920, "GazeDomotics", "CHIFFRES", wait_time=3000)
        Basic_Window_Displayer(1200, 1920, "GazeDomotics", "GO", wait_time=3000)
        Basic_Window_Displayer(1200, 1920, "GazeDomotics", "5", wait_time=3000)
        Basic_Window_Displayer(1200, 1920, "GazeDomotics", "8", wait_time=3000)
        Basic_Window_Displayer(1200, 1920, "GazeDomotics", "9", wait_time=3000)
        Basic_Window_Displayer(1200, 1920, "GazeDomotics", "4", wait_time=3000)
        Basic_Window_Displayer(1200, 1920, "GazeDomotics", "7", wait_time=3000)
        Basic_Window_Displayer(1200, 1920, "GazeDomotics", "1", wait_time=3000)
        Basic_Window_Displayer(1200, 1920, "GazeDomotics", "1", wait_time=3000)
        Basic_Window_Displayer(1200, 1920, "GazeDomotics", "FIN", wait_time=3000)

    if mode == "LandR":
        Basic_Window_Displayer(1200, 1920, "GazeDomotics", "HEY", wait_time=3000)
        Basic_Window_Displayer(1200, 1920, "GazeDomotics", "SLT", wait_time=3000)
        Basic_Window_Displayer(1200, 1920, "GazeDomotics", "CV?", wait_time=3000)
        Basic_Window_Displayer(1200, 1920, "GazeDomotics", "READY?", wait_time=3000)
        Basic_Window_Displayer(1200, 1920, "GazeDomotics", "DROITE A FOND >>", wait_time=3000)
        Basic_Window_Displayer(1200, 1920, "GazeDomotics", "| CENTRE |", wait_time=3000)
        Basic_Window_Displayer(1200, 1920, "GazeDomotics", "<< GAUCHE A FOND", wait_time=3000)
        Basic_Window_Displayer(1200, 1920, "GazeDomotics", "| CENTRE |", wait_time=3000)
        Basic_Window_Displayer(1200, 1920, "GazeDomotics", "DROITE A FOND >>", wait_time=3000)
        Basic_Window_Displayer(1200, 1920, "GazeDomotics", "| CENTRE |", wait_time=3000)
        Basic_Window_Displayer(1200, 1920, "GazeDomotics", "<< GAUCHE A FOND", wait_time=3000)
        Basic_Window_Displayer(1200, 1920, "GazeDomotics", "| CENTRE |", wait_time=3000)
        Basic_Window_Displayer(1200, 1920, "GazeDomotics", "DROITE A FOND >>", wait_time=3000)
        Basic_Window_Displayer(1200, 1920, "GazeDomotics", "| CENTRE |", wait_time=3000)
        Basic_Window_Displayer(1200, 1920, "GazeDomotics", "<< GAUCHE A FOND", wait_time=3000)
        Basic_Window_Displayer(1200, 1920, "GazeDomotics", "| CENTRE |", wait_time=3000)
        Basic_Window_Displayer(1200, 1920, "GazeDomotics", "| CENTRE |", wait_time=3000)
        Basic_Window_Displayer(1200, 1920, "GazeDomotics", "FIN", wait_time=3000)

    cv2.destroyAllWindows()

    sp.call(["kill", str(OpenFace.pid + 1)])