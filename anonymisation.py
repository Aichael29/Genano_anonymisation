import os
import pandas as pd
import hashlib

# Générer une clé secrète aléatoire de 64 caractères en utilisant SHA-512
def generate_secret_key():
    secret_key = hashlib.sha512(os.urandom(64)).hexdigest()
    return secret_key

# Fonction pour nettoyer le hachage en renvoyant les 20 premiers caractères
def cleanhash(s):
    return hashlib.sha512(bytearray(str(s).strip()+generate_secret_key(), "utf8")).hexdigest()[:20]
# Fonction pour anonymiser une colonne dans un dataframe
def anonymize(df):
    for column in df.columns:
        # Ajouter une colonne hashée pour chaque colonne du dataframe
        df[column+'_hash'] = df[column].apply(cleanhash)
    return df

# Clé secrète pour le hachage
seckey = "y3HsVaFY9Uj<\C#!nMnK,%q=F?dR4WA|s(bwisfcU<q.P&L"

# Dossier d'entrée et de sortie pour les fichiers
folder = 'C:/Users/Lenovo/Pictures/'
folderin = folder
folderout = folder + "out/"
# Vérifier si le dossier de sortie existe et le créer s'il n'existe pas
if not os.path.exists(folderout):
    os.makedirs(folderout)
# Nom du fichier d'entrée
filename = 'input.csv'

# Chemin d'accès au fichier d'entrée
filepath = os.path.join(folderin, filename)

# Vérifier le type de fichier d'entrée
file_ext = os.path.splitext(filename)[1]
if file_ext == ".xlsx":
    # Charger le fichier Excel d'entrée dans un dataframe
    df_input = pd.read_excel(filepath)
elif file_ext == ".csv":
    # Charger le fichier CSV d'entrée dans un dataframe
    df_input = pd.read_csv(filepath)
else:
    print("Extension de fichier non prise en charge.")
    exit()

# Anonymiser les données
df_anonymized = anonymize(df_input.copy())

# Supprimer les colonnes d'origine
df_anonymized.drop(df_input.columns, axis=1, inplace=True)

# Nom du fichier de sortie pour les données anonymisées
output_filename = os.path.splitext(filename)[0] + '_anonymized.csv'

# Chemin d'accès pour le fichier de sortie
output_filepath = os.path.join(folderout, output_filename)

# Exporter les données anonymisées dans un fichier CSV
df_anonymized.to_csv(output_filepath, index=False)
