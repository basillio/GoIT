import random

def get_numbers_ticket(min_val, max_val, quantity):
    """
    Generate a set of unique sorted random numbers for lottery.

    Parameters:
    min_val (int): Minimum number (>= 1)
    max_val (int): Maximum number (<= 1000)
    quantity (int): Number of values to select

    Returns:
    list: Sorted list of unique numbers or empty list for invalid data.
    """

    # 1. Validate input data according to requirements
    if not (1 <= min_val <= quantity <= max_val <= 1000):
        return []

    # 2. Generate unique numbers
    # range(min_val, max_val + 1) creates a range of numbers from min to max inclusive
    # random.sample guarantees uniqueness and selects the required number of elements
    try:
        numbers = random.sample(range(min_val, max_val + 1), quantity)

        # 3. Return sorted list
        return sorted(numbers)

    except ValueError:
        # Additional protection in case validation logic is violated
        return []

# Example usage:
lottery_numbers = get_numbers_ticket(1, 49, 6)
print("Your lottery numbers:", lottery_numbers)

# Check for invalid data:
print("Invalid data (empty):", get_numbers_ticket(10, 5, 6))