import hashlib
import multiprocessing as mp
import json
from tqdm import tqdm

def generate_card_number(bin_code, last_four, middle):
    return f"{bin_code}{middle:06d}{last_four}"

def hash_card_number(card_number):
    return hashlib.sha256(card_number.encode()).hexdigest()

def find_card_number(hash_target, bin_code, last_four, middle_range):
    for middle in middle_range:
        card_number = generate_card_number(bin_code, last_four, middle)
        if hash_card_number(card_number) == hash_target:
            return card_number
    return None

def find_card_number_parallel(hash_target, bin_code, last_four, process_count):
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

def serialize_card_number(card_number, path):
    with open(path, 'w') as f:
        json.dump({"card_number": card_number}, f)

def get_cpu_count():
    return mp.cpu_count()