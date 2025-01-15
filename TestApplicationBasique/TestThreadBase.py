import threading
import time
import queue

# Fonction à exécuter périodiquement dans le thread
def votre_commande(shared_queue):
    result = "Résultat de la commande"
    shared_queue.put(result)

def run_periodically(interval, stop_event, shared_queue):
    while not stop_event.is_set():
        votre_commande(shared_queue)
        time.sleep(interval)

# Initialisation des variables du programme principal
variable1 = "Valeur initiale de la variable1"
variable2 = 42

# Créer une file pour partager les résultats entre le thread et le programme principal
shared_queue = queue.Queue()

# Intervalle en secondes pour la commande périodique
interval = 2

# Événement pour arrêter le thread
stop_event = threading.Event()

# Création du thread
thread = threading.Thread(target=run_periodically, args=(interval, stop_event, shared_queue))

# Démarrer le thread
thread.start()

# Code principal
try:
    while True:
        # Vérifier s'il y a des résultats dans la file
        while not shared_queue.empty():
            result = shared_queue.get()
            print(f"Résultat reçu du thread: {result}")
            # Utilisation du résultat pour mettre à jour les variables
            variable1 = result
            variable2 += 1
        print("Code principal s'exécute")
        print(f"Variable1: {variable1}")
        print(f"Variable2: {variable2}")
        time.sleep(1)
except KeyboardInterrupt:
    # Arrêter le thread lors d'une interruption (par exemple, Ctrl+C)
    stop_event.set()
    thread.join()

print("Fin du programme principal")
