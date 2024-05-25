import logging

def luhn_algorithm(card_number):
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
        logging.error(f"An error occurred while executing the Luhn algorithm: {ex}\n")
        return False

def check_card_validity(card_number):
    return luhn_algorithm(card_number)