from datetime import datetime, timedelta

def get_upcoming_birthdays(users):
    # Get current date (without time)
    today = datetime.today().date()

    upcoming_birthdays = []

    for user in users:
        # Convert birthday string to date object
        # Since input format is 'year.month.day', use "%Y.%m.%d"
        birthday = datetime.strptime(user["birthday"], "%Y.%m.%d").date()

        # Determine birthday in current year
        birthday_this_year = birthday.replace(year=today.year)

        # If birthday already passed this year, move to next year
        if birthday_this_year < today:
            birthday_this_year = birthday_this_year.replace(year=today.year + 1)

        # Calculate difference in days between today and birthday
        days_until_birthday = (birthday_this_year - today).days

        # Check if birthday is within next 7 days (including today)
        if 0 <= days_until_birthday <= 7:
            congratulation_date = birthday_this_year

            # Check if date falls on weekend
            # weekday() returns 0 for Monday, 5 for Saturday, 6 for Sunday
            day_of_week = congratulation_date.weekday()

            if day_of_week == 5:  # Saturday
                # Move 2 days forward (Monday)
                congratulation_date += timedelta(days=2)
            elif day_of_week == 6:  # Sunday
                # Move 1 day forward (Monday)
                congratulation_date += timedelta(days=1)

            # Add data to list in required string format
            upcoming_birthdays.append({
                "name": user["name"],
                "congratulation_date": congratulation_date.strftime("%Y.%m.%d")
            })

    return upcoming_birthdays

# Example usage:
users = [
    {"name": "Kurulo Khamov", "birthday": "1985.04.23"}, # For example, if today is 04.21
    {"name": "Natali Shulyak", "birthday": "1990.04.24"},
    {"name": "Oleh Andrus", "birthday": "1992.04.26"},  # Falls on Sunday
    {"name": "Svitlana Shevchenko", "birthday": "1977.05.07"}
]

print("List of congratulations this week:", get_upcoming_birthdays(users))