import hashlib
from openpyxl import load_workbook

def generate_hash(file_path):
    # Charge le fichier XLSX avec openpyxl
    workbook = load_workbook(filename=file_path, read_only=True)

    # Récupère le contenu de chaque cellule de chaque feuille
    content = ''
    for sheet in workbook:
        for row in sheet:
            for cell in row:
                if cell.value:
                    content += str(cell.value)

    # Calcule le hash SHA256 du contenu
    sha256 = hashlib.sha256()
    sha256.update(content.encode('utf-8'))
    return sha256.hexdigest()

if __name__ == '__main__':
    # Exemple d'utilisation

    #Générer le hash du fichier
    hash_value1 = generate_hash("C:\\Users\\Lenovo\\Pictures\\input.xlsx")

    # Générer le hash du fichier
    hash_value2 = generate_hash("C:\\Users\\Lenovo\\Pictures\\input.xlsx")

    # Vérifier si le hash calculé correspond au hash attendu
    if hash_value1 == hash_value2:
        print('Les données du fichier sont intègres.')
    else:
        print('Les données du fichier sont corrompues.')