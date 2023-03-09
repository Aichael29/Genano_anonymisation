import pandas as pd
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad

# Load the Excel file into a pandas dataframe
df = pd.read_excel('input.xlsx')

# Choose the column you want to encrypt
column_to_encrypt = 'phone number'

# Define a function to encrypt the values in the column
def aes_encrypt(value, key):
    cipher = AES.new(key.encode(), AES.MODE_ECB)
    padded_value = pad(value.encode(), AES.block_size)
    encrypted_value = cipher.encrypt(padded_value)
    return encrypted_value.hex()

# Set a key for encryption
key = 'my_secret_key123'

# Apply the encryption function to the chosen column
df[column_to_encrypt] = df[column_to_encrypt].apply(lambda x: aes_encrypt(x, key))

# Save the encrypted file
df.to_excel('output_file.xlsx', index=False)
