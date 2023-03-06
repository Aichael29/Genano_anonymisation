import hashlib

def cleanhash(s, key):
    return hashlib.sha512(bytearray(str(s).strip()+key, "utf8")).hexdigest()[:20]