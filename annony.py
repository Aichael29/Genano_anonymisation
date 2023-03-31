import hashlib
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad


# Définir une fonction pour crypter les valeurs d'une colonne avec AES en mode CBC ou ECB
def aes_encrypt(value, key, mode_chiffrement=None, iv=None):
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
    elif isinstance(value,bytes):
        padded_value = pad(value, AES.block_size)
    elif isinstance(value,bytearray ):
        padded_value = pad(bytes(value), AES.block_size)
    elif isinstance(value, memoryview):
        padded_value = pad(bytes(value), AES.block_size)
    else:
        raise ValueError("Type de données non pris en charge.")
    encrypted_value = cipher.encrypt(padded_value)
    return encrypted_value.hex()
# Define decryption function
def aes_decrypt(value, key, mode_chiffrement=None, iv=None):
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
