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
from Basic_Window_Displayer import Basic_Window_Displayer as bwd
import pyautogui

mode = sys.argv[1] # "center", "LandR", "UandD", "+"
size = pyautogui.size()

if __name__ == "__main__":

    OpenFace = sp.Popen(["bash", "./OpenFace_runner.sh"])

    time.sleep(2)

    if mode == "center":
        bwd(1200, 1920, "GazeDomotics", "HEY", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "SLT", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "CV?", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "READY?", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "RETIENS", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "LA", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "SUITE", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "DE", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "CHIFFRES", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "GO", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "5", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "8", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "9", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "4", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "7", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "1", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "1", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "FIN", wait_time=3000)

    if mode == "LandR":
        bwd(1200, 1920, "GazeDomotics", "HEY", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "SLT", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "CV?", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "READY?", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "DROITE A FOND >>", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "| CENTRE |", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "<< GAUCHE A FOND", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "| CENTRE |", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "DROITE A FOND >>", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "| CENTRE |", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "<< GAUCHE A FOND", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "| CENTRE |", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "DROITE A FOND >>", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "| CENTRE |", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "<< GAUCHE A FOND", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "| CENTRE |", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "| CENTRE |", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "FIN", wait_time=3000)

    if mode == "UandD":
        bwd(1200, 1920, "GazeDomotics", "HEY", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "SLT", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "CV?", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "READY?", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "HAUT A FOND >>", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "| CENTRE |", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "<< BAS A FOND", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "| CENTRE |", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "HAUT A FOND >>", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "| CENTRE |", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "<< BAS A FOND", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "| CENTRE |", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "HAUT A FOND >>", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "| CENTRE |", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "<< BAS A FOND", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "| CENTRE |", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "| CENTRE |", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "FIN", wait_time=3000)

    if mode == "+":
        bwd(1200, 1920, "GazeDomotics", "HEY", wait_time=1000)
        bwd(1200, 1920, "GazeDomotics", "SLT", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "CV?", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "READY?", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "+", wait_time=3000, mode="location", location=(size[0]-20, size[1]-20))
        bwd(1200, 1920, "GazeDomotics", "| CENTRE |", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "+", wait_time=3000, mode="location", location=(1900, 20))
        bwd(1200, 1920, "GazeDomotics", "| CENTRE |", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "+", wait_time=3000, mode="location", location=(960, 20))
        bwd(1200, 1920, "GazeDomotics", "| CENTRE |", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "+", wait_time=3000, mode="location", location=(20, 20))
        bwd(1200, 1920, "GazeDomotics", "| CENTRE |", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "+", wait_time=3000, mode="location", location=(20, 600))
        bwd(1200, 1920, "GazeDomotics", "| CENTRE |", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "+", wait_time=3000, mode="location", location=(20, 1180))
        bwd(1200, 1920, "GazeDomotics", "| CENTRE |", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "+", wait_time=3000, mode="location", location=(960, 1180))
        bwd(1200, 1920, "GazeDomotics", "| CENTRE |", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "+", wait_time=3000, mode="location", location=(1900, 1180))
        bwd(1200, 1920, "GazeDomotics", "| CENTRE |", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "+", wait_time=3000, mode="location", location=(1900, 600))
        bwd(1200, 1920, "GazeDomotics", "| CENTRE |", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "+", wait_time=3000, mode="location", location=(1900, 20))
        bwd(1200, 1920, "GazeDomotics", "| CENTRE |", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "+", wait_time=3000, mode="location", location=(960, 20))
        bwd(1200, 1920, "GazeDomotics", "| CENTRE |", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "+", wait_time=3000, mode="location", location=(20, 20))
        bwd(1200, 1920, "GazeDomotics", "| CENTRE |", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "+", wait_time=3000, mode="location", location=(20, 600))
        bwd(1200, 1920, "GazeDomotics", "| CENTRE |", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "+", wait_time=3000, mode="location", location=(20, 1180))
        bwd(1200, 1920, "GazeDomotics", "| CENTRE |", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "+", wait_time=3000, mode="location", location=(960, 1180))
        bwd(1200, 1920, "GazeDomotics", "| CENTRE |", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "+", wait_time=3000, mode="location", location=(1900, 1180))
        bwd(1200, 1920, "GazeDomotics", "| CENTRE |", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "| CENTRE |", wait_time=3000)
        bwd(1200, 1920, "GazeDomotics", "FIN", wait_time=3000)

    cv2.destroyAllWindows()

    sp.call(["kill", str(OpenFace.pid + 1)])