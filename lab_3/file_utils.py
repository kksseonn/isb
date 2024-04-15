import logging

logging.basicConfig(level=logging.INFO)

def read_file(file_path):
    try:
        with open(file_path, 'rb') as file:
            return file.read()
    except Exception as e:
        logging.error(f"Error occurred while reading file '{file_path}': {e}") 

def write_file(file_path, data):
    try:
        with open(file_path, 'wb') as file:
            file.write(data)
        logging.info(f"Data written to file '{file_path}' successfully.")
    except Exception as e:
        logging.error(f"Error occurred while writing data to file '{file_path}': {e}")
