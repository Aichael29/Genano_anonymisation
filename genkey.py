import secrets
from Crypto.PublicKey import RSA

key = RSA.generate(2048, randfunc=lambda n: int.from_bytes(secrets.token_bytes((n.bit_length() + 7) // 8), 'big'))

# Enregistrer la clé privée
with open('private_key.pem', 'wb') as f:
    f.write(key.export_key('PEM'))

# Enregistrer la clé publique
with open('public_key.pem', 'wb') as f:
    f.write(key.publickey().export_key('PEM'))
