import hashlib

# La fonction cleanhash prend une chaîne de caractères (s) et une clé (key) en entrée,
# ajoute la clé à la chaîne de caractères, calcule le hachage SHA-512 et retourne
# les 20 premiers caractères du hachage en tant que chaîne de caractères.
def cleanhash(s, key):
    return hashlib.sha512(bytearray(str(s).strip()+key, "utf8")).hexdigest()[:20]
