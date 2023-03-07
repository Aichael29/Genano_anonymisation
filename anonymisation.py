import hashlib

# Clé secrète pour le hachage
seckey = "y3HsVaFY9Uj<\C#*!nMnK,*%q=F?dR4WA|s(bwisfcU<q.P\&L"

# Fonction pour nettoyer et hacher chaque valeur dans une colonne
def cleanhash(s):
    return hashlib.sha512(bytearray(str(s).strip()+seckey, "utf8")).hexdigest()[:20]

# Fonction pour anonymiser les colonnes sélectionnées dans le dataframe
def anonymize(df, cols):
    df_anon = df.copy()
    for col in cols:
        df_anon[col] = df_anon[col].apply(cleanhash)
    return df_anon
