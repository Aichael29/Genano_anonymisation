import pandas as pd
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad
import configparser

# Charger le fichier de configuration
config = configparser.ConfigParser()
config.read('configuration.conf')

# Récupérer les paramètres de configuration
key = config['operation']['cle_chiffrement']
vector = config['operation']['vector']
columns_to_encrypt = config['operation']['colonnes'].split(',')
input_file = config['fileinfo']['fichier_entree']
output_file = config['fileinfo']['fichier_sortie']

# Définir une fonction pour crypter les valeurs d'une colonne
def aes_encrypt(value, key, vector):
    cipher = AES.new(key.encode(), AES.MODE_CBC, iv=vector.encode())
    if isinstance(value, int):  # vérifier si la valeur est un entier
        value = str(value)  # convertir l'entier en chaîne de caractères
    padded_value = pad(value.encode(), AES.block_size)
    encrypted_value = cipher.encrypt(padded_value)
    return encrypted_value.hex()

# Charger le fichier Excel dans un dataframe Pandas
df = pd.read_excel(input_file)

# Appliquer la fonction de chiffrement à chaque colonne choisie
for col in columns_to_encrypt:
    df[col] = df[col].apply(lambda x: aes_encrypt(x, key, vector))

# Enregistrer le fichier Excel crypté
df.to_excel(output_file, index=False)