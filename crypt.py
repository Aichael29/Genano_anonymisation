import pandas as pd
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad
import os

# Étape 1 : Charger le fichier Excel en utilisant pandas
df = pd.read_excel('input.xlsx')

# Étape 2 : Chiffrer la colonne souhaitée en utilisant AES
iv = os.urandom(16) # vecteur d'initialisation aléatoire
key = b'maclefsecrete16b' # clé de chiffrement partagée
cipher = AES.new(key, AES.MODE_CBC, iv=iv) # initialisation de l'objet AES

colonne_chiffree = cipher.encrypt(pad(df['ID'].to_string(index=False).encode(), AES.block_size)) # chiffrement de la colonne sensible

# Étape 4 : Ajouter la colonne chiffrée au DataFrame
df['colonne_chiffree'] = [colonne_chiffree]

# Étape 5 : Supprimer la colonne sensible du DataFrame
df = df.drop(columns=['ID'])

# Étape 6 : Enregistrer le DataFrame chiffré dans un nouveau fichier Excel
writer = pd.ExcelWriter('fichier_excel_chiffre.xlsx')
df.to_excel(writer, index=False)
writer.save()
