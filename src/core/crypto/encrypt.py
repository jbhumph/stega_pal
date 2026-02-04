from cryptography.fernet import Fernet
import base64
import hashlib

def password_to_key(password: str) -> bytes:
    password_hash = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(password_hash)

def encrypt_message(message: str, password: str) -> bytes:
    key = password_to_key(password)
    fernet = Fernet(key)
    encrypted_message = fernet.encrypt(message.encode())
    return encrypted_message

def decrypt_message(encrypted_message: bytes, password: str) -> str:
    key = password_to_key(password)
    fernet = Fernet(key)
    try:
        decrypted_message = fernet.decrypt(encrypted_message).decode()
        return decrypted_message
    except Exception:
        raise ValueError("Decryption failed. Check your password and try again.")