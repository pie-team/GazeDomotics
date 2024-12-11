import subprocess

class Commande:
    """Cette class contient différentes commandes
    """
    def __init__(self)->None:
        pass

    
    def Centre_allumer(self)->None:
        """Pour permettre d'envoyer la commande sur le groupe 6/0/8 pour allumer 
        """
        # ~ print("Centre")
        try: 
            subprocess.getoutput('knxtool groupswrite ip: 6/0/8 1')
            print("Envoi commande allume centre salon")
        except:
            print("Bus non connecte")
            pass
            
    def Centre_eteindre(self)->None:
        """Méthode qui permet d'envoyer la commande sur le groupe 6/0/8 pour éteindre 
        """
        # ~ print("Centre")
        try:
            subprocess.getoutput('knxtool groupswrite ip: 6/0/8 0')
            print("Envoi commande eteint centre salon")
        except:
            print("Bus non connecte")
            pass
 
    
    def SAM_allumer(self)->None:
        """Méthode qui permet d'envoyer la commande sur le groupe 6/0/9 pour allumer
        """
        try:
            subprocess.getoutput('knxtool groupswrite ip: 6/0/9 1')
            print("Envoi commande allume SaM")
        except:
            print("Bus non connecte")
            pass
    
    def SAM_eteindre(self)->None:
        """Méthode qui permet d'envoyer la commande sur le groupe 6/0/9 pour eteindre
        """
        try:
            subprocess.getoutput('knxtool groupswrite ip: 6/0/9 0')
            print("Envoi commande eteint SaM")
        except:
            print("Bus non connecte")
            pass

    

    
    
