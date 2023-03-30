import configparser
import sys
import time
from annony import aes_encrypt , aes_decrypt, sha256_hash
import pandas as pd

start=time.time()
# Lecture du fichier de configuration
config = configparser.ConfigParser()
config.read('configuration.conf')

# Opération à effectuer
operation = config['Operations']['operation']


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
df = pd.read_excel(fichier_entree)

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



# Appliquer la fonction de decryptage à chaque colonne choisie
if colonnes:
    colonnes = colonnes.split(',')
else:
    colonnes = df.columns.tolist()
for col in colonnes:
    if operation == 'chiffrement':
        df[col] = df[col].apply(lambda x: aes_encrypt(x, cle_chiffrement, mode_chiffrement,iv=vecteur if mode_chiffrement == 'CBC' else None))
    elif operation == 'dechiffrement':
        df[col] = df[col].apply(lambda x: aes_decrypt(x, cle_chiffrement, mode_chiffrement,iv=vecteur if mode_chiffrement == 'CBC' else None))
    elif operation == 'hashage':
        df[col] = df[col].apply(lambda x: sha256_hash(str(x)))
    else:
        print("Opération non reconnue.")
        sys.exit(1)

# Enregistrer le fichier Excel hashé
fichier_sortie = config['fileinfo']['fichier_sortie']
df.to_excel(fichier_sortie, index=False)


end=time.time()
print("xlsx généré en " + str(end - start) + " secondes")
