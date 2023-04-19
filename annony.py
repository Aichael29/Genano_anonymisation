import hashlib
import random

from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
import json

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
def aes_decrypt(value, key, mode_chiffrement, iv=None):
    if mode_chiffrement == 'CBC' and iv is None:
        raise ValueError("Le vecteur d'initialisation doit être spécifié pour le mode CBC.")
    if mode_chiffrement == 'ECB' and iv is not None:
        raise ValueError("IV n'est pas utile pour le mode ECB.")
    if mode_chiffrement == 'CBC':
        cipher = AES.new(key.encode(), AES.MODE_CBC, iv.encode('utf-8'))
    else:
        cipher = AES.new(key.encode(), AES.MODE_ECB)
    decrypted_value = cipher.decrypt(bytes.fromhex(value))
    return unpad(decrypted_value, AES.block_size).decode()

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

import random

def anonymisation(values):
    unique_values = values.unique().tolist()
    random.shuffle(unique_values)
    # vérifier que les nouvelles valeurs ne sont pas identiques aux anciennes valeurs
    while any(x == y for x, y in zip(values.unique(), unique_values)):
        random.shuffle(unique_values)
    dict_valeurs = {ancienne_valeur: nouvelle_valeur for ancienne_valeur, nouvelle_valeur in zip(values.unique(), unique_values)}
    return values.replace(dict_valeurs)


def deanonymisation(values):
    global dict_valeurs
    return values.replace(dict_valeurs)




