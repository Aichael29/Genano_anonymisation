import pandas as pd
from anonymisation import anonymize

# Demander à l'utilisateur les chemins d'entrée et de sortie
folderin = input("Entrez le chemin du dossier d'entrée: ")
folderout = input("Entrez le chemin du dossier de sortie: ")

# Lecture du fichier Excel d'entrée
input_file = input("Entrez le nom du fichier d'entrée: ")
df_input = pd.read_excel(folderin + "/" + input_file, header=0)

# Demander à l'utilisateur les colonnes à anonymiser
cols = input(
    "Entrez les noms de colonnes séparés par des virgules (laissez vide pour anonymiser toutes les colonnes): ")
if cols == "":
    cols = df_input.columns
else:
    cols = cols.split(",")

# Anonymisation des colonnes sélectionnées
df_output = anonymize(df_input, cols)

# Écrire le fichier Excel de sortie avec les valeurs anonymisées
output_file = input("Entrez le nom du fichier de sortie: ")
df_output.to_excel(folderout + "/" + output_file, sheet_name='hash', index=False)
