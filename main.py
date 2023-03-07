import os
import pandas as pd
import hashlib

# Générer une clé aléatoire de 64 caractères en utilisant SHA-512
def generate_secret_key():
    secret_key = hashlib.sha512(os.urandom(64)).hexdigest()
    return secret_key

# Fonction pour nettoyer le hachage en renvoyant les 20 premiers caractères
def cleanhash(s):
    return hashlib.sha512(str(s).encode()).hexdigest()[:20]

# Fonction pour anonymiser une colonne dans un dataframe
def anonymize(df, column):
    df[column+'_hash'] = df[column].apply(cleanhash)
    return df

# Fonction pour déanonymiser une colonne dans un dataframe
def deanonymize(df, column):
    # Réappliquer la même fonction de hachage pour inverser l'anonymisation
    df[column] = df[column+'_hash'].apply(lambda x: hashlib.sha512(str(x).encode()).hexdigest()[:20])
    return df.drop(columns=[column+'_hash'])

# Clé secrète pour le hachage
seckey = "y3HsVaFY9Uj<\C#!nMnK,%q=F?dR4WA|s(bwisfcU<q.P&L"

# Dossier d'entrée et de sortie pour les fichiers
folder = './'
folderin = folder
folderout = folder + "out/"

# Exemple d'utilisation
df = pd.DataFrame({'ID': [1, 2, 3], 'Name': ['Alice', 'Bob', 'Charlie']})
df_anonymized = anonymize(df.copy(), 'ID')
df_deanonymized = deanonymize(df_anonymized.copy(), 'ID')

# Nom du fichier d'entrée
filename = 'input.csv' # peut être n'importe quel type de fichier, par exemple .txt, .csv, .xlsx, etc.

# Chemin d'accès au fichier d'entrée
filepath = os.path.join(folderin, filename)

# Charger le fichier d'entrée dans un dataframe
df_input = pd.read_csv(filepath, header=0) # supposons que le fichier d'entrée a une ligne d'en-tête

# Anonymiser la colonne 'ID' du dataframe d'entrée
df_anonymized = anonymize(df_input, 'ID')

# Nom du fichier de sortie pour les données anonymisées
output_filename = os.path.splitext(filename)[0] + '_anonymized.xlsx'

# Chemin d'accès pour le fichier de sortie
output_filepath = os.path.join(folderout, output_filename)

# Exporter les données anonymisées dans un fichier Excel
df_anonymized.to_excel(output_filepath, sheet_name='hash', index=False)

# Inverser l'anonymisation pour retrouver les données originales
df_deanonymized = deanonymize(df_anonymized, 'ID')

# Nom du fichier de sortie pour les données déanonymisées
output_filename = os.path.splitext(filename)[0] + '_deanonymized.xlsx'

# Chemin d'accès pour le fichier de sortie
output_filepath = os.path.join(folderout, output_filename)

# Exporter les données déanonymisées dans un fichier Excel
df_deanonymized.to_excel(output_filepath, sheet_name='hash', index=False)
