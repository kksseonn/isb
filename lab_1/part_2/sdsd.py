import json
import logging
from collections import Counter

logging.basicConfig(level=logging.INFO)


def frequency_analysis(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            original_text = f.read()
    except Exception as e:
        logging.error(f"An error occurred while reading the input file: {e}")
        return
    character_count = Counter(original_text)
    total_characters = sum(character_count.values())
    character_frequency_percentage = {char: (
        count / total_characters * 100) for char, count in character_count.items()}
    sorted_character_frequency = dict(sorted(
        character_frequency_percentage.items(), key=lambda item: item[1], reverse=True))
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(sorted_character_frequency, f,
                      ensure_ascii=False, indent=4)
        logging.info(
            "Frequency analysis results (sorted by frequency and represented as percentages) written to JSON file successfully.")
    except Exception as e:
        logging.error(
            f"An error occurred while writing to the output file: {e}")


if __name__ == "__main__":
    try:
        input_file = 'lab_1/part_2/code6.txt'
        output_file = 'lab_1/part_2/frequency_analysis.json'
        frequency_analysis(input_file, output_file)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
