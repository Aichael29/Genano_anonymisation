import pandas as pd
import hashlib
import configparser

# Lecture du fichier de configuration
config = configparser.ConfigParser()
config.read('configuration.conf')

# Colonnes à hasher
colonnes = config['Operations'].get('colonnes', None)
if colonnes is None:
    colonnes = []

# Charger le fichier Excel dans un dataframe Pandas
fichier_entree = config['fileinfo']['fichier_entree']
df = pd.read_excel(fichier_entree)

# Définir une fonction pour hasher les valeurs d'une colonne avec SHA256
def sha256_hash(value):
    return hashlib.sha256(value.encode()).hexdigest()

# Appliquer la fonction de hashage à chaque colonne choisie
if colonnes:
    colonnes = colonnes.split(',')
else:
    colonnes = df.columns.tolist()
for col in colonnes:
    df[col] = df[col].apply(lambda x: sha256_hash(str(x)))

# Enregistrer le fichier Excel hashé
fichier_sortie = config['fileinfo']['fichier_sortie']
df.to_excel(fichier_sortie, index=False)
