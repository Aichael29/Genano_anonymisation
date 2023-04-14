import configparser
import os
import threading
import time
from annony import *
import psutil


# Obtenir l'utilisation de la mémoire avant l'exécution du code
memory_before = psutil.virtual_memory().used

# Obtenir l'utilisation de la CPU avant l'exécution du code
cpu_before = psutil.cpu_percent()
start=time.time()

# Lecture du fichier de configuration
config = configparser.ConfigParser()
config.read('configuration.conf')

# Opération à effectuer
operation = config['Operations']['operation']
sep = config['Operations'].get('separateur', None)
if sep is None or len(sep) == 0:
    sep = ','

# Mode de chiffrement (ECB ou CBC)
mode_chiffrement = config['Operations']['mode_chiffrement']

# Colonnes à crypter
colonnes = config['Operations'].get('colonnes', None)
if colonnes is None:
    colonnes = []

# Clé de chiffrement
cle_chiffrement = config['Operations']['cle_chiffrement']

# Vecteur d'initialisation
vecteur = config['Operations']['vector']

# Charger le fichier Excel dans un dataframe Pandas
fichier_entree = config['fileinfo']['fichier_entree']

# Charger le fichier Excel dans un dataframe Pandas
fichier_sortie = config['fileinfo']['fichier_sortie']

type=os.path.splitext(fichier_entree)[1].lower()

# Vérifier si la clé a la bonne taille
if len(cle_chiffrement) != 16:
    print("La clé doit être de 16 caractères.")
    exit()

# Vérifier si le mode de chiffrement est valide
if mode_chiffrement not in ('ECB', 'CBC'):
    print("Le mode de chiffrement doit être soit ECB ou CBC.")
    exit()

# Vérifier si le vecteur d'initialisation a la bonne taille
if mode_chiffrement == 'CBC' and len(vecteur) != 16:
    print("Le vecteur d'initialisation doit être de 16 octets.")
    exit()

encrypt_file(type,fichier_entree,fichier_sortie, operation, cle_chiffrement,mode_chiffrement,vecteur,colonnes,sep)

#print(nb_threads)
end=time.time()
# Obtenir l'utilisation de la CPU après l'exécution du code
cpu_after = psutil.cpu_percent()

# Obtenir l'utilisation de la mémoire après l'exécution du code
memory_after = psutil.virtual_memory().used

# Calculer la différence d'utilisation de la mémoire
memory_diff = (memory_after - memory_before) / 1000000000


# Afficher les résultats
print("Utilisation de la CPU avant l'exécution du code :", cpu_before, "%")
print("Utilisation de la CPU après l'exécution du code :", cpu_after, "%")
print("Différence d'utilisation de la mémoire :", memory_diff, "Go")
print("le fichier est généré en " + str(end - start) + " secondes")
print("le fichier est généré en " + str((end - start)/60) + " secondes")