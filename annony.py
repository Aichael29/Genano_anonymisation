import hashlib
import json
import pandas as pd
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
import sys


# Définir une fonction pour crypter les valeurs d'une colonne avec AES en mode CBC ou ECB
def aes_encrypt(value, key, mode_chiffrement, iv=None):
    if mode_chiffrement == 'CBC' and iv is None:
        raise ValueError("Le vecteur d'initialisation doit être spécifié pour le mode CBC.")
    if mode_chiffrement == 'CBC':
        cipher = AES.new(key.encode(), AES.MODE_CBC, iv.encode())
    else:
        cipher = AES.new(key.encode(), AES.MODE_ECB)
    if isinstance(value, str):
        padded_value = pad(value.encode(), AES.block_size)
    elif isinstance(value, int):
        padded_value = pad(str(value).encode(), AES.block_size)
    elif isinstance(value, float):
        padded_value = pad(str(value).encode(), AES.block_size)
    elif isinstance(value, bytes):
        padded_value = pad(value, AES.block_size)
    elif isinstance(value, bytearray):
        padded_value = pad(bytes(value), AES.block_size)
    elif isinstance(value, memoryview):
        padded_value = pad(bytes(value), AES.block_size)
    else:
        raise ValueError("Type de données non pris en charge.")
    encrypted_value = cipher.encrypt(padded_value)
    return encrypted_value.hex()

# Définir une fonction pour décrypter les valeurs d'une colonne avec AES en mode CBC ou ECB
# Define decryption function
def aes_decrypt(value, key, mode_chiffrement, iv=None):
    if mode_chiffrement == 'CBC' and iv is None:
        raise ValueError("Le vecteur d'initialisation doit être spécifié pour le mode CBC.")
    if mode_chiffrement == 'ECB' and iv is not None:
        raise ValueError("IV n'est pas utile pour le mode ECB.")
    if mode_chiffrement == 'CBC':
        cipher = AES.new(key.encode(), AES.MODE_CBC, iv.encode())
    else:
        cipher = AES.new(key.encode(), AES.MODE_ECB)
    decrypted_value = unpad(cipher.decrypt(bytes.fromhex(value)), AES.block_size)
    return decrypted_value.decode('utf-8')

# Définir une fonction pour hasher les valeurs d'une colonne avec SHA256
def sha256_hash(value):
    if isinstance(value, bytes):
        return hashlib.sha256(value).hexdigest()
    elif isinstance(value, bytearray):
        return hashlib.sha256(bytes(value)).hexdigest()
    elif isinstance(value, memoryview):
        return hashlib.sha256(bytes(value)).hexdigest()
    elif hasattr(value, 'read'):
        value_hash = hashlib.sha256()
        while True:
            chunk = value.read(4096)
            if not chunk:
                break
            value_hash.update(chunk)
        return value_hash.hexdigest()
    else:
        return hashlib.sha256(str(value).encode()).hexdigest()
def encrypt_file(file_extension, fichier_entree, fichier_sortie ,operation,cle_chiffrement, mode_chiffrement,vecteur, colonnes=None,separateur=None,section=None):

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
        df = pd.read_csv(fichier_entree,sep=separateur)
        print("azertyuio")
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
        section = df.to_csv(index=False, header=False, sep=separateur).split('\n')[:-1]
        # écrire le dataframe modifié dans un nouveau fichier excel
        df.to_csv(fichier_sortie, index=False,sep=separateur)

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