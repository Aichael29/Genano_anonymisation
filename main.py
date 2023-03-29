import configparser
import sys
import subprocess
import time

start=time.time()
# Lecture du fichier de configuration
config = configparser.ConfigParser()
config.read('configuration.conf')

# Opération à effectuer
operation = config['Operations']['operation']

# Exécuter le fichier Python correspondant à l'opération
if operation == 'chiffrement':
    subprocess.run(['python', 'crypt.py'])
elif operation == 'dechiffrement':
    subprocess.run(['python', 'decrypt.py'])
elif operation == 'hashage':
    subprocess.run(['python', 'hash.py'])
else:
    print("Opération non reconnue.")
    sys.exit(1)

end=time.time()
print("xlsx généré en " + str(end - start) + " secondes")
