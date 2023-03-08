import pandas as pd
import numpy as np
import hashlib
import string
import random

# Clé secrète utilisée pour l'anonymisation
seckey = "y3HsVaFY9Uj<\C#*!nMnK,*%q=F?dR4WA|s(bwisfcU<q.P\&L"

# Fonction pour récupérer le hash à partir de l'ID original
def get_hash(id):
    # Concaténer l'ID avec la clé secrète, puis hasher la chaîne de caractères résultante avec SHA-512
    # et récupérer les 20 premiers caractères du hash
    return hashlib.sha512(bytearray(str(id).strip()+seckey, "utf8")).hexdigest()[:20]

# Fonction pour anonymiser une colonne
def anonymize_column(col):
    if col.dtype == np.int64 or col.dtype == np.float64:
        # Si la colonne contient des nombres, appliquer la fonction get_hash() à chaque élément de la colonne
        return col.apply(get_hash)
    elif col.dtype == np.object or col.dtype == np.str:
        # Si la colonne contient des chaînes de caractères, générer une nouvelle chaîne aléatoire de même longueur
        # pour chaque élément de la colonne
        return pd.Series([random_string() for i in range(len(col))])
    else:
        # Si la colonne ne contient ni nombres ni chaînes de caractères, convertir la colonne en type float64
        # et appliquer la fonction get_hash() à chaque élément de la colonne
        return col.astype(np.float64).apply(get_hash)

# Fonction pour anonymiser plusieurs colonnes
def anonymize(df, col_names):
    for col_name in col_names:
        # Appliquer la fonction anonymize_column() à chaque colonne indiquée dans la liste col_names
        df[col_name] = anonymize_column(df[col_name])
    return df

# Fonction pour générer une chaîne de caractères aléatoire
def random_string(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))
