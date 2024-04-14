import os
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asymmetric_padding
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def generate_keys(options):
    symmetric_key_path = options['symmetric_key']
    public_key_path = options['public_key']
    private_key_path = options['private_key']
    
    symmetric_key = os.urandom(16)
    with open(symmetric_key_path, 'wb') as f:
        f.write(symmetric_key)
    
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()
    
    with open(public_key_path, 'wb') as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))
    with open(private_key_path, 'wb') as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))
    
    print("Keys generated successfully.")

def encrypt_data(options):
    input_file_path = options['input_file']
    public_key_path = options['public_key']
    encrypted_key_path = options['encrypted_key']
    output_file_path = options['output_file']
    
    with open(input_file_path, 'rb') as f:
        plaintext = f.read()
    
    symmetric_key = os.urandom(16)
    
    with open(public_key_path, 'rb') as f:
        public_key = serialization.load_pem_public_key(
            f.read(),
            backend=default_backend()
        )
    encrypted_key = public_key.encrypt(
        symmetric_key,
        asymmetric_padding.OAEP(
            mgf=asymmetric_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    with open(encrypted_key_path, 'wb') as f:
        f.write(encrypted_key)
    
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(symmetric_key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(128).padder()
    padded_plaintext = padder.update(plaintext) + padder.finalize()
    ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
    
    with open(output_file_path, 'wb') as f:
        f.write(iv)
        f.write(ciphertext)
    
    print("Data encrypted successfully.")

def decrypt_data(options):
    input_file_path = options['input_file']
    private_key_path = options['private_key']
    encrypted_key_path = options['encrypted_key']
    output_file_path = options['output_file']
    
    with open(encrypted_key_path, 'rb') as f:
        encrypted_key = f.read()
    
    with open(private_key_path, 'rb') as f:
        private_key = serialization.load_pem_private_key(
            f.read(),
            password=None,
            backend=default_backend()
        )
    symmetric_key = private_key.decrypt(
        encrypted_key,
        asymmetric_padding.OAEP(
            mgf=asymmetric_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    with open(input_file_path, 'rb') as f:
        iv = f.read(16)
        ciphertext = f.read()
    
    cipher = Cipher(algorithms.AES(symmetric_key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    unpadder = padding.PKCS7(128).unpadder()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    plaintext = unpadder.update(plaintext) + unpadder.finalize()
    
    with open(output_file_path, 'wb') as f:
        f.write(plaintext)
    
    print("Data decrypted successfully.")