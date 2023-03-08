import pandas as pd
import hashlib

# Clé secrète utilisée pour l'anonymisation
seckey = "y3HsVaFY9Uj<\C#*!nMnK,*%q=F?dR4WA|s(bwisfcU<q.P\&L"

# Fonction pour récupérer l'ID original à partir du hash
def get_id(hash):
    # Essayer les 1 000 000 premiers entiers en les hashant avec la clé secrète et en comparant les 20 premiers
    # caractères du hash avec le hash fourni. Si une correspondance est trouvée, renvoyer l'entier correspondant.
    for i in range(1000000):
        if hashlib.sha512(bytearray(str(i).strip()+seckey, "utf8")).hexdigest()[:20] == hash:
            return i
    # Si aucune correspondance n'est trouvée, renvoyer None.
    return None

# Fonction pour désanonymiser une colonne
def dehash_column(df, col_name):
    if df[col_name].dtype == pd.np.object or df[col_name].dtype == pd.np.str:
        # Si la colonne contient des chaînes de caractères, appliquer la fonction get_id() à chaque élément de la colonne
        # pour récupérer l'ID original correspondant au hash
        df[col_name] = pd.Series([get_id(df[col_name][i]) for i in range(len(df[col_name]))])
    else:
        # Si la colonne contient des nombres, appliquer la fonction get_id() à chaque élément de la colonne
        # pour récupérer l'ID original correspondant au hash
        df[col_name] = df[col_name].apply(get_id)

# Fonction pour désanonymiser plusieurs colonnes
def dehash_columns(df, col_names):
    for col_name in col_names:
        # Appliquer la fonction dehash_column() à chaque colonne indiquée dans la liste col_names
        dehash_column(df, col_name)
