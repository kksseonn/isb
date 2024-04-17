import logging
import json
from cryptography_utils import generate_keys, encrypt_data, decrypt_data


logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":
    """
    Main script to generate keys, encrypt data, or decrypt data based on the mode specified in the options file.
    """
    try:
        with open("lab_3/options.json", "r") as options_file:
            options = json.load(options_file)
            
        mode = options['mode']
        
        match mode:
            case 'generation':
                generate_keys(options['generation'])
            case 'encryption':
                encrypt_data(options['encryption'])
            case 'decryption':
                decrypt_data(options['decryption'])
            case _:
                raise ValueError(f"Invalid mode: {mode}")
    
    except Exception as e:
        logging.error(f"An error occurred: {e}")