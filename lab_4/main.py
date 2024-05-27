import argparse
import json
import logging

from card_finder import find_card_number_parallel, get_cpu_count, serialize_card_number
from luhn_checker import check_card_validity
from time_measure import time_measurement
from visualize import visualize_time_measurements


logging.basicConfig(level=logging.INFO)


def load_options(file_path: str) -> dict:
    """Load options from a JSON file.

    Args:
        file_path (str): The path to the JSON options file.

    Returns:
        dict: The loaded options.
    """
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error(f"Options file {file_path} not found.")
        raise
    except json.JSONDecodeError:
        logging.error(f"Error decoding JSON from file {file_path}.")
        raise


def main() -> None:
    """Main function to execute the card hash collision finder and validator."""
    
    parser = argparse.ArgumentParser(description='Card hash collision finder and validator.')
    parser.add_argument('mode', choices=['find', 'check', 'measure'], help='Mode of operation')
    parser.add_argument('--options', type=str, help='Path to the options JSON file', required=True)
    
    args = parser.parse_args()
    
    try:
        options = load_options(args.options)
    except Exception as e:
        logging.error(f"Failed to load options: {e}")
        return

    match args.mode:
        case 'find':
            try:
                for bin_code in options['bins']:
                    card_number = find_card_number_parallel(options['hash'], bin_code, options['last_numbers'], get_cpu_count())
                    if card_number:
                        serialize_card_number(card_number, options['data_path'])
                        logging.info(f"Found card number: {card_number}")
                        break
                else:
                    logging.info("Card number not found.")
            except Exception as e:
                logging.error(f"An error occurred in 'find' mode: {e}")

        case 'check':
            try:
                card_number = options.get('card_number')
                if not card_number:
                    logging.error("No card number provided in options for 'check' mode.")
                    return

                if check_card_validity(card_number):
                    logging.info("Card number is valid.")
                else:
                    logging.info("Card number is invalid.")
            except Exception as e:
                logging.error(f"An error occurred in 'check' mode: {e}")

        case 'measure':
            try:
                process_counts, time_measurements = time_measurement(tuple(options['bins']), options['hash'], options['last_numbers'])
                visualize_time_measurements(process_counts, time_measurements)
            except Exception as e:
                logging.error(f"An error occurred in 'measure' mode: {e}")

if __name__ == "__main__":
    main()
