import json
from cryptography_utils import generate_keys

if __name__ == "__main__":
    with open("lab_3/options.json", "r") as options_file:
            options = json.load(options_file)
            
    mode = options['mode']
    
    if mode == 'generation':
        generate_keys(options['generation'])