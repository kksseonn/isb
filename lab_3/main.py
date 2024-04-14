import json
from cryptography_utils import generate_keys, encrypt_data, decrypt_data

if __name__ == "__main__":
    with open("lab_3/options.json", "r") as options_file:
            options = json.load(options_file)
            
    mode = options['mode']
    
    if mode == 'generation':
        generate_keys(options['generation'])
    elif mode == 'encryption':
        encrypt_data(options['encryption'])
    elif mode == 'decryption':
        decrypt_data(options['decryption'])