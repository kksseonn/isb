import argparse
import logging
import json

from hybrid_crypto_system import HybridCryptoSystem


logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":
    """
    Main function to generate keys, encrypt data, or decrypt data based on the mode specified in the options.
    """
    parser = argparse.ArgumentParser(description="Process options for Hybrid Crypto System")
    parser.add_argument("options_file", help="Path to the JSON options file")
    args = parser.parse_args()

    try:
        with open(args.options_file, "r") as options_file:
            options = json.load(options_file)
        
        mode = options['mode']
        match mode:
            case 'generation':
                HybridCryptoSystem.generate_keys(options['generation'])
            case 'encryption':
                HybridCryptoSystem.encrypt_data(options['encryption'])
            case 'decryption':
                HybridCryptoSystem.decrypt_data(options['decryption'])
            case _:
                raise ValueError(f"Invalid mode: {mode}")
    
    except Exception as e:
        logging.error(f"An error occurred: {e}")
