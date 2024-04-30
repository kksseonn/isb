import logging


logging.basicConfig(level=logging.INFO)


def read_file(file_path: str) -> bytes:
    """
    Read binary data from the specified file.

    Args:
        file_path (str): The path to the file to be read.

    Returns:
        bytes: The binary data read from the file.
    """
    try:
        with open(file_path, 'rb') as file:
            return file.read()
    except Exception as e:
        logging.error(f"Error occurred while reading file '{file_path}': {e}")


def write_file(file_path: str, data: bytes) -> None:
    """
    Write binary data to the specified file.

    Args:
        file_path (str): The path to the file to be written.
        data (bytes): The binary data to be written to the file.

    Returns:
        None
    """
    try:
        with open(file_path, 'wb') as file:
            file.write(data)
        logging.info(f"Data written to file '{file_path}' successfully.")
    except Exception as e:
        logging.error(f"Error occurred while writing data to file '{file_path}': {e}")