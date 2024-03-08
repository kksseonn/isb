import logging

logging.basicConfig(level=logging.INFO)


def read_from_file(file_path: str) -> str:
    """
    Read text data from the specified file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        logging.error(f"An error occurred while reading the file '{file_path}': {e}")
        return ''

def write_to_file(file_path: str, data: str) -> None:
    """
    Write data to the specified file.
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(data)
        logging.info(f"Data written to '{file_path}' successfully.")
    except Exception as e:
        logging.error(f"An error occurred while writing to the file '{file_path}': {e}")