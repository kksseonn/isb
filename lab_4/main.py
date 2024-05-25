import argparse
import json

from card_finder import find_card_number_parallel, get_cpu_count, serialize_card_number
from luhn_checker import check_card_validity


def load_options(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def main():
    parser = argparse.ArgumentParser(description='Card hash collision finder and validator.')
    parser.add_argument('mode', choices=['find', 'check'], help='Mode of operation')
    parser.add_argument('--options', type=str, help='Path to the options JSON file', required=True)
    
    args = parser.parse_args()
    options = load_options(args.options)
    
    if args.mode == 'find':
        for bin_code in options['bins']:
            card_number = find_card_number_parallel(options['hash'], bin_code, options['last_numbers'], get_cpu_count())
            if card_number:
                serialize_card_number(card_number, options['data_path'])
                print(f"Found card number: {card_number}")
                break
        else:
            print("Card number not found.")

    elif args.mode == 'check':
        if check_card_validity(options['card_number']):
            print("Card number is valid.")
        else:
            print("Card number is invalid.")

if __name__ == "__main__":
    main()