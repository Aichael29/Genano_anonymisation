import configparser
import json
import os
import time
from annony import *
import pandas as pd
start=time.time()
# Lecture du fichier de configuration
config = configparser.ConfigParser()
config.read('configuration.conf')
# Opération à effectuer
operation = config['Operations']['operation']

#type=config['Operations']['filetype']

# Mode de chiffrement (ECB ou CBC)
mode_chiffrement = config['Operations']['mode_chiffrement']
# Colonnes à crypter
colonnes = config['Operations'].get('colonnes', None)
if colonnes is None:
    colonnes = []
print(colonnes)
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


def encrypt_file(file_extension, fichier_entree, fichier_sortie,operation,cle_chiffrement, mode_chiffrement, iv=None, colonnes=None):
    if file_extension == '.json':
        # ouvrir le fichier et lire chaque ligne
        print(file_extension)
        with open(fichier_entree, 'r') as file:
            data = json.load(file)

        keys = get_keys(data)
        # appliquer l'opération sur chaque ligne
        if operation == 'chiffrement':
            for key in keys:
                if colonnes and key not in colonnes:
                    continue
                if mode_chiffrement == 'ECB':
                    data[key] = aes_encrypt(data[key], cle_chiffrement, mode_chiffrement)
                else:
                    data[key] = aes_encrypt(data[key], cle_chiffrement, mode_chiffrement, iv)
        elif operation == 'dechiffrement':
            for key in keys:
                if colonnes and key not in colonnes:
                    continue
                if mode_chiffrement == 'ECB':
                    data[key] = aes_decrypt(data[key], cle_chiffrement, mode_chiffrement)
                else:
                    data[key] = aes_decrypt(data[key], cle_chiffrement, mode_chiffrement, iv)
        elif operation == 'hashage':
            for key in keys:
                if colonnes and key not in colonnes:
                    continue
                data[key] = sha256_hash(data[key])
        else:
            print("Opération non reconnue.")
            sys.exit(1)

        # écrire les données modifiées dans un nouveau fichier
        with open(fichier_sortie, 'w') as encrypted_file:
            json.dump(data, encrypted_file, indent=4)


        # ouvrir le fichier et lire chaque ligne
    elif file_extension in ['.csv','.txt','.xml','.html']:
             with open(fichier_entree, 'r') as file:
                lines = []
                for line in file:
                    # appliquer l'opération sur chaque ligne
                    if operation == 'chiffrement':
                        line = aes_encrypt(line.strip(), cle_chiffrement, mode_chiffrement, iv=None)
                    elif operation == 'dechiffrement':
                        line = aes_decrypt(line.strip(), cle_chiffrement, mode_chiffrement, iv=None)
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

    elif file_extension == '.docx':
        with open(fichier_entree, 'rb') as f:
            document = f.read()
        if operation == 'chiffrement':
            document_encrypted = aes_encrypt(document, cle_chiffrement,mode_chiffrement, iv=None)
            with open(fichier_sortie, 'wb') as f:
                f.write(document_encrypted)
        elif operation == 'dechiffrement':
            document_decrypted = aes_decrypt(document, cle_chiffrement,mode_chiffrement, iv=None)
            with open(fichier_sortie, 'wb') as f:
                f.write(document_decrypted)
        elif operation == 'hashage':
            document_hash = sha256_hash(document)
            with open(fichier_sortie, 'wb') as f:
                f.write(document_hash.encode())
    elif file_extension in ['.jpg', '.jpeg', '.png', '.gif']:
        # Ouvrir le fichier image
        with open(fichier_entree, 'rb') as f:
            image = f.read()

        # Appliquer l'opération sur l'image
            if operation == 'chiffrement':
                # Chiffrer l'image avec AES
                image_encrypted = aes_encrypt(image, cle_chiffrement, mode_chiffrement, iv=None)
                with open(fichier_sortie, 'wb') as f:
                    f.write(image_encrypted)
            elif operation == 'dechiffrement':
                # Déchiffrer l'image avec AES
                image_decrypted = aes_decrypt(image, cle_chiffrement, mode_chiffrement, iv=None)
                with open(fichier_sortie, 'wb') as f:
                    f.write(image_decrypted)
            elif operation == 'hashage':
                # Calculer le hash SHA-256 de l'image
                image_hash = sha256_hash(image)
                with open(fichier_sortie, 'wb') as f:
                    f.write(image_hash.encode())
            else:
                print("Opération non reconnue.")
                sys.exit(1)
    else:
        print("Type de fichier non reconnu.")
        sys.exit(1)



encrypt_file(type,fichier_entree,fichier_sortie,operation,cle_chiffrement,mode_chiffrement,vecteur,colonnes)

end=time.time()