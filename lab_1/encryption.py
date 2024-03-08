import json
import logging
from read_and_write import read_from_file, write_to_file

logging.basicConfig(level=logging.INFO)


def encrypt_text(text_path: str, key_path: str) -> str:
    """
    Encrypts the given text using the provided key.

    Args:
        text (str): The path to the text to be encrypted.
        key_path (str): The path to the encryption key where keys are uppercase characters
                    and values are their corresponding encrypted forms.

    Returns:
        str: The encrypted text.
    """
    encrypted_text = ''
    try:
        with open(text_path, 'r', encoding='utf-8') as f:
            text = f.read()
        with open(key_path, encoding='utf-8') as f:
            key = json.load(f)
        for char in text:
            if char.upper() in key:
                encrypted_text += key[char.upper()]
            else:
                encrypted_text += char
    except Exception as e:
        logging.error(f"Error occurred during encryption: {e}")
    return encrypted_text


def decrypt_text(encrypted_text: str, key_path: str) -> str:
    """
    Decrypts the given text using the provided key.

    Args:
        encrypted_text (str): The path to the text to be decrypted.
        key_path (str): The path to the encryption key where values are encrypted characters
                    and keys are their corresponding decrypted forms.

    Returns:
        str: The decrypted text.
    """
    decrypted_text = ''
    try:
        with open(encrypted_text, 'r', encoding='utf-8') as f:
            text = f.read()
        with open(key_path, encoding='utf-8') as f:
            key = json.load(f)
        reverse_key = {value: key for key, value in key.items()}
        for char in text:
            if char in reverse_key:
                decrypted_text += reverse_key[char]
            else:
                decrypted_text += char
    except Exception as e:
        logging.error(f"Error occurred during decryption: {e}")
    return decrypted_text


if __name__ == "__main__":
    try:
        with open("lab_1/options.json", "r") as options_file:
            options = json.load(options_file)
        encrypted_text = encrypt_text(options['original_text'], options['key'])

        with open(options['encrypted_text'], 'w', encoding='utf-8') as f:
            f.write(encrypted_text)

        decrypted_text = decrypt_text(
            options['encrypted_text'], options['key'])

        with open(options['decrypted_text'], 'w', encoding='utf-8') as f:
            f.write(decrypted_text)
    except Exception as e:
        logging.error(f"An error occurred: {e}")