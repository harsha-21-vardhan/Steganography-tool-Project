from PIL import Image
import stepic
import base64
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes

BLOCK_SIZE = 16

# Padding for encryption
def pad(s):
    return s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)

def unpad(s):
    return s[:-ord(s[len(s)-1:])]

def derive_key(password, salt):
    return PBKDF2(password, salt, dkLen=32, count=1000000)

def encrypt_message(message, password):
    salt = get_random_bytes(16)
    key = derive_key(password.encode(), salt)
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(message).encode())
    return base64.b64encode(salt + cipher.iv + ct_bytes).decode()

def decrypt_message(ciphertext, password):
    raw = base64.b64decode(ciphertext.encode())
    salt = raw[:16]
    iv = raw[16:32]
    ct = raw[32:]
    key = derive_key(password.encode(), salt)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ct).decode())

def encode_text(image_path, message, output_path):
    image = Image.open(image_path)
    encoded_image = stepic.encode(image, message.encode())
    encoded_image.save(output_path, 'PNG')

def decode_text(image_path):
    image = Image.open(image_path)
    data = stepic.decode(image)
    if isinstance(data, bytes):
        return data.decode()
    return data  # Already a string


def encode_file(image_path, file_path, output_path):
    with open(file_path, "rb") as f:
        data = f.read()
    image = Image.open(image_path)
    encoded_image = stepic.encode(image, data)
    encoded_image.save(output_path, 'PNG')

def decode_file(image_path, output_file_path):
    image = Image.open(image_path)
    data = stepic.decode(image)
    with open(output_file_path, "wb") as f:
        f.write(data)
