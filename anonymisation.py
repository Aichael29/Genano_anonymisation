import os
import pandas as pd
import hashlib

# définir la clé secrète
secret_key = "y3HsVaFY9Uj<\C#*!nMnK,*%q=F?dR4WA|s(bwisfcU<q.P\&L"

# fonction d'anonymisation
def anonymize(value):
    # appliquer une fonction de hachage avec la clé secrète pour anonymiser la valeur
    return hashlib.sha512(bytearray(str(value).strip()+secret_key, "utf8")).hexdigest()[:20]

# charger le fichier de données
input_file = input("Entrez le nom du fichier d'entrée : ")
if os.path.splitext(input_file)[1] == '.csv':
    data = pd.read_csv(input_file)
elif os.path.splitext(input_file)[1] == '.xlsx':
    data = pd.read_excel(input_file)
else:
    print("Le format de fichier n'est pas supporté.")
    exit()

# anonymiser les données
for col in data.columns:
    data[col] = data[col].apply(anonymize)

# exporter les données anonymisées dans un fichier Excel
output_file = input("Entrez le nom du fichier de sortie : ")
data.to_excel(output_file, index=False)
print("Les données ont été anonymisées avec succès et exportées dans le fichier", output_file)
