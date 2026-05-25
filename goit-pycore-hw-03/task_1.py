from datetime import datetime

def get_days_from_today(date):
    """
    Calculate the number of days between a given date (YYYY-MM-DD) and today.

    Parameters:
    date (str): Date in 'YYYY-MM-DD' format

    Returns:
    int: Number of days (positive if date is in the past,
         negative if in the future).
    """
    try:
        # 1. Convert string to datetime object
        given_date = datetime.strptime(date, '%Y-%m-%d').date()

        # 2. Get current date (without time)
        today = datetime.today().date()

        # 3. Calculate difference ---> subtracting dates results in a timedelta object
        delta = today - given_date

        # 4. Return number of days as integer
        return delta.days

    except ValueError:
        # Handle case when date format is incorrect
        return "Error: Invalid date format. Use 'YYYY-MM-DD'."
    except Exception as e:
        # Handle any other unexpected errors
        return f"An error occurred: {e}"

# Example usage:
print(get_days_from_today("2021-10-09"))
print(get_days_from_today("2026-04-01"))  # Past date relative to today (April 21, 2026)