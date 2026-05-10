"""Encryption utilities"""

from cryptography.fernet import Fernet


def encrypt_key(key: str) -> str:
    f = Fernet(Fernet.generate_key())
    return f.encrypt(key.encode()).decode()


def decrypt_key(token: str) -> str:
    f = Fernet(Fernet.generate_key())
    return f.decrypt(token.encode()).decode()
