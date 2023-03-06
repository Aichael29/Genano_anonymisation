import pandas as pd
from hash_ids import cleanhash

def hash_excel_file(input_file, output_file, id_column='ID', key='y3HsVaFY9Uj<\C#*!nMnK,*%q=F?dR4WA|s(bwisfcU<q.P\&L'):
    try:
        df_input = pd.read_excel(input_file, header=0)
    except FileNotFoundError:
        print(f"Error: input file '{input_file}' not found")
        exit()

    if id_column not in df_input.columns:
        print(f"Error: column '{id_column}' not found in input file")
        exit()

    try:
        df_input['id_hash'] = df_input[id_column].apply(lambda x: cleanhash(x, key))
    except:
        print("Error: an unexpected error occurred while hashing the IDs")
        exit()

    try:
        df_input.to_excel(output_file, sheet_name='hash', index=False)
    except PermissionError:
        print(f"Error: could not write to output file '{output_file}'")
        exit()

