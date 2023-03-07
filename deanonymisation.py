import os
import pandas as pd
import hashlib

# Fonction pour générer une clé aléatoire de 64 caractères en utilisant SHA-512
def generate_secret_key():
    secret_key = hashlib.sha512(os.urandom(64)).hexdigest()
    return secret_key

# Fonction pour nettoyer le hachage en renvoyant les 20 premiers caractères
def cleanhash(s):
    return hashlib.sha512(str(s).encode()).hexdigest()[:20]

# Fonction pour déanonymiser une colonne dans un dataframe
def deanonymize(df):
    for column in df.columns:
        if '_hash' in column:
            # récupérer le nom de la colonne avant l'anonymisation
            column_name = column.replace('_hash', '')
            # réappliquer la même fonction de hachage pour inverser l'anonymisation
            df[column_name] = df[column].apply(lambda x: hashlib.sha512(str(x).encode()).hexdigest()[:20])
    # supprimer les colonnes anonymisées
    return df.drop(columns=[col for col in df.columns if '_hash' in col])

# Dossier d'entrée et de sortie pour les fichiers
folder = 'C:/Users/Lenovo/Pictures/out/'
folderin = folder
folderout = folder + "out/"

# Vérifier si le dossier de sortie existe et le créer s'il n'existe pas
if not os.path.exists(folderout):
    os.makedirs(folderout)

# Nom du fichier d'entrée
filename = 'input_anonymized.csv'

# Chemin d'accès au fichier d'entrée
filepath = os.path.join(folderin, filename)

# Charger le fichier d'entrée dans un dataframe
if filepath.endswith('.csv'):
    df_input = pd.read_csv(filepath, encoding='iso-8859-1')
elif filepath.endswith('.xlsx'):
    df_input = pd.read_excel(filepath)
else:
    raise ValueError("Type de fichier non supporté")

# Déanonymiser les données
df_deanonymized = deanonymize(df_input.copy())

# Nom du fichier de sortie pour les données déanonymisées
output_filename = os.path.splitext(filename)[0] + '_deanonymized.xlsx'

# Chemin d'accès pour le fichier de sortie
output_filepath = os.path.join(folderout, output_filename)

# Exporter les données déanonymisées dans un fichier xlsx
df_deanonymized.to_excel(output_filepath, index=False)
