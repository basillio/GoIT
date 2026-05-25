## Personal Assistant Bot (Address Book) 📱

A professional console-based assistant bot designed to manage your contacts efficiently. Built with Python, this application allows you to store names, multiple phone numbers, and birthdays, while providing automated reminders for upcoming celebrations.

### Key Features

* 💾 **Contact Management:** Add new contacts or append multiple phone numbers to existing ones.
* 🎂 **Birthday Tracking:** Store birthdays and retrieve them with a single command.
* 📅 **Smart Reminders:** Automatically calculates congratulation dates for the next 7 days, seamlessly adjusting weekend birthdays to the following Monday.
* ✅ **Data Validation:** Built-in strict validation for phone numbers (exactly 10 digits) and dates (`DD.MM.YYYY`).
* 🧱 **Modular Architecture:** Clean code separation into `main.py`, `handlers.py`, and `models.py` for maximum maintainability.

---

### Available Commands

| Command | Description | Example |
| :--- | :--- | :--- |
| **hello** | Receive a friendly greeting from the bot | `hello` |
| **add** | Add a new contact or append a phone to an existing one | `add Hanna 0954656234` |
| **change** | Replace an old phone number with a new one | `change Hanna 0954656234 0991234567` |
| **phone** | Display all saved phone numbers for a contact | `phone Hanna` |
| **all** | Show all contacts currently stored in the address book | `all` |
| **add-birthday** | Set a birthday date for a specific contact | `add-birthday Hanna 10.05.1990` |
| **show-birthday** | View the birthday date of a specific contact | `show-birthday Hanna` |
| **birthdays** | Show upcoming birthdays for the next 7 days with congratulation dates | `birthdays` |
| **close** / **exit** | Securely terminate the application | `exit` |

---

### Project Structure

* **`main.py`**: The entry point of the application. Handles the main CLI interaction loop and command routing using structural pattern matching.
* **`handlers.py`**: Contains the command-line interface handlers, argument parsing, and the `@input_error` decorator for safe exception handling.
* **`models.py`**: Defines core data structures (`AddressBook`, `Record`, `Field`, `Name`, `Phone`, `Birthday`) and primary business logic.

---

### How to Install and Run

#### Prerequisites
* **Python 3.10 or higher** is required (due to the use of `match/case` statements).

#### Setup Instructions
1. Clone the repository or copy the project files to your local workspace.
2. Open your terminal (or PowerShell/Command Prompt on Windows).
3. Navigate to the project directory:
   bash
   cd goit-pycode-hw-07

Run the application:
   bash
   python main.py