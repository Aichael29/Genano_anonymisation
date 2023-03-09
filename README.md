# Chiffrement et décryptage de colonnes dans un fichier Excel à l'aide de l'algorithme AES
chiffrement et décryptage de colonnes dans un fichier Excel à l'aide de l'algorithme de chiffrement symétrique AES en mode ECB.

Le fichier Excel est lu dans un dataframe Pandas à l'aide de la bibliothèque pandas. La colonne à chiffrer est choisie et une fonction est définie pour effectuer le chiffrement. La clé de chiffrement est définie manuellement dans le code.

Une fois la colonne chiffrée, le dataframe est enregistré dans un nouveau fichier Excel. Pour décrypter la colonne chiffrée, le fichier Excel est lu dans un nouveau dataframe Pandas et la fonction de décryptage est appliquée à la colonne choisie. Le dataframe décrypté est ensuite enregistré dans un autre fichier Excel.