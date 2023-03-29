import pandas as pd
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad
from Cryptodome.Random import get_random_bytes
import configparser

# Lecture du fichier de configuration
config = configparser.ConfigParser()
config.read('configuration.conf')

# Opération de chiffrement ou de déchiffrement
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
df = pd.read_excel(fichier_entree)

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



# Appliquer la fonction de cryptage à chaque colonne choisie
if colonnes:
    colonnes = colonnes.split(',')
else:
    colonnes = df.columns.tolist()
for col in colonnes:
    df[col] = df[col].apply(lambda x: aes_encrypt(x, cle_chiffrement, mode_chiffrement, iv=vecteur if mode_chiffrement == 'CBC' else None))

# Enregistrer le fichier Excel crypté
fichier_sortie = config['fileinfo']['fichier_sortie']
df.to_excel(fichier_sortie, index=False)
