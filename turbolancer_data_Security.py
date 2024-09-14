from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64

def pad(text):
    block_size = 16
    padding_length = block_size - (len(text) % block_size)
    padding = bytes([padding_length]) * padding_length
    return text + padding

def unpad(padded_text):
    padding_length = padded_text[-1]
    return padded_text[:-padding_length]

def encrypt(key, text):
    try:
        backend = default_backend()
        cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
        encryptor = cipher.encryptor()

        padded_text = pad(text.encode())

        ciphertext = encryptor.update(padded_text) + encryptor.finalize()

        encrypted_data = base64.urlsafe_b64encode(ciphertext).decode().rstrip("=")
        return encrypted_data
    except Exception as e:
        return f"Encryption Error: {str(e)}"

def decrypt(key, encrypted_data):
    try:
        backend = default_backend()

        padding_length = len(encrypted_data) % 4
        encrypted_data += "=" * padding_length

        ciphertext = base64.urlsafe_b64decode(encrypted_data.encode())

        cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
        decryptor = cipher.decryptor()

        padded_text = decryptor.update(ciphertext) + decryptor.finalize()

        text = unpad(padded_text).decode()
        return text
    except Exception as e:
        return f"Decryption Error: {str(e)}"
