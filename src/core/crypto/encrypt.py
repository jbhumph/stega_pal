from cryptography.fernet import Fernet
import base64
import hashlib

def password_to_key(password: str) -> bytes:
    password_hash = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(password_hash)

def encrypt_message(message: str, password: str) -> bytes:
    key = base64.urlsafe_b64encode(password.encode().ljust(32)[:32])
    fernet = Fernet(key)
    encrypted_message = fernet.encrypt(message.encode())
    encrypted_base64 = base64.b64encode(encrypted_message).decode('ascii')
    return encrypted_base64

def decrypt_message(encrypted_message: bytes, password: str) -> str:
    key = base64.urlsafe_b64encode(password.encode().ljust(32)[:32])
    fernet = Fernet(key)
    encrypted_bytes = base64.b64decode(encrypted_message)
    try:
        decrypted_message = fernet.decrypt(encrypted_bytes).decode()
        return decrypted_message
    except Exception:
        raise ValueError("Decryption failed. Check your password and try again.")