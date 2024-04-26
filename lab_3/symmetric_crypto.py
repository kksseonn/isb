import os
import logging
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class SymmetricCrypto:
    """
    Class providing methods for symmetric cryptography operations.
    """

    def encrypt(symmetric_key: bytes, plaintext: bytes) -> tuple:
        """
        Encrypt the plaintext using symmetric key.

        Args:
            symmetric_key (bytes): The symmetric key to use for encryption.
            plaintext (bytes): The plaintext to encrypt.

        Returns:
            tuple: A tuple containing the initialization vector (IV) and the ciphertext.
        """
        try:
            iv = os.urandom(16)
            cipher = Cipher(algorithms.SM4(symmetric_key), modes.CBC(iv))
            encryptor = cipher.encryptor()
            padder = padding.PKCS7(128).padder()
            padded_plaintext = padder.update(plaintext) + padder.finalize()
            ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
            return iv, ciphertext
        except Exception as e:
            logging.error(f"Error occurred while encrypting data: {e}")

    def decrypt(symmetric_key: bytes, iv: bytes, ciphertext: bytes) -> bytes:
        """
        Decrypt the ciphertext using symmetric key and initialization vector.

        Args:
            symmetric_key (bytes): The symmetric key to use for decryption.
            iv (bytes): The initialization vector (IV) used in encryption.
            ciphertext (bytes): The ciphertext to decrypt.

        Returns:
            bytes: The decrypted plaintext.
        """
        try:
            cipher = Cipher(algorithms.SM4(symmetric_key), modes.CBC(iv))
            decryptor = cipher.decryptor()
            unpadder = padding.PKCS7(128).unpadder()
            plaintext = decryptor.update(ciphertext) + decryptor.finalize()
            plaintext = unpadder.update(plaintext) + unpadder.finalize()
            return plaintext
        except Exception as e:
            logging.error(f"Error occurred while decrypting data: {e}")
