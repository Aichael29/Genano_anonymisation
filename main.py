import configparser
import json
import os
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

# Charger le fichier Excel dans un dataframe Pandas
fichier_sortie = config['fileinfo']['fichier_sortie']

delimiter = config['Operations'].get('separateur', None)
if delimiter is None or len(delimiter) == 0:
    delimiter = ','

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


def encrypt_file(file_extension, fichier_entree, fichier_sortie ,cle_chiffrement, mode_chiffrement, iv=None, colonnes=None,delimiter=None):

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
        df = pd.read_csv(fichier_entree,sep=delimiter)
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
        # écrire le dataframe modifié dans un nouveau fichier excel
        df.to_csv(fichier_sortie, index=False,sep=delimiter)

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
                    df[col] = df[col].apply(lambda x: aes_encrypt(str(x), cle_chiffrement, mode_chiffrement, iv=vecteur if mode_chiffrement == 'CBC' else None))
                elif operation == 'dechiffrement':
                    df[col] = df[col].apply(lambda x: aes_decrypt(str(x), cle_chiffrement, mode_chiffrement, iv=vecteur if mode_chiffrement == 'CBC' else None))
                elif operation == 'hashage':
                    df[col] = df[col].apply(lambda x: sha256_hash(str(x)))
        # écrire le dataframe modifié dans un nouveau fichier excel
        df.to_excel(fichier_sortie, index=False)

    else:
                    print("Opération non reconnue.")
                    sys.exit(1)


encrypt_file(type,fichier_entree,fichier_sortie,cle_chiffrement,mode_chiffrement,vecteur,colonnes,delimiter)


end=time.time()
print("généré en " + str(end - start) + " secondes")
