import configparser
import os

config = configparser.ConfigParser()
config.read('configuration.conf')

fichier_entree = config['fileinfo']['fichier_entree']
fichier_sortie = config['fileinfo']['fichier_sortie']
type = os.path.splitext(fichier_entree)[1].lower()
operation = config['Operations']['operation']
colonnes = config['Operations'].get('colonnes', None)
if colonnes is None:
    colonnes = []


if operation in ["chiffrement", "dechiffrement"]:
    mode_chiffrement = config['Operations']['mode_chiffrement']
    if mode_chiffrement not in ('ECB', 'CBC'):
        print("Le mode de chiffrement doit être soit ECB ou CBC.")
        exit()
    cle_chiffrement = config['Operations']['cle_chiffrement']
    if len(cle_chiffrement) != 16:
        print("La clé doit être de 16 caractères.")
        exit()
    if mode_chiffrement == "CBC":
        vecteur = config['Operations']['vector']
        if mode_chiffrement == 'CBC' and len(vecteur) != 16:
            print("Le vecteur d'initialisation doit être de 16 octets.")
            exit()

