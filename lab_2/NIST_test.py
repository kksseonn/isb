import json
import logging
from collections import Counter
from math import erf, sqrt

logging.basicConfig(level=logging.INFO)


def frequency_bit_test(sequence):
    sequence = [1 if int(bit) == 1 else -1 for bit in sequence]
    counts = Counter(sequence)
    n_negatives = counts[-1]
    n_positives = counts[1]
    total_length = n_negatives + n_positives
    value = (n_positives - n_negatives) / sqrt(total_length)
    p_value = 0.5 * (1 + erf(abs(value) / sqrt(2)))
    return p_value


def consecutive_bits_test(sequence):
    sequence = [1 if int(bit) == 1 else -1 for bit in sequence]
    counts = Counter(sequence)
    ones_count = counts[1]
    n = len(sequence)
    dzeta = ones_count / n
    if abs(dzeta - 0.5) < (2 / sqrt(n)):
        v = 0
        for bit in range(len(sequence) - 1):
            if sequence[bit] != sequence[bit + 1]:
                v += 1
        numerator = abs(v - 2 * n * dzeta * (1 - dzeta))
        denominator = 2 * sqrt(2 * n) * dzeta * (1 - dzeta)
        p_value = erf(numerator / denominator)
    else:
        p_value = 0
    return p_value


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

    c_plus_plus_bit_test = frequency_bit_test(options['c++_sequence'])
    write_to_file(options['file_name'], f"C++ frequency_bit_test: {c_plus_plus_bit_test:.16f}")

    java_bit_test = frequency_bit_test(options['java_sequence'])
    write_to_file(options['file_name'], f"Java frequency_bit_test: {java_bit_test:.16f}")

    c_plus_plus_consecutive_test = consecutive_bits_test(
        options['c++_sequence'])
    write_to_file(options['file_name'], f"C++ consecutive bits test: {c_plus_plus_consecutive_test:.16f}")

    java_consecutive_test = consecutive_bits_test(options['java_sequence'])
    write_to_file(options['file_name'], f"Java consecutive bits test: {java_consecutive_test:.16f}")
