import configparser
import csv
import json
import os
import sys
import time
from annony import aes_encrypt, aes_decrypt, sha256_hash
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
file_extension = os.path.splitext(fichier_entree)[1].lower()
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
def encrypt_file(file_extension, fichier_entree, fichier_sortie ,cle_chiffrement, mode_chiffrement, iv=None, colonnes=None):

        # vérifier l'extension et exécuter le traitement approprié
     if file_extension in ['.csv', '.txt']:
         # ouvrir le fichier et lire chaque ligne
            with open(fichier_entree, 'r') as file:
                lines = []
                for line in file:
                    # appliquer l'opération sur chaque ligne
                    if operation == 'chiffrement':
                        line = aes_encrypt(line.strip(), cle_chiffrement, mode_chiffrement=None, iv=None)
                    elif operation == 'dechiffrement':
                        line = aes_decrypt(line.strip(), cle_chiffrement, mode_chiffrement=None, iv=None)
                    elif operation == 'hashage':
                        line = sha256_hash(line.strip())
                    else:
                        print("Opération non reconnue.")
                        sys.exit(1)
                    lines.append(line)

            # écrire les lignes modifiées dans un nouveau fichier
            with open(fichier_sortie, 'w') as encrypted_file:
                for line in lines:
                    encrypted_file.write(line + '\n')

     elif file_extension == '.json':
            # ouvrir le fichier json et charger le contenu en un dictionnaire
            with open(fichier_entree, 'r') as json_file:
                json_dict = json.load(json_file)

            # appliquer l'opération sur chaque valeur de chaque clé spécifiée
            for key in json_dict:
                if colonnes is None or key in colonnes:
                    if operation == 'chiffrement':
                        json_dict[key] = aes_encrypt(json_dict[key], cle_chiffrement, mode_chiffrement, iv)
                    elif operation == 'dechiffrement':
                        json_dict[key] = aes_decrypt(json_dict[key], cle_chiffrement, mode_chiffrement, iv)
                    elif operation == 'hashage':
                        json_dict[key] = sha256_hash(json_dict[key])
                    else:
                        print("Opération non reconnue.")
                        sys.exit(1)

            # écrire le dictionnaire modifié dans un nouveau fichier json
            with open(fichier_sortie, 'w') as f:
                json.dump(json_dict, f)

     elif file_extension == '.xlsx':
            df = pd.read_excel(fichier_entree, engine='openpyxl')

            # Appliquer la fonction de decryptage à chaque colonne spécifiée
            if colonnes:
                for col in colonnes:
                    if operation == 'chiffrement':
                        df[col] = df[col].apply(lambda x: aes_encrypt(str(x), cle_chiffrement, mode_chiffrement, iv))
                    elif operation == 'dechiffrement':
                        df[col] = df[col].apply(lambda x: aes_decrypt(str(x), cle_chiffrement, mode_chiffrement, iv))
                    elif operation == 'hashage':
                        df[col] = df[col].apply(lambda x: sha256_hash(str(x)))

            # écrire le dataframe modifié dans un nouveau fichier excel
            df.to_excel(fichier_sortie, index=False)

     elif file_extension in ['.jpg', '.jpeg', '.png', '.bmp']:
         # open the image file and read the binary data
         with open(fichier_entree, 'rb') as file:
             binary_data = file.read()

         # apply the operation on the binary data
         if operation == 'chiffrement':
             encrypted_data = aes_encrypt(binary_data, cle_chiffrement, mode_chiffrement, iv)
         elif operation == 'dechiffrement':
             encrypted_data = aes_decrypt(binary_data, cle_chiffrement, mode_chiffrement, iv)
         elif operation == 'hashage':
             encrypted_data = sha256_hash(binary_data)
         else:
             print("Opération non reconnue.")
             sys.exit(1)
         with open(fichier_sortie, 'wb') as encrypted_file:
             if operation == "chiffrement":
                 encrypted_file.write(encrypted_data.encode('utf-8'))
             elif operation == "dechiffrement":
                 encrypted_file.write(encrypted_data.decode())
             elif operation == "hashage":
                 encrypted_file.write(encrypted_data.encode('utf-8'))
             else:
                 print("Opération non reconnue.")
                 sys.exit(1)

     else:
            print("Type de fichier non reconnu.")
            sys.exit(1)


encrypt_file(file_extension,fichier_entree,fichier_sortie,cle_chiffrement,mode_chiffrement,vecteur,colonnes=None)


end=time.time()
print("xlsx généré en " + str(end - start) + " secondes")