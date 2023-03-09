import pandas as pd
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import unpad
import binascii

# Étape 8 : Déchiffrer la colonne souhaitée en utilisant la même clé de chiffrement partagée et le même vecteur d'initialisation
df = pd.read_excel('fichier_excel_chiffre.xlsx')
key = b'maclefsecrete16b' # clé de chiffrement partagée
iv = df['colonne_chiffree'][0][:16] # extraire le vecteur d'initialisation du fichier Excel
cipher = AES.new(key, AES.MODE_CBC, iv=iv) # initialisation de l'objet AES
encrypted_data = df['colonne_chiffree'][0]
colonne_dechiffree = unpad(cipher.decrypt(encrypted_data), AES.block_size).decode() # déchiffrement de la colonne chiffrée

# Étape 9 : Déchiffrer l'ensemble du fichier Excel
iv = encrypted_data[:16] # extraire le vecteur d'initialisation du fichier Excel
cipher = AES.new(key, AES.MODE_CBC, iv=iv) # initialisation de l'objet AES
decrypted_data = cipher.decrypt(encrypted_data)
df['colonne_sensible'] = unpad(decrypted_data, AES.block_size).decode() # déchiffrement de la colonne chiffrée
df = df.drop(columns=['colonne_chiffree']) # supprimer la colonne chiffrée du DataFrame
writer = pd.ExcelWriter('fichier_excel_dechiffre.xlsx') # enregistrer le DataFrame déchiffré dans un nouveau fichier Excel
df.to_excel(writer, index=False)
writer.save()
