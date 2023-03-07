# projetData_Inwi

##### Le code fourni est un script Python qui permet d'anonymiser une colonne d'un fichier de données et de dé-anonymiser cette colonne par la suite en utilisant une technique de hachage.

### Générer une clé aléatoire de 64 caractères en utilisant SHA-512

def generate_secret_key():
    secret_key = hashlib.sha512(os.urandom(64)).hexdigest()
    return secret_key

   ####    Test de la fonction

secret_key = generate_secret_key()
print(secret_key)

Ce code va générer une clé aléatoire de 128 caractères (64 octets) en utilisant SHA-512 et l'afficher à l'écran. Vous pouvez exécuter ce code plusieurs fois pour générer des clés secrètes différentes à chaque fois.


### Fonction pour nettoyer le hachage en renvoyant les 20 premiers caractères

Ce code utilise la fonction de hachage SHA-512 pour anonymiser une colonne "ID" d'un DataFrame Pandas. La fonction "cleanhash" nettoie le hachage en ne gardant que les 20 premiers caractères. La méthode "apply" est utilisée pour appliquer cette fonction à chaque ligne de la colonne "ID" du DataFrame.
La sortie du premier "print" montre le DataFrame original avec la colonne "ID" anonymisée en utilisant la fonction de hachage SHA-512. La sortie du deuxième "print" montre le DataFrame anonymisé ré-anonymisé à l'aide de la fonction de hachage SHA-512.

### Fonction pour anonymiser une colonne dans un dataframe

La fonction anonymize prend en entrée un dataframe df et une colonne column et ajoute une nouvelle colonne avec le nom column_hash qui contient les valeurs de la colonne column hachées à l'aide de la fonction cleanhash. Elle renvoie le dataframe avec la nouvelle colonne ajoutée.

### Fonction pour déanonymiser une colonne dans un dataframe

La fonction deanonymize(df, column) prend en entrée un dataframe et le nom de la colonne à déanonymiser. Elle applique la même fonction de hachage pour inverser l'anonymisation en utilisant la colonne de hachage et renvoie le dataframe déanonymisé en supprimant la colonne de hachage.

