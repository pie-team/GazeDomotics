from __future__ import division
import os
import cv2
import dlib
from .eye import Eye
from .calibration import Calibration
# ~ from CoefVariation import CalculEcartTypeRelatif
import numpy as np
from collections import deque


class GazeTracking(object):
    """
    This class tracks the user's gaze.
    It provides useful information like the position of the eyes
    and pupils and allows to know if the eyes are open or closed
    """

    def __init__(self):
        self.frame = None
        self.eye_left = None
        self.eye_right = None
        self.calibration = Calibration()
        self.erreur_relative=100.0
        # ~ self.taille_FIFO = Nb_elements *1.0 
        # ~ self.FIFO_ratio = deque(maxlen=Nb_elements)	# cree le FIFO
        self.taille_FIFO = 10 *1.0 
        self.FIFO_ratio = deque(maxlen=10)	# cree le FIFO


        # _face_detector is used to detect faces
        self._face_detector = dlib.get_frontal_face_detector()

        # _predictor is used to get facial landmarks of a given face
        cwd = os.path.abspath(os.path.dirname(__file__))
        model_path = os.path.abspath(os.path.join(cwd, "trained_models/shape_predictor_68_face_landmarks.dat"))
        self._predictor = dlib.shape_predictor(model_path)

    @property
    def pupils_located(self):
        """Check that the pupils have been located"""
        try:
            int(self.eye_left.pupil.x)
            int(self.eye_left.pupil.y)
            int(self.eye_right.pupil.x)
            int(self.eye_right.pupil.y)
            return True
        except Exception:
            return False

    def _analyze(self):
        """Detects the face and initialize Eye objects"""
        frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        faces = self._face_detector(frame)

        try:
            landmarks = self._predictor(frame, faces[0])
            self.eye_left = Eye(frame, landmarks, 0, self.calibration)
            self.eye_right = Eye(frame, landmarks, 1, self.calibration)

        except IndexError:
            self.eye_left = None
            self.eye_right = None

    def refresh(self, frame):
        """Refreshes the frame and analyzes it.

        Arguments:
            frame (numpy.ndarray): The frame to analyze
        """
        self.frame = frame
        self._analyze()

    def pupil_left_coords(self):
        """Returns the coordinates of the left pupil"""
        if self.pupils_located:
            x = self.eye_left.origin[0] + self.eye_left.pupil.x
            y = self.eye_left.origin[1] + self.eye_left.pupil.y
            return (x, y)

    def pupil_right_coords(self):
        """Returns the coordinates of the right pupil"""
        if self.pupils_located:
            x = self.eye_right.origin[0] + self.eye_right.pupil.x
            y = self.eye_right.origin[1] + self.eye_right.pupil.y
            return (x, y)

    def horizontal_ratio(self):
        """Returns a number between 0.0 and 1.0 that indicates the
        horizontal direction of the gaze. The extreme right is 0.0,
        the center is 0.5 and the extreme left is 1.0
        """
        pupil_left = 0.0
        pupil_right = 0.0
        h_ratio = 0.0
        if self.pupils_located:
            pupil_left = self.eye_left.pupil.x / (self.eye_left.center[0] * 2 -5 )     #- 10)
            pupil_right = self.eye_right.pupil.x / (self.eye_right.center[0] * 2 -5 ) #- 10)
            h_ratio = (pupil_left + pupil_right) / 2
            print(" h_ratio : ",h_ratio) 
            # ~ print("type (ligne 92 de gaze_tracking) : ",type(h_ratio))
            # ~ self.erreur_relative.ajout_ratio(ratio_horizontal)	# ajout ratio dans FIFO
            self.ajout_ratio(h_ratio)	# ajout ratio dans FIFO
            self.erreur_relative = self.coefficient_de_variation()	# calcul erreur
            # ~ print("type (ligne 104 de gaze_tracking) : ",type(h_ratio))
            print("erreur_relative (ligne 105 de gaze_tracking) : ",self.erreur_relative)
            return 0.0 #h_ratio #(pupil_left + pupil_right) / 2

    def vertical_ratio(self):
        """Returns a number between 0.0 and 1.0 that indicates the
        vertical direction of the gaze. The extreme top is 0.0,
        the center is 0.5 and the extreme bottom is 1.0
        """
        if self.pupils_located:
            pupil_left = self.eye_left.pupil.y / (self.eye_left.center[1] * 2 - 10)
            pupil_right = self.eye_right.pupil.y / (self.eye_right.center[1] * 2 - 10)
            v_ratio = (pupil_left + pupil_right) / 2
            print(" v_ratio : ",v_ratio)
            return v_ratio  #(pupil_left + pupil_right) / 2

    def is_right(self):
        """Returns true if the user is looking to the right"""
        if self.pupils_located:
            return self.horizontal_ratio() <= 0.45

    def is_left(self):
        """Returns true if the user is looking to the left"""
        if self.pupils_located:
            return self.horizontal_ratio() >= 0.6  #0.65

    def is_center(self):
        """Returns true if the user is looking to the center"""
        if self.pupils_located:
            return self.is_right() is not True and self.is_left() is not True

    def is_blinking(self):
        """Returns true if the user closes his eyes"""
        if self.pupils_located:
            blinking_ratio = (self.eye_left.blinking + self.eye_right.blinking) / 2
            return blinking_ratio > 3.8

    def annotated_frame(self):
        """Returns the main frame with pupils highlighted"""
        frame = self.frame.copy()

        if self.pupils_located:
            color = (0, 255, 0)
            x_left, y_left = self.pupil_left_coords()
            x_right, y_right = self.pupil_right_coords()
            cv2.line(frame, (x_left - 5, y_left), (x_left + 5, y_left), color)
            cv2.line(frame, (x_left, y_left - 5), (x_left, y_left + 5), color)
            cv2.line(frame, (x_right - 5, y_right), (x_right + 5, y_right), color)
            cv2.line(frame, (x_right, y_right - 5), (x_right, y_right + 5), color)

        return frame
        
# ~ class CalculEcartTypeRelatif:
    # ~ def __init__(self, Nb_elements):
        # ~ self.taille_FIFO = Nb_elements *1.0 
        # ~ self.FIFO_ratio = deque(maxlen=Nb_elements)	# cree le FIFO
        # ~ self.erreur_relative=100.0

    def ajout_ratio(self, ratio_entrant):
        # ~ nouveau_ratio = ratio_entrant * 1.0
        self.FIFO_ratio.append(ratio_entrant)		# pousse nouveau ratio dans FIFO
        # ~ self.FIFO_ratio = self.FIFO_ratio[] * 1.0  
        # ~ print("type rdans gaze tracking ajout ratio ligne 167 ) : ",type(self.FIFO_ratio))

    def coefficient_de_variation(self):
        # ~ fin_FIFO = float(self.taille_FIFO)
        # ~ tableau_ratio = np.arange(0.0,fin_FIFO)
        # ~ tableau_ratio = [1.0] * self.taille_FIFO
        if len(self.FIFO_ratio) == 0:				# si pas de donnees
            return float(0.0)  								# on sort pour éviter la division par zéro quand calcul moyenne
        self.tableau_ratio = np.array(self.FIFO_ratio)	# transformation en tableau pour utiliser numpy pour optimiser les calcul
        # ~ print("type  dans gaze tracking coef de variation (ligne 176 : ",type(self.tableau_ratio))        
        self.tableau_ratio = self.tableau_ratio
        mean = np.mean(self.tableau_ratio)				# calcul moyenne
                # ~ print("moyenne (ligne 178 : ",mean)        
        std_dev = np.std(self.tableau_ratio)				# calcul ecart type
                # ~ print("ecart type (ligne 180 : ",std_dev)        
        if mean == 0:								# si moyenne est nulle
            return float(1.0)  								# pour éviter la division par zéro quand calcul ecart type relatif
        return float(std_dev / mean)						# calcul ecart type relatif
           
