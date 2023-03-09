import pandas as pd
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad

# Charger le fichier Excel dans un dataframe Pandas
df = pd.read_excel('input.xlsx')

# Choisir la colonne que vous souhaitez crypter
column_to_encrypt = 'phone number'

# Définir une fonction pour crypter les valeurs de la colonne
def aes_encrypt(value, key):
    cipher = AES.new(key.encode(), AES.MODE_ECB)
    if isinstance(value, int):  # vérifier si la valeur est un entier
        value = str(value)  # convertir l'entier en chaîne de caractères
    padded_value = pad(value.encode(), AES.block_size)
    encrypted_value = cipher.encrypt(padded_value)
    return encrypted_value.hex()

# Définir une clé pour le chiffrement
key = 'my_secret_key123'

# Appliquer la fonction de chiffrement à la colonne choisie
df[column_to_encrypt] = df[column_to_encrypt].apply(lambda x: aes_encrypt(x, key))

# Enregistrer le fichier Excel crypté
df.to_excel('output_file.xlsx', index=False)
