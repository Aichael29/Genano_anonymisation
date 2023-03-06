import pandas as pd
from hash_ids import cleanhash

# La fonction hash_excel_file prend en entrée le nom du fichier Excel d'entrée (input_file),
# le nom du fichier Excel de sortie (output_file), le nom de la colonne contenant les IDs (id_column)
# et une clé pour le hachage (key). La fonction lit le fichier d'entrée avec pandas, vérifie
# que la colonne ID existe, ajoute les hachages à la colonne id_hash et écrit le résultat dans le fichier
# de sortie.
def hash_excel_file(input_file, output_file, id_column='ID', key='y3HsVaFY9Uj<\C#*!nMnK,*%q=F?dR4WA|s(bwisfcU<q.P\&L'):
    try:
        df_input = pd.read_excel(input_file, header=0)
    except FileNotFoundError:
        print(f"Error: input file '{input_file}' not found")
        exit()

    if id_column not in df_input.columns:
        print(f"Error: column '{id_column}' not found in input file")
        exit()

    try:
        # La fonction apply est utilisée pour appliquer la fonction cleanhash à chaque valeur de la colonne ID.
        df_input['id_hash'] = df_input[id_column].apply(lambda x: cleanhash(x, key))
    except:
        print("Error: an unexpected error occurred while hashing the IDs")
        exit()

    try:
        # La méthode to_excel est utilisée pour écrire le DataFrame pandas dans le fichier de sortie.
        df_input.to_excel(output_file, sheet_name='hash', index=False)
    except PermissionError:
        print(f"Error: could not write to output file '{output_file}'")
        exit()
