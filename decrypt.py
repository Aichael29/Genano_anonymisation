import pandas as pd
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import unpad

# Charger le fichier Excel crypté dans un dataframe Pandas
encrypted_file_path = input("Veuillez entrer le chemin du fichier crypté : ")
df = pd.read_excel(encrypted_file_path)

# Choisir les colonnes que vous souhaitez décrypter
columns_to_decrypt = input("Veuillez entrer les noms des colonnes à décrypter, séparés par des virgules: ").split(',')

# Demander à l'utilisateur de saisir la clé pour le décryptage
key = input("Veuillez entrer la clé de décryptage : ")

# Définir une fonction pour décrypter les valeurs de la colonne
def aes_decrypt(value, key):
    cipher = AES.new(key.encode(), AES.MODE_ECB)
    decrypted_value = cipher.decrypt(bytes.fromhex(value))
    unpadded_value = unpad(decrypted_value, AES.block_size)
    return unpadded_value.decode()

# Appliquer la fonction de décryptage aux colonnes choisies
for col in columns_to_decrypt:
    df[col] = df[col].apply(lambda x: aes_decrypt(x, key))

# Enregistrer le fichier Excel décrypté
decrypted_file_path = input("Veuillez entrer le chemin de sortie pour le fichier décrypté : ")
df.to_excel(decrypted_file_path, index=False)
