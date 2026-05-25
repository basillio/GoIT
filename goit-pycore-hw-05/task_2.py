import re
from typing import Callable, Generator

def generator_numbers(text: str) -> Generator[float, None, None]:

    # Regular expression to find real numbers surrounded by spaces.
    # \d+\.\d+ — finds numbers with decimal point
    # \d+ — finds integers
    pattern = r'\b\d+(?:\.\d+)?\b'

    for match in re.finditer(pattern, text):
        # yield returns value and preserves function state
        yield float(match.group())

def sum_profit(text: str, func: Callable[[str], Generator[float, None, None]]) -> float:

    total_sum = 0
    # Iterate over generator returned by generator_numbers function
    for number in func(text):
        total_sum += number
    return total_sum

# Example usage:
text = ("The employee's total income consists of several parts: "
        "1000.01 as base income, supplemented by additional income "
        "27.45 and 324.00 dollars.")

total_income = sum_profit(text, generator_numbers)
print(f"Total income: {total_income}")