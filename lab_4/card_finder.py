import hashlib
import multiprocessing as mp
import json
import logging

from tqdm import tqdm


logging.basicConfig(level=logging.INFO)


def generate_card_number(bin_code: str, last_four: str, middle: int) -> str:
    """Generate a card number based on BIN code, last four digits, and middle part.

    Args:
        bin_code (str): The BIN (Bank Identification Number) code.
        last_four (str): The last four digits of the card number.
        middle (int): The middle part of the card number.

    Returns:
        str: The generated card number.
    """
    return f"{bin_code}{middle:06d}{last_four}"


def hash_card_number(card_number: str) -> str:
    """Hash a card number using SHA-256 algorithm.

    Args:
        card_number (str): The card number to hash.

    Returns:
        str: The hashed card number.
    """
    return hashlib.sha256(card_number.encode()).hexdigest()


def find_card_number(hash_target: str, bin_code: str, last_four: str, middle_range: range) -> str:
    """Find a card number that matches the given hash target within the specified range of middle parts.

    Args:
        hash_target (str): The hash value to match.
        bin_code (str): The BIN (Bank Identification Number) code.
        last_four (str): The last four digits of the card number.
        middle_range (range): The range of middle parts to search within.

    Returns:
        str: The card number if found, otherwise None.
    """
    try:
        for middle in middle_range:
            card_number = generate_card_number(bin_code, last_four, middle)
            if hash_card_number(card_number) == hash_target:
                return card_number
        return None
    except Exception as e:
        logging.error(f"An error occurred while finding card number: {e}")
        return None


def find_card_number_parallel(hash_target: str, bin_code: str, last_four: str, process_count: int) -> str:
    """Find a card number in parallel using multiple processes.

    Args:
        hash_target (str): The hash value to match.
        bin_code (str): The BIN (Bank Identification Number) code.
        last_four (str): The last four digits of the card number.
        process_count (int): The number of processes to use for parallel execution.

    Returns:
        str: The card number if found, otherwise None.
    """
    try:
        pool = mp.Pool(process_count)
        chunk_size = 1000000 // process_count
        ranges = [(hash_target, bin_code, last_four, range(i * chunk_size, (i + 1) * chunk_size)) for i in range(process_count)]
        with tqdm(total=1000000, desc="Searching") as pbar:
            results = pool.starmap(find_card_number, ranges)
            for result in results:
                pbar.update(chunk_size)
                if result:
                    pool.terminate()
                    return result
        return None
    except Exception as e:
        logging.error(f"An error occurred while finding card number in parallel: {e}")
        return None


def serialize_card_number(card_number: str, path: str) -> None:
    """Serialize a card number to a JSON file.

    Args:
        card_number (str): The card number to serialize.
        path (str): The file path to save the serialized data.
    """
    try:
        with open(path, 'w') as f:
            json.dump({"card_number": card_number}, f)
    except Exception as e:
        logging.error(f"An error occurred while serializing card number: {e}")


def get_cpu_count() -> int:
    """Get the number of available CPU cores.

    Returns:
        int: The number of CPU cores.
    """
    try:
        return mp.cpu_count()
    except Exception as e:
        logging.error(f"An error occurred while getting CPU count: {e}")
