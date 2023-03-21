## Introduction:
Le chiffrement de données est un processus important pour protéger la confidentialité des informations sensibles. Dans ce contexte, le chiffrement de fichiers est une technique de chiffrement de données qui permet de protéger le contenu d'un fichier en le convertissant en un format illisible, ce qui rend son contenu illisible pour toute personne n'ayant pas la clé de chiffrement. Cela est particulièrement utile pour protéger des fichiers contenant des données sensibles, telles que des informations de compte, des données personnelles, des plans de projet, des données financières et autres informations confidentielles.

## Objectif:
L'objectif de ce projet est d'implémenter un chiffrement de fichiers basé sur le chiffrement AES (Advanced Encryption Standard) à l'aide du module Cryptodome en Python. Ce projet comprend deux scripts: le premier script crypte les données d'un fichier Excel et le deuxième script décrypte les données du fichier Excel crypté.

## Fonctionnalités:

Lecture de la configuration à partir d'un fichier de configuration (configuration.conf)
Vérification de la taille de la clé de chiffrement et de la validité du mode de chiffrement
Définition de la fonction de chiffrement AES et de la fonction de déchiffrement AES
Cryptage des données d'un fichier Excel à l'aide du script crypt.py
Décryptage des données d'un fichier Excel crypté à l'aide du script decrypt.py
Enregistrement des données chiffrées/déchiffrées dans un nouveau fichier Excel

## Fonctionnement:
Le script crypt.py lit le fichier Excel en entrée et applique la fonction de chiffrement AES à chaque colonne du dataframe. Les données chiffrées sont ensuite enregistrées dans un nouveau fichier Excel. Le script decrypt.py lit le fichier Excel chiffré en entrée et applique la fonction de déchiffrement AES à chaque colonne du dataframe. Les données déchiffrées sont ensuite enregistrées dans un nouveau fichier Excel.

## Conclusion:
Le chiffrement de fichiers est un processus important pour protéger la confidentialité des informations sensibles. Ce projet montre comment utiliser le chiffrement AES pour crypter et décrypter les données d'un fichier Excel à l'aide du module Cryptodome en Python. En appliquant les méthodes de chiffrement et de déchiffrement aux données sensibles, les utilisateurs peuvent s'assurer que leurs données sont en sécurité et protégées contre tout accès non autorisé.