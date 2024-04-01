import json
from collections import Counter
import logging

logging.basicConfig(level=logging.INFO)

def frequency_bit_test(sequence):
    sequence = [int(bit) for bit in sequence]
    
    counts = Counter(sequence)
    
    n_zeros = counts[0]
    n_ones = counts[1]
    total_bits = n_zeros + n_ones
    
    expected_ones = total_bits / 2
    expected_zeros = total_bits / 2
    
    chi_square = ((n_zeros - expected_zeros) ** 2) / expected_zeros + ((n_ones - expected_ones) ** 2) / expected_ones
    
    return chi_square

def write_to_file(file_path: str, data: str) -> None:
    """
    Write data to the specified file.
    """
    try:
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(data + '\n')
        logging.info(f"Data written to '{file_path}' successfully.")
    except Exception as e:
        logging.error(
            f"An error occurred while writing to the file '{file_path}': {e}")

if __name__ == "__main__":
    
    with open("lab_2/options.json", "r") as options_file:
        options = json.load(options_file)
    
    c_plus_plus_chi_square = frequency_bit_test(options['c++_sequence'])
    write_to_file(options['file_name'], f"C++ sequence: {c_plus_plus_chi_square:.16f}")
    
    java_chi_square = frequency_bit_test(options['java_sequence'])
    write_to_file(options['file_name'], f"Java sequence: {java_chi_square:.16f}")