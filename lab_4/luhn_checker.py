import logging


logging.basicConfig(level=logging.INFO)


def luhn_algorithm(card_number: str) -> bool:
    """Check if the given card number passes the Luhn algorithm.

    Args:
        card_number (str): The card number to validate.

    Returns:
        bool: True if the card number is valid, False otherwise.
    """
    try:
        digits = [int(d) for d in card_number]
        checksum = digits.pop()
        digits.reverse()
        
        for i in range(len(digits)):
            if i % 2 == 0:
                digits[i] *= 2
                if digits[i] > 9:
                    digits[i] -= 9
        
        total_sum = sum(digits)
        check_digit = (total_sum * 9) % 10
        
        if check_digit == checksum:
            logging.info("The card data have passed the test for compliance with the Luhn algorithm.")
            return True
        else:
            logging.info("The card data didn't pass the test for compliance with the Luhn algorithm.")
            return False
    except Exception as ex:
        logging.error(f"An error occurred while executing the Luhn algorithm: {ex}")
        return False

def check_card_validity(card_number: str) -> bool:
    """Check the validity of a card number.

    Args:
        card_number (str): The card number to validate.

    Returns:
        bool: True if the card number is valid, False otherwise.
    """
    return luhn_algorithm(card_number)
