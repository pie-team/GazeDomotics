import cv2
from gaze_tracking import GazeTracking
import time
import numpy as np
from openpyxl import Workbook
import pandas as pd
import pyautogui
import Commandes


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

# ~ largeur_nouvelle = WF*1	# nouvelle largeur image 1920pb 3200ok  x2pb  x3pb  x4pb  x5ok
# ~ hauteur_nouvelle = HF*1	# nouvelle hauteur image   x2pb   x3pb   x4pb  x5pb
ratio_horizontal = 0.0
erreur_relative = 0.0

webcam = cv2.VideoCapture(0)
# ~ gaze = GazeTracking()
# ~ webcam = cv2.VideoCapture(0)
time.sleep(1)
webcam.set(cv2.CAP_PROP_FRAME_WIDTH,WF)			# defini largeur capture video
webcam.set(cv2.CAP_PROP_FRAME_HEIGHT,HF)		# defini hauteur capture video
time.sleep(1)

gaze = GazeTracking()			# lance tracker

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
    
    if gaze.is_blinking():
        text = "Clignotement"
        # ~ liste_oeil_ferme.append(1)
    elif gaze.is_right():
        text = "Regard à droite"
        Commandes.Centre_allumer()
        
        print("")
        print(text)
        print("")
    elif gaze.is_left():
        text = "Regard à gauche"
        print("")
        print("regard a gauche")
        print("")
    elif gaze.is_center():
        text = "Regard au centre"
    # ~ else:
        # ~ liste_oeil_ferme.append(0)
        
# ~ ###############   AFFICHAGE INFOS  #############################
    # ~ left_pupil = gaze.pupil_left_coords()		# recup coordonnées pupille gauche
    # ~ right_pupil = gaze.pupil_right_coords()		# recup coordonnées pupille droite
    # ~ cv2.putText(frame, "Pupille gauche:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)	# affiche coordonnées pupille gauche
    # ~ cv2.putText(frame, "Pupille droite: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)	# affiche coordonnées pupille droite
# ~ ###############   AFFICHAGE INFOS  #############################

# ~ ###############   ESTIMATION RATIO A APPLIQUER   ################## 
    # ~ ratio_horizontal = gaze.horizontal_ratio()	# releve ratio
    # ~ erreur_relative = gaze.coefficient_de_variation()
    # ~ cv2.putText(frame, "ratio " + str(ratio_horizontal), (90, 200), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    # ~ cv2.putText(frame, "Erreur relative: " + str(erreur_relative), (90, 230), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
# ~ ###############   ESTIMATION RATIO A APPLIQUER   ################## 

# ~ ###############  CREATION DES REPERES POUR POSITIONNEMENT DE LA TETE  ################## 
    # ~ cv2.line(frame, (0, int(HF/2)-20), (WF,int(HF/2)-20),(0,255,0))
    # ~ cv2.line(frame, (int(WF/2), 0), (int(WF/2),HF),(0,255,0))
    # ~ cv2.circle(frame,(320,240),100,(0,255,0),6)
# ~ ###############  CREATION DES REPERES POUR POSITIONNEMENT DE LA TETE  ################## 

############# CREER LA FENETRE DE COMMANDE   #######################
    # Définir la place dispo pour les bandes (percues comme boutons de commandes)
    # ~ WDispo = WEcran - width
    WDispo = screen_width - width
    LargeurBandes = int(WDispo/2)
    ## ~ print(" hauteur bandes: ",height)
    ## ~ LargeurBandes = 300
    ## ~ width = 700
    #print("Largeur bandes :", LargeurBandes)
    
    # Créer une fenetre composée d'une matrice
    fenetre_commande = np.zeros((height, WEcran, 3), dtype=np.uint8)
    # np.zeros matrice numpy remplie de zeros (couleur noire)
    # height nb de lignes (nb lignes webcam)
    # largeur nb de colonnes (nb de colonnes de l'écran)
    # 3 couches de profondeur, 1 pour chacune des couleurs BGR
    # type matrice numpy en entier non signé 8 bits
    
    # Placer la bande bleue à gauche
    fenetre_commande[:, :LargeurBandes] = [255, 0, 0]  # Couleur bleue (BGR)
    #  [hauteur , largeur]
    # :, toutes les lignes
    # :LargeurBandes       les colonnes depuis le début (:) jusqu'à LargeurBandes

    # Placer la bande rouge à droite
    fenetre_commande[:, -LargeurBandes:] = [0, 0, 255]  # Couleur rouge (BGR)
    #  [hauteur , largeur]    
    # :, toutes les lignes
    # -LargeurBandes:       les colonnes depuis la fin (:) en remontant de LargeurBandes
    
    # Placer le flux vidéo au centre de la fenetre
    fenetre_commande[:, LargeurBandes:LargeurBandes + width] = frame
    # ~ #  [hauteur , largeur]    
    # ~ # : toutes les lignes
    # ~ # LargeurBandes:            colonne de départ
    # ~ # :LargeurBandes + width    colonne de fin
############## CREER FENETRE DE COMMANDE ####################    
    
#############  AFFICHAGE FENETRE DE COMMANDE  ####################
    # Afficher l'image
    cv2.imshow("Chez Gérard", fenetre_commande)
    # ~ xx = 40
    # ~ yy = 400
    # ~ cv2.moveWindow(LaFenetre, xx, yy)
    # ~ cv2.moveWindow('Chez Gérard', 200, 200) # NE FONCTIONNE PAS
    # ~ cv2.resizeWindow("Chez Gérard", screen_width, window_height)	# retaille la fenetre
#############  AFFICHAGE FENETRE DE COMMANDE  ####################

###########   ENREGISTREMENT DES MESURES    ###################	
    liste_erreur_relative.append(gaze.erreur_relative) # ajout de la derniere erreur a la liste
    liste_horizontal_ratio.append(gaze.ratio)			# ajout du dernier ratio horizontal a la liste
    liste_pupilles_detectees.append(gaze.pupilles_detectees)
    liste_oeil_ferme.append(gaze.oeil_ferme)
###########   ENREGISTREMENT DES MESURES    ###################	

    if cv2.waitKey(1) == 27:
        break
   
webcam.release()
cv2.destroyAllWindows()

# ~ AJOUTER REGARD A GAUCHE, AU CENTRE, A DROITE DANS gaze_tracking.py AU MEME ENDROIT QUE LES AUTRES

###############  SAUVEGARDE DES MESURES  ######################
# Convertir les listes en DataFrame
df = pd.DataFrame({
    "Ratio": liste_horizontal_ratio,
    "Erreur (%)": liste_erreur_relative,
    "Detection pupilles": liste_pupilles_detectees,
    "Oeil ferme": liste_oeil_ferme
})

# Écrire le DataFrame dans un fichier Excel
df.to_excel("MesuresRegardTestAppli.xlsx", index=False, engine='openpyxl')
###############  SAUVEGARDE DES MESURES  ######################

# ~ ###############   SAUVEGARDE DES MESURES TRAITEES    #################
# ~ DonneesTraitees = df[df['Erreur (%)'] < 0.25]
# ~ # Écrire le DataFrame dans un fichier Excel
# ~ DonneesTraitees.to_excel("MesuresRegardTestAppliTraitees.xlsx", index=False, engine='openpyxl')
# ~ ###############   SAUVEGARDE DES MESURES TRAITEES    #################


# ~ # Définir les options d'importation et importer les données pour MesuresRegardTest
# ~ chemin_du_fichier = "~/jef/MesuresRegardTest.xlsx"
# ~ RecupDonneesXL = pd.read_excel(
    # ~ chemin_du_fichier,
    # ~ sheet_name="Sheet1",
    # ~ usecols="A:D",
    # ~ skiprows=1,
    # ~ nrows=679,
    # ~ names=["Ratio", "Erreur", "DetectionPupilles", "OeilFerme"],
    # ~ dtype={"Ratio": float, "Erreur": float, "DetectionPupilles": float, "OeilFerme": float}
# ~ )

# ~ RecupDonnees = RecupDonneesXL.values	# Conversion du DataFrame en matrice NumPy

RecupDonnees = df.values	# Conversion du DataFrame en matrice NumPy

# Supprimer les 60 premieres mesures soit environ 2 secondes
RecupDonnees = RecupDonnees[60:]

# Garde les donnees dont l'erreur relative est inferieure a 0.25 dans MoyenneMobile
index = RecupDonnees[:, 1] < 0.25
MoyenneMobile = RecupDonnees[index].copy()
toto = len(RecupDonnees)
print("Nb valeurs initiales dans RecupDonnees:",toto)
toto = len(MoyenneMobile)
print("Nb valeurs gardees pour calcul MoyenneMobile:",toto)

# Suppression des 3eme et 4eme colonnes
col_index = 2  						# Indice de la colonne à supprimer pour supprimer la troisieme colonne (indice 2)
MoyenneMobile = np.delete(MoyenneMobile, col_index, axis=1)		# Suppression de la colonne
MoyenneMobile = np.delete(MoyenneMobile, col_index, axis=1)		# Suppression de la colonne

# Enregistre moyenne mobile sur 'NbValeurs' dans colonne 2
NbValeurs = 20  # 60
MoyenneMobile[:, 1] = pd.Series(MoyenneMobile[:, 0]).rolling(NbValeurs).mean()

# Recopier les premières valeurs pour éviter les NaN du debut
for i in range(NbValeurs- 1):
    MoyenneMobile[i,1] = MoyenneMobile[i, 0]

# Recherche des donnees composants les fronts
NbDonnees = len(MoyenneMobile[:, 0])  # Nb de donnees brutes

MoyenneMobile = np.hstack((MoyenneMobile, np.zeros((NbDonnees, 1))))  # ajoute une colonne de 0 en colonne 3

# Recherche indices pour indentifier debut de fronts
for i in range(NbDonnees - NbValeurs + 1):					# i debute à 0
    ValeursFenetre = MoyenneMobile[i:i + NbValeurs, 1]		# releve les donnees de la fenetre glissante sur la colonne 1 (moyenne mobile des donnees brutes)
    # pour front montant
    if np.all(np.diff(ValeursFenetre) > 0):		# si toutes les valeurs de la fenetre glissante sont croissantes
        MoyenneMobile[i, 2] = 1  				# recoit 1 dans colonne 2 pour indentifier les donnees composants le front montant pour debut front montant
    # pour front descendant
    elif np.all(np.diff(ValeursFenetre) < 0):	#  si toutes les valeurs de la fenetre glissante sont decroissantes
        MoyenneMobile[i, 2] = 2  				# recoit 2 dans colonne 2 pour indentifier les donnees composants le front descendant pour debut front descendant

# Recherhce indices pour indentifier fin de fronts
for i in range(NbValeurs, NbDonnees - NbValeurs):
    ValeursFenetre = MoyenneMobile[i - NbValeurs + 1:i + 1, 1]
    # pour front montant
    if np.all(np.diff(ValeursFenetre) > 0):		# si toutes les valeurs de la fenetre glissante sont croissantes
        MoyenneMobile[i, 2] = 3  				# recoit 3 pour indentifier les donnees composants le front montant pour fin front montant
    # pour front descendant
    elif np.all(np.diff(ValeursFenetre) < 0):	# recoit 2 pour indentifier les donnees composants le front descendant pour debut front descendant
        MoyenneMobile[i, 2] = 4  				# recoit 4 pour indentifier les donnees composants le front descendant pour fin front descendant

# Trouver les indices des donnees composants les fronts
indices_1 = np.where(MoyenneMobile[:, 2] == 1)[0]  # extrait les donnees composants un front montant pour detecter debut front montant
indices_2 = np.where(MoyenneMobile[:, 2] == 2)[0]  # extrait les donnees composants un front descendant pour detecter debut front descendant
indices_3 = np.where(MoyenneMobile[:, 2] == 3)[0]  # extrait les donnees composants un front montant pour detecter fin front montant
indices_4 = np.where(MoyenneMobile[:, 2] == 4)[0]  # extrait les donnees composants un front descendant pour detecter fin front descendant

# Identifier les indices de debut et fin des fronts
indices_1_retenus = []
indices_2_retenus = []
indices_3_retenus = []
indices_4_retenus = []

# Indice1 debut fronts montants
NbIndices_1 = len(indices_1)
j = 0
indices_1_retenus.append(indices_1[0])
for i in range(NbIndices_1 - 1):
    if indices_1[i + 1] == indices_1[i] + 1:
        indices_1_retenus[j] = indices_1[i + 1]
    if (indices_1[i + 1] - indices_1[i] + 1) > NbValeurs:
        indices_1_retenus[j] = indices_1[i]
        j += 1
        indices_1_retenus.append(indices_1[i + 1])

# Indice2 debut fronts descendants
NbIndices_2 = len(indices_2)
j = 0
indices_2_retenus.append(indices_2[0])
for i in range(NbIndices_2 - 1):
    if indices_2[i + 1] == indices_2[i] + 1:
        indices_2_retenus[j] = indices_2[i + 1]
    if (indices_2[i + 1] - indices_2[i] + 1) > NbValeurs:
        indices_2_retenus[j] = indices_2[i]
        j += 1
        indices_2_retenus.append(indices_2[i + 1])

# Indice3 fins front montants
NbIndices_3 = len(indices_3)
j = 0
indices_3_retenus.append(indices_3[0])
for i in range(NbIndices_3 - 1):
    if (indices_3[i] - indices_3_retenus[j]) > NbValeurs:
        j += 1
        indices_3_retenus.append(indices_3[i])

# Indice4 fin fronts descendants
NbIndices_4 = len(indices_4)
j = 0
indices_4_retenus.append(indices_4[0])
for i in range(NbIndices_4 - 1):
    if (indices_4[i] - indices_4_retenus[j]) > NbValeurs:
        j += 1
        indices_4_retenus.append(indices_4[i])

# Verif presence premier front montant
if indices_2_retenus[0] < indices_1_retenus[0]:
    indices_1_retenus.insert(0, 2)
    indices_3_retenus.insert(0, 4)
# Verif presence dernier front montant
if indices_4_retenus[-1] > indices_1_retenus[-1]:
    indices_1_retenus.append(NbDonnees - 20)

# Chercher les plateaux
# Regards a gauche : debute par front montant termine par front descendant
RegardExterieurGauche = MoyenneMobile[indices_3_retenus[0]:indices_2_retenus[0], 1]
RegardInterieurGauche = MoyenneMobile[indices_3_retenus[1]:indices_2_retenus[1], 1]

# Regards a droite : debute par front descendant termine par front montant
RegardExterieurDroite = MoyenneMobile[indices_4_retenus[0]:indices_1_retenus[1], 1]
RegardInterieurDroite = MoyenneMobile[indices_4_retenus[1]:indices_1_retenus[2], 1]

# Calcul des bornes
BorneRegardExterieurGauche = np.mean(RegardExterieurGauche)  # moyenne plateau RegardExterieurGauche
BorneRegardInterieurGauche = np.mean(RegardInterieurGauche)  # moyenne plateau RegardInterieurGauche
BorneRegardExterieurDroite = np.mean(RegardExterieurDroite)  # moyenne plateau RegardExterieurDroite
BorneRegardInterieurDroite = np.mean(RegardInterieurDroite)  # moyenne plateau RegardInterieurDroite

# Affiche les bornes calculees
print("BorneRegardExterieurGauche:",BorneRegardExterieurGauche)
print("BorneRegardInterieurGauche:",BorneRegardInterieurGauche)
print("BorneRegardExterieurDroite:",BorneRegardExterieurDroite)
print("BorneRegardInterieurDroite:",BorneRegardInterieurDroite)


