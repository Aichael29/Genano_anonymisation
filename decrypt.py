import pandas as pd
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import unpad

# Charger le fichier Excel crypté dans un dataframe Pandas
df = pd.read_excel('output_file.xlsx')

# Choisir la colonne que vous souhaitez décrypter
column_to_decrypt = 'phone number'

# Définir une fonction pour décrypter les valeurs de la colonne
def aes_decrypt(value, key):
    cipher = AES.new(key.encode(), AES.MODE_ECB)
    decrypted_value = cipher.decrypt(bytes.fromhex(value))
    unpadded_value = unpad(decrypted_value, AES.block_size)
    return unpadded_value.decode()

# Définir la clé pour le décryptage
key = 'my_secret_key123'

# Appliquer la fonction de décryptage à la colonne choisie
df[column_to_decrypt] = df[column_to_decrypt].apply(lambda x: aes_decrypt(x, key))

# Enregistrer le fichier Excel décrypté
df.to_excel('decrypted_file.xlsx', index=False)
