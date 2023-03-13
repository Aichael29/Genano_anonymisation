import pandas as pd
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad

# Charger le fichier Excel dans un dataframe Pandas
input_file = input("Entrez le nom du fichier d'entrée (par ex. 'input.xlsx') : ")
df = pd.read_excel(input_file)

# Demander à l'utilisateur les colonnes à crypter
columns_to_encrypt = input("Entrez le nom de la ou des colonnes à crypter, séparées par des virgules : ").split(',')

# Demander à l'utilisateur la clé de chiffrement
key = input("Entrez la clé de chiffrement de 16 caractères : ")

# Définir une fonction pour crypter les valeurs d'une colonne
def aes_encrypt(value, key):
    cipher = AES.new(key.encode(), AES.MODE_ECB)
    if isinstance(value, int):  # vérifier si la valeur est un entier
        value = str(value)  # convertir l'entier en chaîne de caractères
    padded_value = pad(value.encode(), AES.block_size)
    encrypted_value = cipher.encrypt(padded_value)
    return encrypted_value.hex()

# Appliquer la fonction de chiffrement à chaque colonne choisie
for col in columns_to_encrypt:
    df[col] = df[col].apply(lambda x: aes_encrypt(x, key))

# Enregistrer le fichier Excel crypté
output_file = input("Entrez le nom du fichier de sortie (par ex. 'output.xlsx') : ")
df.to_excel(output_file, index=False)

print("Cryptage terminé !")
