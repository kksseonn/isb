import time
import multiprocessing as mp
import logging

from tqdm import tqdm
from card_finder import find_card_number_parallel, hash_card_number, generate_card_number


logging.basicConfig(level=logging.INFO)


def measure_time(hash_target: str, bin_code: str, last_four: str, process_count: int) -> float:
    """Measure the time taken to find a card number collision using parallel processing.

    Args:
        hash_target (str): The hash value to match.
        bin_code (str): The BIN (Bank Identification Number) code.
        last_four (str): The last four digits of the card number.
        process_count (int): The number of processes to use for parallel execution.

    Returns:
        float: The elapsed time in seconds.
    """
    try:
        start_time = time.time()
        find_card_number_parallel(hash_target, bin_code, last_four, process_count)
        end_time = time.time()
        return end_time - start_time
    except Exception as e:
        logging.error(f"An error occurred while measuring time: {e}")
        return None


def measure_time_for_various_processes(hash_target: str, bin_code: str, last_four: str, max_processes: int) -> tuple:
    """Measure the time taken for various process counts.

    Args:
        hash_target (str): The hash value to match.
        bin_code (str): The BIN (Bank Identification Number) code.
        last_four (str): The last four digits of the card number.
        max_processes (int): The maximum number of processes to test.

    Returns:
        tuple: A tuple containing lists of process counts and corresponding time measurements.
    """
    try:
        process_counts = list(range(1, max_processes + 1))
        time_measurements = []

        for process_count in tqdm(process_counts, desc="Measuring time for various processes"):
            elapsed_time = measure_time(hash_target, bin_code, last_four, process_count)
            time_measurements.append(elapsed_time)

        return process_counts, time_measurements
    except Exception as e:
        logging.error(f"An error occurred while measuring time for various processes: {e}")
        return None, None


def time_measurement(bins: tuple, hash: str, last_numbers: str) -> tuple:
    """Measure time taken for card number collisions using multiprocessing.

    Args:
        bins (tuple): A tuple with the intended BIN.
        hash (str): Hash value.
        last_numbers (str): The last 4 digits of the number.

    Returns:
        tuple: A tuple containing lists of process counts and corresponding time measurements.
    """
    try:
        args = []
        for i in range(0, 1000000):
            args.append((i, bins, hash, last_numbers))

        times_list = []
        for i in tqdm(range(1, int(mp.cpu_count() * 1.5) + 1), desc="Processes"):
            start = time.time()
            with mp.Pool(processes=i) as p:
                for result in p.starmap(check_hash, args):
                    if result:
                        end = time.time() - start
                        times_list.append(end)
                        p.terminate()
                        break
                else:
                    end = time.time() - start
                    times_list.append(end)
        return range(len(times_list)), times_list
    except Exception as e:
        logging.error(f"An error occurred while measuring time: {e}")
        return None, None


def check_hash(middle: int, bins: tuple, hash: str, last_numbers: str) -> str:
    """Check for a hash collision for a given middle part.

    Args:
        middle (int): The middle part of the card number.
        bins (tuple): A tuple with the intended BIN.
        hash (str): Hash value.
        last_numbers (str): The last 4 digits of the number.

    Returns:
        str: The card number if found, otherwise None.
    """
    for bin_code in bins:
        card_number = generate_card_number(bin_code, last_numbers, middle)
        if hash_card_number(card_number) == hash:
            return card_number
    return None