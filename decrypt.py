import pandas as pd
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import unpad
import configparser

# Lecture du fichier de configuration
config = configparser.ConfigParser()
config.read('configuration.conf')

# Opération de chiffrement ou de déchiffrement
operation = config['Operations']['operation']

# Mode de chiffrement (ECB ou CBC)
mode_chiffrement = config['Operations']['mode_chiffrement']

# Clé de chiffrement
cle_chiffrement = config['Operations']['cle_chiffrement']

# Vecteur d'initialisation
vecteur = config['Operations']['vector']

# Colonnes à decrypter
colonnes = config['Operations'].get('colonnes', None)
if colonnes is None:
    colonnes = []

# Charger le fichier Excel crypté dans un dataframe Pandas
fichier_entree = config['fileinfo']['fichier_entree']
df = pd.read_excel(fichier_entree)

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
    encrypted_value = bytes.fromhex(value)
    decrypted_value = unpad(cipher.decrypt(encrypted_value), AES.block_size)
    if isinstance(decrypted_value, bytes):
        return decrypted_value.decode()
    else:
        return decrypted_value


# Appliquer la fonction de decryptage à chaque colonne choisie
if colonnes:
    colonnes = colonnes.split(',')
else:
    colonnes = df.columns.tolist()
for col in colonnes:
    df[col] = df[col].apply(lambda x: aes_decrypt(x, cle_chiffrement, mode_chiffrement, iv=vecteur if mode_chiffrement == 'CBC' else None))

#Enregistrer le fichier Excel déchiffré
fichier_sortie = config['fileinfo']['fichier_sortie']
df.to_excel(fichier_sortie, index=False)