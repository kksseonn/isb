import os
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asymmetric_padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives import padding, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from file_utils import read_file, write_file

def generate_keys(options):
    public_key_path = options['public_key']
    private_key_path = options['private_key']
    
    symmetric_key = os.urandom(16)
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

    encrypted_key = public_key.encrypt(
        symmetric_key,
        asymmetric_padding.OAEP(
            mgf=asymmetric_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    write_file(options['encrypted_key'], encrypted_key)
    
    print("Keys generated successfully.")

def encrypt_data(options):
    output_file_path = options['output_file']

    plaintext = read_file(options['input_file'])
    encrypted_key = read_file(options['encrypted_key'])
    private_bytes = read_file(options['private_key'])

    d_private_key = load_pem_private_key(private_bytes,password=None,)
    
    symmetric_key = d_private_key.decrypt(encrypted_key, asymmetric_padding.OAEP(mgf=asymmetric_padding.MGF1(algorithm=hashes.SHA256()),
                                                            algorithm=hashes.SHA256(), label=None))

    iv = os.urandom(16)
    cipher = Cipher(algorithms.SM4(symmetric_key), modes.CBC(iv))
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
    
    encrypted_key = read_file(options['encrypted_key'])

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
    
    cipher = Cipher(algorithms.SM4(symmetric_key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    unpadder = padding.PKCS7(128).unpadder()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    plaintext = unpadder.update(plaintext) + unpadder.finalize()
    
    write_file(options['output_file'], plaintext)
    
    print("Data decrypted successfully.")