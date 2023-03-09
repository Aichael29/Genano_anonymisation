import argparse
import pandas as pd
from crypt import chiffrement
from decrypt import dechiffrement
from hash import hashage
from verify import verification

# Fonction pour demander à l'utilisateur s'il souhaite chiffrer/déchiffrer toutes les colonnes ou spécifier des colonnes
def ask_columns():
    while True:
        choice = input("Voulez-vous chiffrer/déchiffrer toutes les colonnes (o/n) ? ")
        if choice.lower() == 'o':
            return None
        elif choice.lower() == 'n':
            cols = input("Entrez le nom des colonnes séparées par des virgules: ")
            return cols.split(',')
        else:
            print("Veuillez entrer 'o' ou 'n'.")

# Fonction pour demander à l'utilisateur si le fichier doit être hashé
def ask_hash():
    while True:
        choice = input("Voulez-vous calculer le hash du fichier (o/n) ? ")
        if choice.lower() == 'o':
            return True
        elif choice.lower() == 'n':
            return False
        else:
            print("Veuillez entrer 'o' ou 'n'.")

# Fonction pour demander à l'utilisateur si le fichier doit être vérifié avec un hash
def ask_verify():
    while True:
        choice = input("Voulez-vous vérifier le hash du fichier (o/n) ? ")
        if choice.lower() == 'o':
            return True
        elif choice.lower() == 'n':
            return False
        else:
            print("Veuillez entrer 'o' ou 'n'.")

# Analyser les arguments de ligne de commande
parser = argparse.ArgumentParser(description='Programme de chiffrement/déchiffrement de fichiers')
parser.add_argument('action', help='Action à effectuer (chiffrer, déchiffrer, hasher, vérifier)')
parser.add_argument('filename', help='Nom du fichier à traiter')
parser.add_argument('output', help='Nom du fichier de sortie')
args = parser.parse_args()

# Exécuter l'action correspondante
if args.action == 'chiffrer':
    columns = ask_columns()
    chiffrement(args.filename, args.output, columns)
elif args.action == 'dechiffrer':
    columns = ask_columns()
    dechiffrement(args.filename, args.output, columns)
elif args.action == 'hasher':
    hashage(args.filename)
elif args.action == 'vérifier':
    hash = input("Entrez le hash du fichier: ")
    verification(args.filename, hash)
else:
    print('Action non reconnue.')

# Demander à l'utilisateur si le fichier doit être hashé et vérifié (uniquement pour les actions de chiffrement/déchiffrement)
if args.action in ['chiffrer', 'dechiffrer']:
    hash_file = ask_hash()
    if hash_file:
        hash = hashage(args.output)
        print(f"Le hash du fichier est: {hash}")

    verify_file = ask_verify()
    if verify_file:
        hash = input("Entrez le hash du fichier: ")
        verification(args.output, hash)
