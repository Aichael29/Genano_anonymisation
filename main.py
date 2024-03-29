import configparser
import json
import os
import random
import sys
import time
from annony import aes_encrypt, aes_decrypt, sha256_hash, anonymisation
import pandas as pd

start=time.time()
config = configparser.ConfigParser()
config.read('configuration.conf')

fichier_entree = config['fileinfo']['fichier_entree']
fichier_sortie = config['fileinfo']['fichier_sortie']
type = os.path.splitext(fichier_entree)[1].lower()
operation = config['Operations']['operation']
sep =config['Operations'].get('separateur', None)
if sep is None or len(sep)==0:
   sep = ","
colonnes = config['Operations'].get('colonnes', None)
if colonnes is None:
    colonnes = []


if operation in ["chiffrement", "dechiffrement"]:
    mode_chiffrement = config['Operations']['mode_chiffrement']
    if mode_chiffrement not in ('ECB', 'CBC'):
        print("Le mode de chiffrement doit être soit ECB ou CBC.")
        exit()
    cle_chiffrement = config['Operations']['cle_chiffrement']
    if len(cle_chiffrement) != 16:
        print("La clé doit être de 16 caractères.")
        exit()
    if mode_chiffrement == "CBC":
        vecteur = config['Operations']['vector']
        if mode_chiffrement == 'CBC' and len(vecteur) != 16:
            print("Le vecteur d'initialisation doit être de 16 octets.")
            exit()

def encrypt_file(file_extension, fichier_entree, fichier_sortie,colonnes=None):


    # vérifier l'extension et exécuter le traitement approprié
    if file_extension in ['.txt','.html','.docx']:
        # ouvrir le fichier et lire chaque ligne
        with open(fichier_entree, 'r') as file:
            lines = []
            for line in file:
                # appliquer l'opération sur chaque ligne
                if operation == 'chiffrement':
                    line = aes_encrypt(line.strip(), cle_chiffrement, mode_chiffrement, iv=vecteur if mode_chiffrement == 'CBC' else None)
                elif operation == 'dechiffrement':
                    line = aes_decrypt(line.strip(), cle_chiffrement, mode_chiffrement, iv=vecteur if mode_chiffrement == 'CBC' else None)
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

    elif file_extension == '.xml':
        # Charger le fichier XML en un DataFrame Pandas
        df = pd.read_xml(fichier_entree)
        # Appliquer la fonction de décryptage ou de hachage à chaque colonne spécifiée
        if colonnes:
            colonnes = colonnes.split(',')
        else:
            colonnes = df.columns.tolist()

        for col in colonnes:
            if operation == 'chiffrement':
                df[col] = df[col].apply(lambda x: aes_encrypt(str(x), cle_chiffrement, mode_chiffrement,iv=vecteur if mode_chiffrement == 'CBC' else None))
            elif operation == 'dechiffrement':
                df[col] = df[col].apply(lambda x: aes_decrypt(str(x), cle_chiffrement, mode_chiffrement,iv=vecteur if mode_chiffrement == 'CBC' else None))
            elif operation == 'hashage':
                df[col] = df[col].apply(lambda x: sha256_hash(str(x)))

        # écrire le DataFrame modifié dans un nouveau fichier XML
        df.to_xml(fichier_sortie, root_name='root', row_name='row', index=False)

    elif file_extension == '.csv':
        df = pd.read_csv(fichier_entree,sep=sep)

        # Appliquer la fonction de decryptage à chaque colonne spécifiée
        if colonnes:
            colonnes = colonnes.split(',')
        else:
            colonnes = df.columns.tolist()

        for col in colonnes:
                if operation == 'chiffrement':
                    df[col] = df[col].apply(lambda x: aes_encrypt(str(x), cle_chiffrement, mode_chiffrement, iv=vecteur if mode_chiffrement == 'CBC' else None))
                elif operation == 'dechiffrement':
                    df[col] = df[col].apply(lambda x: aes_decrypt(str(x), cle_chiffrement, mode_chiffrement, iv=vecteur if mode_chiffrement == 'CBC' else None))
                elif operation == 'hashage':
                    df[col] = df[col].apply(lambda x: sha256_hash(str(x)))
                elif operation == 'anonymisation':
                    df[col] = anonymisation(df[col])

        # écrire le dataframe modifié dans un nouveau fichier excel
        df.to_csv(fichier_sortie, index=False,sep=sep)

    elif file_extension == '.json':
        # Charger le fichier JSON en un dataframe pandas
        with open(fichier_entree) as f:
            data = json.load(f)
        df = pd.json_normalize(data)
        # Appliquer la fonction de decryptage à chaque colonne spécifiée
        if colonnes:
            colonnes = colonnes.split(',')
        else:
            colonnes = df.columns.tolist()

        for col in colonnes:
            if operation == 'chiffrement':
                df[col] = df[col].apply(lambda x: aes_encrypt(str(x), cle_chiffrement, mode_chiffrement,iv=vecteur if mode_chiffrement == 'CBC' else None))
            elif operation == 'dechiffrement':
                df[col] = df[col].apply(lambda x: aes_decrypt(str(x), cle_chiffrement, mode_chiffrement,iv=vecteur if mode_chiffrement == 'CBC' else None))
            elif operation == 'hashage':
                df[col] = df[col].apply(lambda x: sha256_hash(str(x)))
        # Écrire le dataframe modifié dans un nouveau fichier JSON
        df_json = json.loads(df.to_json(orient='records'))
        with open(fichier_sortie, 'w') as f:
            json.dump(df_json, f, indent=4)


    elif file_extension == '.xlsx':

        df = pd.read_excel(fichier_entree, engine='openpyxl')
        # Appliquer la fonction de decryptage à chaque colonne spécifiée
        if colonnes:
            colonnes = colonnes.split(',')
        else:
            colonnes = df.columns.tolist()
        for col in colonnes:
            if operation == 'chiffrement':
                df[col] = df[col].apply(lambda x: aes_encrypt(str(x), cle_chiffrement, mode_chiffrement,
                                                              iv=vecteur if mode_chiffrement == 'CBC' else None))
            elif operation == 'dechiffrement':
                df[col] = df[col].apply(lambda x: aes_decrypt(str(x), cle_chiffrement, mode_chiffrement,
                                                              iv=vecteur if mode_chiffrement == 'CBC' else None))
            elif operation == 'hashage':
                df[col] = df[col].apply(lambda x: sha256_hash(str(x)))
            elif operation == 'anonymisation':
                df[col] = anonymisation(df[col])
            # écrire le dataframe modifié dans un nouveau fichier excel
            df.to_excel(fichier_sortie, index=False)


    else:
                    print("Opération non reconnue.")
                    sys.exit(1)

encrypt_file(type,fichier_entree,fichier_sortie,colonnes)


end=time.time()

print("le fichier est généré en " + str(end - start) + " secondes")

