import pandas as pd
from anonymisation import anonymize
from deanonymisation import dehash_columns

# Demander à l'utilisateur les chemins d'entrée et de sortie
folderin = input("Entrez le chemin du dossier d'entrée: ")
folderout = input("Entrez le chemin du dossier de sortie: ")

# Lecture du fichier Excel original
input_file = input("Entrez le nom du fichier Excel original: ")
df_input = pd.read_excel(folderin+"/"+input_file, header=0)

# Demander à l'utilisateur les noms des colonnes à anonymiser
cols = input("Entrez les noms des colonnes séparés par des virgules à anonymiser: ")
cols = cols.split(",")

# Anonymiser les colonnes sélectionnées
df_anon = anonymize(df_input, cols)

# Écrire le fichier Excel anonymisé
output_file = input("Entrez le nom du fichier de sortie: ")
df_anon.to_excel(folderout+"/"+output_file, sheet_name='anonyme', index=False)

# Demander à l'utilisateur les noms des colonnes à désanonymiser
cols = input("Entrez les noms des colonnes séparés par des virgules à désanonymiser: ")
cols = cols.split(",")

# Lecture du fichier Excel anonymisé
input_file = output_file
df_input = pd.read_excel(folderout+"/"+input_file, header=0)

# Désanonymiser les colonnes sélectionnées
dehash_columns(df_input, cols)

# Écrire le fichier Excel désanonymisé
output_file = "deanonymise_" + output_file
df_input.to_excel(folderout+"/"+output_file, sheet_name='deanonymise', index=False)

print("Opération terminée avec succès !")
