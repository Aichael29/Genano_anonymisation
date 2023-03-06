import pandas as pd
import hashlib
import os

seckey = "y3HsVaFY9Uj<\C#*!nMnK,*%q=F?dR4WA|s(bwisfcU<q.P\&L"
folder = './'
folderin = folder
folderout = folder + "out/"

# Fonction pour nettoyer et hacher une chaîne de caractères
def cleanhash(s):
    return hashlib.sha512(bytearray(str(s).strip()+seckey, "utf8")).hexdigest()[:20]

# Fonction pour anonymiser une colonne dans un dataframe
def anonymize(df, column):
    df[column+'_hash'] = df[column].apply(cleanhash)
    return df

# Fonction pour déanonymiser une colonne dans un dataframe
def deanonymize(df, column):
    # Réappliquer la même fonction de hachage pour inverser l'anonymisation
    df[column] = df[column+'_hash'].apply(lambda x: hashlib.sha512(bytearray(str(x).strip()+seckey, "utf8")).hexdigest()[:20])
    return df.drop(columns=[column+'_hash'])

# Exemple d'utilisation :
filename = 'input.csv'  # peut être n'importe quel type de fichier, par exemple .txt, .csv, .xlsx, etc.
filepath = os.path.join(folderin, filename)
df_input = pd.read_csv(filepath, header=0)  # supposons que le fichier d'entrée a une ligne d'en-tête
df_anonymized = anonymize(df_input, 'ID')
output_filename = os.path.splitext(filename)[0] + '_anonymized.xlsx'
output_filepath = os.path.join(folderout, output_filename)
df_anonymized.to_excel(output_filepath, sheet_name='hash', index=False)

# Inverser l'anonymisation
df_deanonymized = deanonymize(df_anonymized, 'ID')
output_filename = os.path.splitext(filename)[0] + '_deanonymized.xlsx'
output_filepath = os.path.join(folderout, output_filename)
df_deanonymized.to_excel(output_filepath, sheet_name='hash', index=False)
