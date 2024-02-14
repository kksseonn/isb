import json

def encrypt_text(text: str, key: dict) -> str:
    """
    Encrypts the given text using the provided key.

    Args:
        text (str): The text to be encrypted.
        key (dict): The encryption key where keys are uppercase characters
                    and values are their corresponding encrypted forms.

    Returns:
        str: The encrypted text.
    """
    encrypted_text = ''
    for char in text:
        if char.upper() in key:
            encrypted_text += key[char.upper()]
        else:
            encrypted_text += char
    return encrypted_text

def decrypt_text(encrypted_text: str, key: dict) -> str:
    """
    Decrypts the given text using the provided key.

    Args:
        encrypted_text (str): The text to be decrypted.
        key (dict): The encryption key where values are encrypted characters
                    and keys are their corresponding decrypted forms.

    Returns:
        str: The decrypted text.
    """
    decrypted_text = ''
    reverse_key = {value: key for key, value in key.items()}
    for char in encrypted_text:
        if char in reverse_key:
            decrypted_text += reverse_key[char]
        else:
            decrypted_text += char
    return decrypted_text

if __name__ == "__main__":
    with open('lab_1/part_1/key_1.json', encoding='utf-8') as f:
        key = json.load(f)

    with open('lab_1/part_1/original_text.txt', 'r', encoding='utf-8') as f:
        original_text = f.read()

    encrypted_text = encrypt_text(original_text, key)

    with open('lab_1/part_1/encrypted_text.txt', 'w', encoding='utf-8') as f:
        f.write(encrypted_text)

    decrypted_text = decrypt_text(encrypted_text, key)

    with open('lab_1/part_1/decrypted_text.txt', 'w', encoding='utf-8') as f:
        f.write(decrypted_text)