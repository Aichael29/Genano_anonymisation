
# projet_anony&deanony
Ce projet vise à fournir une solution de traitement de données permettant d'anonymiser et de dé-anonymiser les données.

### anonymisation :

Ce script charge un fichier de données en entrée, qui peut être soit un fichier CSV, soit un fichier Excel.
Les données sont anonymisées en utilisant la fonction "anonymize()", qui applique une fonction de hachage à chaque colonne du dataframe. Les colonnes originales sont supprimées et remplacées par de nouvelles colonnes contenant le hachage.
Les données anonymisées sont exportées dans un fichier CSV.
Le script utilise les modules os, pandas et hashlib.

### deanonymisation :

Ce script charge un fichier de données en entrée, qui peut être soit un fichier CSV, soit un fichier Excel.
Les données sont déanonymisées en utilisant la fonction "deanonymize()", qui inverse la fonction de hachage appliquée lors de l'anonymisation pour retrouver les valeurs d'origine.
Les données déanonymisées sont exportées dans un fichier Excel.
Le script utilise les modules os, pandas et hashlib.