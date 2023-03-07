'''import pandas as pd


def deanonymize_excel(anonymized_filename, original_filename):
    # Charger les fichiers Excel
    df_anonymized = pd.read_excel(anonymized_filename)
    df_original = pd.read_excel(original_filename)

    # Extraire les colonnes qui ont été anonymisées
    cols_to_anonymize = [col for col in df_anonymized.columns if col.startswith("anon_")]

    # Remplacer les valeurs anonymisées par les valeurs originales
    for col in cols_to_anonymize:
        df_anonymized[col] = df_anonymized[col].apply(
            lambda x: df_original.loc[df_original[col].astype(str) == x, col].iloc[0])

    # Enregistrer le fichier Excel déanonymisé
    deanonymized_filename = f"deanonymized_{anonymized_filename}"
    df_anonymized.to_excel(deanonymized_filename, index=False)

    return deanonymized_filename
'''