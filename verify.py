import hashlib


def verification(filename, expected_hash):
    # Ouvrir le fichier en mode binaire
    with open(filename, 'rb') as f:
        # Calculer le hash SHA256 du fichier
        h = hashlib.sha256()
        h.update(f.read())
        file_hash = h.hexdigest()

        # Vérifier si le hash calculé correspond au hash attendu
        if file_hash == expected_hash:
            print(f'Le hash du fichier {filename} correspond au hash attendu.')
        else:
            print(f'ERREUR : Le hash du fichier {filename} ne correspond pas au hash attendu.')
