import hashlib


def hash_email(email: str):
    return hashlib.md5(email.lower().encode('utf-8')).hexdigest()
