
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad
import hashlib
from Cryptodome.Util.Padding import unpad

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
    else:
        raise ValueError("Type de données non pris en charge.")
    encrypted_value = cipher.encrypt(padded_value)
    return encrypted_value.hex()


def aes_decrypt(value, key, mode_chiffrement, iv=None):
    if mode_chiffrement == 'CBC' and iv is None:
        raise ValueError("Le vecteur d'initialisation doit être spécifié pour le mode CBC.")
    if mode_chiffrement == 'ECB' and iv is not None:
        raise ValueError("IV n'est pas utile pour le mode ECB.")
    if mode_chiffrement == 'CBC':
        cipher = AES.new(key.encode(), AES.MODE_CBC, iv.encode())
    else:
        cipher = AES.new(key.encode(), AES.MODE_ECB)
    encrypted_value = bytes.fromhex(value)
    decrypted_value = unpad(cipher.decrypt(encrypted_value), AES.block_size)
    if isinstance(decrypted_value, bytes):
        return decrypted_value.decode()
    else:
        return decrypted_value


# Définir une fonction pour hasher les valeurs d'une colonne avec SHA256
def sha256_hash(value):
    return hashlib.sha256(value.encode()).hexdigest()
from Crypto.Cipher import AES
import os
import binascii
import hashlib

# Clé de chiffrement (doit être de 16, 24 ou 32 octets)

def encrypt_txt_ECB(input_file,output_file,key):
    # Créer un objet de chiffrement AES avec la clé
    encryptor = AES.new(key, AES.MODE_ECB)

    with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        # Chiffrer le contenu du fichier d'entrée par blocs de 16 octets
        while True:
            block = f_in.read(16)
            if len(block) == 0:
                break
            elif len(block) % 16 != 0:
                block += b' ' * (16 - len(block) % 16)
            encrypted_block = encryptor.encrypt(block)

            f_out.write(binascii.hexlify(encrypted_block))

def decrypt_txt_ECB(input_file,output_file,key):
    # Créer un objet de déchiffrement AES avec la clé
    decryptor = AES.new(key, AES.MODE_ECB)

    with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        # Déchiffrer le contenu du fichier d'entrée par blocs de 16 octets
        while True:
            block = f_in.read(32)
            if len(block) == 0:
                break
            decrypted_block = decryptor.decrypt(binascii.unhexlify(block))
            f_out.write(decrypted_block.rstrip(b' '))
def hachage(fichier_entree,fichier_sortie):
 # Ouverture du fichier à hacher
        with open(fichier_entree, "rb") as f:
            # Lecture du contenu du fichier
            contenu = f.read()
        # Calcul du hachage SHA-256
            hachage = hashlib.sha256(contenu).hexdigest()
        # Ouverture du fichier en mode écriture
        with open(fichier_sortie, "w") as f:
            # Écriture du texte dans le fichier
            f.write(hachage)

def encrypt_txt_CBC(input_file,output_file,key,iv):
    # Créer un objet de chiffrement AES avec la clé et le vecteur d'initialisation
    encryptor = AES.new(key, AES.MODE_CBC, iv)

    with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        # Chiffrer le contenu du fichier d'entrée par blocs de 16 octets
        while True:
            block = f_in.read(16)
            if len(block) == 0:
                break
            elif len(block) % 16 != 0:
                block += b' ' * (16 - len(block) % 16)
            encrypted_block = encryptor.encrypt(block)

            f_out.write(binascii.hexlify(encrypted_block))

def decrypt_txt_CBC(input_file,output_file,key,iv):
    # Créer un objet de déchiffrement AES avec la clé et le vecteur d'initialisation
    decryptor = AES.new(key, AES.MODE_CBC, iv)

    with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        # Déchiffrer le contenu du fichier d'entrée par blocs de 16 octets
        while True:
            block = f_in.read(32) # On lit deux blocs chiffrés à la fois, car un bloc chiffré est représenté par deux caractères hexadécimaux
            if len(block) == 0:
                break
            decrypted_block = decryptor.decrypt(binascii.unhexlify(block))
            f_out.write(decrypted_block.rstrip(b' '))




