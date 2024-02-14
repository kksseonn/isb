import json

def encrypt_text(text, key):
    encrypted_text = ''
    for char in text:
        if char.upper() in key:
            encrypted_text += key[char.upper()]
        else:
            encrypted_text += char
    return encrypted_text

def decrypt_text(encrypted_text, key):
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