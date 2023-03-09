import pandas as pd
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import unpad

# Load the encrypted Excel file into a pandas dataframe
df = pd.read_excel('output_file.xlsx')

# Choose the column you want to decrypt
column_to_decrypt = 'phone number'

# Define a function to decrypt the values in the column
def aes_decrypt(value, key):
    cipher = AES.new(key.encode(), AES.MODE_ECB)
    decrypted_value = cipher.decrypt(bytes.fromhex(value))
    unpadded_value = unpad(decrypted_value, AES.block_size)
    return unpadded_value.decode()

# Set the key for decryption
key = 'my_secret_key123'

# Apply the decryption function to the chosen column
df[column_to_decrypt] = df[column_to_decrypt].apply(lambda x: aes_decrypt(x, key))

# Save the decrypted file
df.to_excel('decrypted_file.xlsx', index=False)
