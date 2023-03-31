import hashlib
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad

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
    return encrypted_value

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
    decrypted_value = unpad(cipher.decrypt(value), AES.block_size)
    return decrypted_value

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
