"""import os
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
def anonymize(df):
    for column in df.columns:
        df[column + '_hash'] = df[column].apply(cleanhash)
    return df


# Fonction pour déanonymiser une colonne dans un dataframe
def deanonymize(df):
    for column in df.columns:
        if '_hash' in column:
            column_name = column.replace('_hash', '')
            # Réappliquer la même fonction de hachage pour inverser l'anonymisation
            df[column_name] = df[column].apply(lambda x: hashlib.sha512(str(x).encode()).hexdigest()[:20])
    return df.drop(columns=[col for col in df.columns if '_hash' in col])


# Clé secrète pour le hachage
seckey = "y3HsVaFY9Uj<\C#!nMnK,%q=F?dR4WA|s(bwisfcU<q.P&L"

# Dossier d'entrée et de sortie pour les fichiers
folder = 'C:/Users/Lenovo/Pictures/'
folderin = folder
folderout = folder + "out/"


# Fonction pour traiter le fichier d'entrée
def process_file(filepath):
    # Charger le fichier d'entrée dans un dataframe
    df_input = pd.read_csv(filepath, encoding='iso-8859-1')

    # Anonymiser les données
    df_anonymized = anonymize(df_input.copy())

    # Nom du fichier de sortie pour les données anonymisées
    output_filename = os.path.splitext(os.path.basename(filepath))[0] + '_anonymized.csv'

    # Chemin d'accès pour le fichier de sortie
    output_filepath = os.path.join(folderout, output_filename)

    # Exporter les données anonymisées dans un fichier CSV
    df_anonymized.to_csv(output_filepath, index=False)

    # Déanonymiser les données
    df_deanonymized = deanonymize(df_anonymized.copy())

    # Nom du fichier de sortie pour les données déanonymisées
    output_filename = os.path.splitext(os.path.basename(filepath))[0] + '_deanonymized.csv'

    # Chemin d'accès pour le fichier de sortie
    output_filepath = os.path.join(folderout, output_filename)

    # Exporter les données déanonymisées dans un fichier CSV
    df_deanonymized.to_csv(output_filepath, index=False)


# Traitement de tous les fichiers dans le dossier d'entrée
for filename in os.listdir(folderin):
    # Chemin d'accès au fichier d'entrée
    filepath = os.path.join(folderin, filename)
    if os.path.isfile(filepath):
        # Processus de traitement du fichier
        process_file(filepath)
"""