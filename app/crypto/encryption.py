"""AES-256-GCM encryption for API keys"""

import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from app.config import settings


def _get_cipher() -> Fernet:
    """Get Fernet cipher from encryption key."""
    if not settings.encryption_key:
        raise ValueError("ENCRYPTION_KEY not configured. Set ENCRYPTION_KEY in .env")

    # Derive a 32-byte key from the settings key using PBKDF2
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b"ai-gateway-salt",  # Fixed salt for consistency
        iterations=480000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(settings.encryption_key.encode()))
    return Fernet(key)


def encrypt_key(plain_key: str) -> str:
    """Encrypt an API key."""
    cipher = _get_cipher()
    encrypted = cipher.encrypt(plain_key.encode())
    return base64.urlsafe_b64encode(encrypted).decode()


def decrypt_key(encrypted_key: str) -> str:
    """Decrypt an API key."""
    cipher = _get_cipher()
    decoded = base64.urlsafe_b64decode(encrypted_key.encode())
    decrypted = cipher.decrypt(decoded)
    return decrypted.decode()
