import os
import pandas as pd
import hashlib

# fonction de déanonymisation
def deanonymize(value, secret_key):
    # utiliser la clé secrète pour déanonymiser la valeur
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

# récupérer la clé secrète
secret_key = input("Entrez la clé secrète : ")

# déanonymiser les données
for col in data.columns:
    data[col] = data[col].apply(deanonymize, args=(secret_key,))

# exporter les données déanonymisées dans un fichier Excel
output_file = input("Entrez le nom du fichier de sortie : ")
data.to_excel(output_file, index=False)
print("Les données ont été déanonymisées avec succès et exportées dans le fichier", output_file)
