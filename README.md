
# Projet d'anonymisation de données

Ce projet permet d'anonymiser et de désanonymiser des données contenues dans un fichier Excel. Les données à anonymiser doivent être sélectionnées par l'utilisateur. L'anonymisation est effectuée à l'aide d'un hashage et d'une clé secrète, tandis que la désanonymisation se fait en retrouvant les valeurs originales à partir des hashs correspondants.

Le projet est composé de 3 fichiers Python :

anonymisation.py : contient les fonctions pour anonymiser une colonne et plusieurs colonnes d'un DataFrame
deanonymisation.py : contient les fonctions pour désanonymiser une colonne et plusieurs colonnes d'un DataFrame
main.py : contient le script principal pour demander à l'utilisateur les informations nécessaires et effectuer l'anonymisation et la désanonymisation

## Utilisation :

Placer le fichier Excel à anonymiser dans un dossier d'entrée
Lancer le script main.py et suivre les instructions
Le fichier Excel anonymisé sera créé dans un dossier de sortie avec le nom spécifié par l'utilisateur
Pour désanonymiser les colonnes, relancer le script main.py et choisir les colonnes à désanonymiser ainsi que le fichier Excel anonymisé généré précédemment
Le fichier Excel désanonymisé sera créé dans le même dossier de sortie avec un nom différent


