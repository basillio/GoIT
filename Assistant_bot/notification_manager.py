"""
Notification management module for Personal Assistant Bot
Handles birthday notifications and reminders
"""
from datetime import datetime, timedelta
from threading import Thread, Event
import time


class NotificationManager:
    """Manages birthday notifications and reminders"""

    def __init__(self, contact_book, settings_manager):
        self.contact_book = contact_book
        self.settings_manager = settings_manager
        self.notification_thread = None
        self.stop_event = Event()

    def get_upcoming_birthdays(self, days_in_advance=None):
        """Get contacts with birthdays in the next N days"""
        if days_in_advance is None:
            days_in_advance = self.settings_manager.get("notifications.days_in_advance", 7)

        today = datetime.now().date()
        target_date = today + timedelta(days=days_in_advance)
        upcoming = []

        for contact in self.contact_book.list_all_contacts():
            if contact.birthday:
                try:
                    birthday = datetime.strptime(contact.birthday, "%d.%m.%Y").date()
                    birthday_this_year = birthday.replace(year=today.year)

                    if birthday_this_year < today:
                        birthday_this_year = birthday_this_year.replace(year=today.year + 1)

                    days_until = (birthday_this_year - today).days
                    if 0 <= days_until <= days_in_advance:
                        age = today.year - birthday.year
                        upcoming.append({
                            "name": contact.name,
                            "birthday": contact.birthday,
                            "days_until": days_until,
                            "age": age,
                        })
                except ValueError:
                    pass

        return sorted(upcoming, key=lambda x: x["days_until"])

    def format_notification_message(self, upcoming_birthdays):
        """Format upcoming birthdays into a readable message"""
        if not upcoming_birthdays:
            return "No upcoming birthdays"

        message = "Upcoming Birthdays:\n\n"
        for birthday_info in upcoming_birthdays:
            name = birthday_info["name"]
            days = birthday_info["days_until"]
            age = birthday_info["age"]

            if days == 0:
                when = "Today"
            elif days == 1:
                when = "Tomorrow"
            else:
                when = f"In {days} days"

            message += f"• {name} - {when} (turns {age})\n"

        return message

    def check_birthdays(self):
        """Check for upcoming birthdays and return notification data"""
        if not self.settings_manager.get("notifications.enabled", True):
            return None

        upcoming = self.get_upcoming_birthdays()
        if upcoming:
            return {
                "title": "Birthday Reminders",
                "message": self.format_notification_message(upcoming),
                "birthdays": upcoming,
            }
        return None

    def start_periodic_check(self, callback=None):
        """Start periodic birthday checks in a background thread"""
        if self.notification_thread and self.notification_thread.is_alive():
            return

        self.stop_event.clear()
        self.notification_thread = Thread(
            target=self._periodic_check_loop,
            args=(callback,),
            daemon=True
        )
        self.notification_thread.start()

    def _periodic_check_loop(self, callback=None):
        """Background loop for periodic birthday checks"""
        interval_str = self.settings_manager.get("notifications.check_interval", "1h")
        interval_seconds = self._parse_interval(interval_str)

        while not self.stop_event.is_set():
            try:
                notification = self.check_birthdays()
                if notification and callback:
                    callback(notification)
            except Exception:
                pass

            # Sleep in small increments to allow quick shutdown
            for _ in range(int(interval_seconds)):
                if self.stop_event.is_set():
                    break
                time.sleep(1)

    def stop_periodic_check(self):
        """Stop the periodic birthday check thread"""
        self.stop_event.set()
        if self.notification_thread:
            self.notification_thread.join(timeout=5)

    def _parse_interval(self, interval_str):
        """Parse interval string to seconds"""
        if interval_str == "1h":
            return 3600
        elif interval_str == "6h":
            return 21600
        elif interval_str == "daily":
            return 86400
        else:
            return 3600  # Default to 1 hour

    def get_today_birthdays(self):
        """Get contacts with birthdays today"""
        today = datetime.now().date()
        today_birthdays = []

        for contact in self.contact_book.list_all_contacts():
            if contact.birthday:
                try:
                    birthday = datetime.strptime(contact.birthday, "%d.%m.%Y").date()
                    birthday_this_year = birthday.replace(year=today.year)

                    if birthday_this_year == today:
                        age = today.year - birthday.year
                        today_birthdays.append({
                            "name": contact.name,
                            "birthday": contact.birthday,
                            "age": age,
                        })
                except ValueError:
                    pass

        return today_birthdays

    def get_tomorrow_birthdays(self):
        """Get contacts with birthdays tomorrow"""
        tomorrow = datetime.now().date() + timedelta(days=1)
        tomorrow_birthdays = []

        for contact in self.contact_book.list_all_contacts():
            if contact.birthday:
                try:
                    birthday = datetime.strptime(contact.birthday, "%d.%m.%Y").date()
                    birthday_this_year = birthday.replace(year=tomorrow.year)

                    if birthday_this_year == tomorrow:
                        age = tomorrow.year - birthday.year
                        tomorrow_birthdays.append({
                            "name": contact.name,
                            "birthday": contact.birthday,
                            "age": age,
                        })
                except ValueError:
                    pass

        return tomorrow_birthdays
