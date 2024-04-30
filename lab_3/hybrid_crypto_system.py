import os
import logging

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from asymmetric_crypto import AsymmetricCrypto
from symmetric_crypto import SymmetricCrypto
from file_utils import read_file, write_file


logging.basicConfig(level=logging.INFO)


class HybridCryptoSystem:
    """
    Class to perform hybrid cryptography operations.
    """

    def generate_keys(options: dict) -> None:
        """
        Generate RSA key pair and a symmetric key, and save them to files.

        Args:
            options (dict): A dictionary containing the paths for public key,
                private key, and encrypted symmetric key.

        Returns:
            None
        """
        logging.basicConfig(level=logging.INFO)

        public_key_path = options['public_key']
        private_key_path = options['private_key']

        symmetric_key = os.urandom(16)
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        public_key = private_key.public_key()

        write_file(public_key_path, public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))
        write_file(private_key_path, private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

        encrypted_key = AsymmetricCrypto.encrypt_with_public_key(public_key, symmetric_key)
        write_file(options['encrypted_key'], encrypted_key)

        logging.info("Keys generated successfully.")


    def encrypt_data(options: dict) -> None:
        """
        Encrypt data using RSA and symmetric key, and save to a file.

        Args:
            options (dict): A dictionary containing the paths for input file,
                encrypted key, private key, and output file.

        Returns:
            None
        """
        logging.basicConfig(level=logging.INFO)

        output_file_path = options['output_file']

        try:
            plaintext = read_file(options['input_file'])
            encrypted_key = read_file(options['encrypted_key'])
            private_key_bytes = read_file(options['private_key'])

            private_key = AsymmetricCrypto.decrypt_private_key(private_key_bytes)

            symmetric_key = AsymmetricCrypto.decrypt_with_private_key(private_key, encrypted_key)

            iv, ciphertext = SymmetricCrypto.encrypt(symmetric_key, plaintext)

            with open(output_file_path, 'wb') as f:
                f.write(iv)
                f.write(ciphertext)

            logging.info("Data encrypted successfully.")

        except Exception as e:
            logging.error(f"Error occurred while encrypting data: {e}")


    def decrypt_data(options: dict) -> None:
        """
        Decrypt data using RSA and symmetric key, and save to a file.

        Args:
            options (dict): A dictionary containing the paths for input file,
                encrypted key, private key, and output file.

        Returns:
            None
        """
        logging.basicConfig(level=logging.INFO)

        input_file_path = options['input_file']
        private_key_path = options['private_key']

        try:
            encrypted_key = read_file(options['encrypted_key'])

            private_key_bytes = read_file(private_key_path)
            private_key = AsymmetricCrypto.decrypt_private_key(private_key_bytes)

            symmetric_key = AsymmetricCrypto.decrypt_with_private_key(private_key, encrypted_key)

            with open(input_file_path, 'rb') as f:
                iv = f.read(16)
                ciphertext = f.read()

            plaintext = SymmetricCrypto.decrypt(symmetric_key, iv, ciphertext)

            write_file(options['output_file'], plaintext)

            logging.info("Data decrypted successfully.")

        except Exception as e:
            logging.error(f"Error occurred while decrypting data: {e}")