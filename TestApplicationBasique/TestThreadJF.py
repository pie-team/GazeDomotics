# le thread est execute toutes les 2 secondes et met a jour variable1
# le programme principal met a jour variable2 et a une attente de 1 seconde
# donc variable2 est mis a jour 2 fois plus souvent que variable1

import threading	# pip install ?
import time
import queue	# pip install ?
# ~ import keyboard  # pip install keyboard

# Fonction executee dans le thread
def CommandeDuThread(FilePartagee):
    # ~ resultat = "Résultat de la commande du thread"
    resultat = variable1 + 1
    FilePartagee.put(resultat)

# Fonction executee periodiquement (thread)
def ExecutionPeriodique(PeriodeExecutionThread, ConditionArretThread, FilePartagee):
		# PeriodeExecutionThread : periode execution en secondes
		# ConditionArretThread : evenement a definir pour arret le thread
		# FilePartagee : file d'attente entre le thread et le programme principal
    while not ConditionArretThread.is_set():	# tant que la condition d'arret n'existe pas
        CommandeDuThread(FilePartagee)			# execute la fonction CommandeDuThread
        time.sleep(PeriodeExecutionThread)		# mise en attente de duree PeriodeExecutionThread

# Initialisation des variables du programme principal
# ~ variable1 = "Valeur initiale de la variable1"
variable1 = 1
variable2 = 42

# Créer une file pour partager les résultats entre le thread et le programme principal
FilePartagee = queue.Queue()

# Intervalle en secondes pour executer commande du thread
PeriodeExecutionThread = 2

# Cree un objet evenement pour arrêter le thread initialement de valeur non definie 
ConditionArretThread = threading.Event()	# mecanisme de synchro 

# Création du thread
thread = threading.Thread(target=ExecutionPeriodique, args=(PeriodeExecutionThread, ConditionArretThread, FilePartagee))
		# thread : objet de type threading
		# target=ExecutionPeriodique : fonction execute par l'objet thread
		# args=(PeriodeExecutionThread, ConditionArretThread, FilePartagee) : arguments de la fonction execute par l'objet thread
		#		PeriodeExecutionThread : periode en secondes
		#		ConditionArretThread : condition d'arret du thread
		#		FilePartagee : file d'attente pour echange entre thread et programme principal
		
# Démarrer le thread
thread.start()

# Code principal
try:
    while True:
        # Vérifier s'il y a des résultats dans la file
        while not FilePartagee.empty():		# tant que la file n'est pas vide
            result = FilePartagee.get()		# resulta recoit la valeur de la file d'attente
            print(f"Résultat reçu du thread: {result}")		# affichage
            # Utilisation du résultat pour mettre à jour les variables
            variable1 = result				# variable1 recoit valeur de la file d'attente
            variable2 += 1					# incremente variable2
        print("Code principal s'exécute")
        print(f"Variable1: {variable1}")
        print(f"Variable2: {variable2}")
        time.sleep(1)						# attente 1 seconde
        
        ###############  A VERIFIER  ###################
        # ~ if keyboard.is_pressed('esc'):
			# ~ ConditionArretThread.set()	# defini evenement d'arret
			# ~ break
        ###############  A VERIFIER  ###################

except KeyboardInterrupt:
    # Arrêter le thread lors d'une interruption (par exemple, Ctrl+C)
    ConditionArretThread.set()	# indique que l'evenement est defini provoquera arret thread
    thread.join()		# attendre que le thread se termine avant de quitter le programme principal

print("Fin du programme principal")
