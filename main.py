import configparser

# lire le fichier de configuration
config = configparser.ConfigParser()
config.read("configuration.config")

input_file = config["fileinfo"]["fichier_entree"]
output_file = config["fileinfo"]["fichier_sortie"]
mode_chiffrement = config["anonymization"]["mode_chiffrement"]
operation = config["anonymization"]["operation"]
key = config["anonymization"]["cle_chiffrement"].encode()
vector = config["anonymization"]["vector"].encode()
colonnes = config["anonymization"]["colonnes"].split(",")
if operation == "chiffrement":
    pass #crypt(input_file, output_file, key, vector, mode_chiffrement)
elif operation == "dechiffrement":
    pass #decrypt(input_file, output_file, key, vector, mode_chiffrement)
elif operation == "hashage":
    pass  # ajouter la fonctionnalité de hashage
else:
    raise ValueError("Invalid operation value. Expected 'chiffrement', 'dechiffrement', or 'hashage'")
