import logging
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding as asymmetric_padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key


logging.basicConfig(level=logging.INFO)


class AsymmetricCrypto:
    """
    Class providing methods for asymmetric cryptography operations.
    """

    def decrypt_private_key(private_key_bytes: bytes):
        """
        Decrypt the private key.

        Args:
            private_key_bytes (bytes): The bytes representing the private key.

        Returns:
            RSAPrivateKey: The decrypted private key.
        """
        try:
            return load_pem_private_key(private_key_bytes, password=None)
        except Exception as e:
            logging.error(f"Error occurred while decrypting private key: {e}")

    def decrypt_with_private_key(private_key, encrypted_data: bytes) -> bytes:
        """
        Decrypt data using the private key.

        Args:
            private_key (RSAPrivateKey): The private key to use for decryption.
            encrypted_data (bytes): The encrypted data to decrypt.

        Returns:
            bytes: The decrypted data.
        """
        try:
            return private_key.decrypt(
                encrypted_data,
                asymmetric_padding.OAEP(
                    mgf=asymmetric_padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
        except Exception as e:
            logging.error(f"Error occurred while decrypting data with private key: {e}")

    def encrypt_with_public_key(public_key, plaintext: bytes) -> bytes:
        """
        Encrypt data using the public key.

        Args:
            public_key (RSAPublicKey): The public key to use for encryption.
            plaintext (bytes): The data to encrypt.

        Returns:
            bytes: The encrypted data.
        """
        try:
            return public_key.encrypt(
                plaintext,
                asymmetric_padding.OAEP(
                    mgf=asymmetric_padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
        except Exception as e:
            logging.error(f"Error occurred while encrypting data with public key: {e}")
