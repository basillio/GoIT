import re

def normalize_phone(phone_number):
    """
    Normalize phone number: keep only digits and '+',
    add '+38' code if missing.
    """
    # 1. Remove all characters except digits and '+'
    # [^\d+] means "everything that is NOT a digit (\d) and NOT a plus (+)"
    cleaned_number = re.sub(r'[^\d+]', '', phone_number.strip())

    # 2. Logic for adding +38 prefix
    if cleaned_number.startswith('+'):
        # If already starts with '+', check if it's a full code
        normalized = cleaned_number
    elif cleaned_number.startswith('380'):
        # If starts with 380, just add '+'
        normalized = '+' + cleaned_number
    else:
        # In all other cases (e.g., 050...) add '+38'
        normalized = '+38' + cleaned_number

    return normalized

# Verification according to our example:
raw_numbers = [
    "067\t123 4567",
    "(095) 234-5678\n",
    "+380 44 123 4567",
    "380501234567",
    "    +38(050)123-32-34",
    "     0503451234",
    "(050)8889900",
    "38050-111-22-22",
    "38050 111 22 11   ",
]

sanitized_numbers = [normalize_phone(num) for num in raw_numbers]
print("Normalized phone numbers for SMS distribution:")
print(sanitized_numbers)