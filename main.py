import configparser
from anonymisation import *
import pandas as pd
import time
import hashlib
start = time.time()

# Lecture du fichier de configuration
config = configparser.ConfigParser()
config.read('configuration.conf')

# Opération de chiffrement ou de déchiffrement
operation = config['Operations']['operation']

# Mode de chiffrement (ECB ou CBC)
mode_chiffrement = config['Operations']['mode_chiffrement']

# Vecteur d'initialisation
vecteur = config['Operations']['vector']

# fichier d'entree
fichier_entree = config['fileinfo']['fichier_entree']
#fichier de sortie
fichier_sortie = config['fileinfo']['fichier_sortie']

# Clé de chiffrement
cle_chiffrement = config['Operations']['cle_chiffrement']
cle_chiffrement = cle_chiffrement.encode('utf-8')
vecteur = vecteur.encode('utf-8')
# Vérifier si la clé a la bonne taille
if len(cle_chiffrement) != 16:
    print("La clé doit être de 16 caractères.")
    exit()

# Vérifier si le mode de chiffrement est valide
if mode_chiffrement not in ('ECB', 'CBC'):
    print("Le mode de chiffrement doit être soit ECB ou CBC.")
    exit()

# Check if IV is required for mode
if mode_chiffrement == 'CBC' and len(vecteur) != 16:
    raise ValueError("Le vecteur d'initialisation doit être de 16 octets.")
#le type de fichier d'entree
#type_fichier = config['Operations']['type_fichier']
type_fichier = os.path.splitext(fichier_entree)[1].lower()
if type_fichier == '.csv':
    # Charger le fichier Excel dans un dataframe Pandas
    df = pd.read_excel(fichier_entree)

    # Colonnes à crypter
    colonnes = config['Operations'].get('colonnes', None)
    if colonnes is None:
        colonnes = []


    if colonnes:
            colonnes = colonnes.split(',')
    else:
            colonnes = df.columns.tolist()

    if operation == 'chiffrement':
        for col in colonnes:
            df[col] = df[col].apply(lambda x: aes_encrypt(x, cle_chiffrement, mode_chiffrement, iv=vecteur if mode_chiffrement == 'CBC' else None))
    elif operation == 'dechiffrement':
        for col in colonnes:
            df[col] = df[col].apply(lambda x: aes_decrypt(x, cle_chiffrement, mode_chiffrement, iv=vecteur if mode_chiffrement == 'CBC' else None))
    elif operation == 'hashage':
       # Appliquer la fonction de hashage à chaque colonne choisie
       for col in colonnes:
           df[col] = df[col].apply(lambda x: sha256_hash(str(x)))
    else:
        print("Opération non reconnue.")

    #Enregistrer le fichier Excel déchiffré
    fichier_sortie = config['fileinfo']['fichier_sortie']
    df.to_excel(fichier_sortie, index=False)

if type_fichier == '.txt':

    if operation == 'hash':
        hachage(fichier_entree,fichier_sortie)

    elif mode_chiffrement == "ECB":
        if operation == 'chiffrement':
            encrypt_txt_ECB(fichier_entree,fichier_sortie,cle_chiffrement)
        elif operation == 'dechiffrement':
            decrypt_txt_ECB(fichier_entree,fichier_sortie,cle_chiffrement)

    elif mode_chiffrement == "CBC":
        if operation == 'chiffrement':
            encrypt_txt_CBC(fichier_entree,fichier_sortie,cle_chiffrement,vecteur)
        elif operation == 'dechiffrement':
            decrypt_txt_CBC(fichier_entree,fichier_sortie,cle_chiffrement,vecteur)

    else:
        print("Opération non reconnue.")
else:
    print('type non trouvé')

end = time.time()
print("csv généré en " + str(end - start) + " secondes")
print("csv généré en " + str((end - start)/60) + " minutes")

