import hashlib

def hashage(filename):
    # Ouvrir le fichier en mode binaire
    with open(filename, 'rb') as f:
        # Calculer le hash SHA256 du fichier
        h = hashlib.sha256()
        h.update(f.read())
        print(f'Le hash SHA256 du fichier {filename} est : {h.hexdigest()}')
