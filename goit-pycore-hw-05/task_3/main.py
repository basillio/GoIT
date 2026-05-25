import sys
import os

def parse_log_line(line: str) -> dict:
    """Parse log line into dictionary."""
    parts = line.split(' ', 3)
    if len(parts) < 4:
        return {}  # Return empty dictionary for invalid lines
    return {
        'date': parts[0],
        'time': parts[1],
        'level': parts[2].upper(),
        'message': parts[3].strip()
    }

def load_logs(file_path: str) -> list:
    """Load logs from file, handling access errors."""
    logs = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                parsed = parse_log_line(line)
                if parsed:
                    logs.append(parsed)
    except FileNotFoundError:
        print(f"Error: File at path '{file_path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred while reading file: {e}")
        sys.exit(1)
    return logs

def filter_logs_by_level(logs: list, level: str) -> list:
    """Filter log list by level (case insensitive)."""
    return [log for log in logs if log['level'] == level.upper()]

def count_logs_by_level(logs: list) -> dict:
    """Count number of entries for each logging level."""
    counts = {}
    for log in logs:
        level = log['level']
        counts[level] = counts.get(level, 0) + 1
    return counts

def display_log_counts(counts: dict):
    """Display table with level statistics."""
    print(f"{'Logging Level':<17} | {'Count':<10}")
    print("-" * 18 + "|" + "-" * 11)
    # Sort for pretty output
    for level, count in sorted(counts.items()):
        print(f"{level:<17} | {count:<10}")

def main():
    # Check for at least one argument (file path)
    if len(sys.argv) < 2:
        print("Usage: python main.py <file_path> [logging_level]")
        return

    file_path = sys.argv[1]
    logs = load_logs(file_path)
    counts = count_logs_by_level(logs)

    # Display general statistics
    display_log_counts(counts)

    # If second argument is specified (logging level)
    if len(sys.argv) > 2:
        specific_level = sys.argv[2].upper()
        filtered = filter_logs_by_level(logs, specific_level)

        if filtered:
            print(f"\nLog details for level '{specific_level}':")
            for entry in filtered:
                print(f"{entry['date']} {entry['time']} - {entry['message']}")
        else:
            print(f"\nNo entries found for level '{specific_level}'.")

if __name__ == "__main__":
    main()