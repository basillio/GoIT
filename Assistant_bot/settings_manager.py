"""
Settings management module for Personal Assistant Bot
Handles loading, saving, and managing application settings
"""
import json
from pathlib import Path


class SettingsManager:
    """Manages application settings and configuration"""

    DEFAULT_SETTINGS = {
        "notifications": {
            "enabled": True,
            "days_in_advance": 7,
            "check_interval": "1h",
            "show_on_startup": True,
        },
        "ui": {
            "theme": "light",
            "tab_order": ["Contacts", "Notes", "Settings"],
            "auto_save_interval": 30,
        },
        "colors": {
            "default_palette": [
                "#FF6B6B",
                "#4ECDC4",
                "#45B7D1",
                "#FFA07A",
                "#98D8C8",
                "#F7DC6F",
                "#BB8FCE",
                "#85C1E2",
                "#F8B88B",
                "#A8E6CF",
            ]
        },
    }

    def __init__(self, config_file="config.json"):
        self.config_file = Path(config_file)
        self.settings = self._load_settings()

    def _load_settings(self):
        """Load settings from config file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    config = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    return self._merge_settings(self.DEFAULT_SETTINGS, config)
            except (json.JSONDecodeError, IOError):
                return self.DEFAULT_SETTINGS.copy()
        return self.DEFAULT_SETTINGS.copy()

    def _merge_settings(self, defaults, user_settings):
        """Merge user settings with defaults"""
        merged = defaults.copy()
        for key, value in user_settings.items():
            if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                merged[key] = self._merge_settings(merged[key], value)
            else:
                merged[key] = value
        return merged

    def _save_settings(self):
        """Save settings to config file"""
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=2)
            return True
        except IOError:
            return False

    def get(self, key, default=None):
        """Get a setting value by key (supports nested keys with dot notation)"""
        keys = key.split(".")
        value = self.settings
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        return value if value is not None else default

    def set(self, key, value):
        """Set a setting value by key (supports nested keys with dot notation)"""
        keys = key.split(".")
        settings = self.settings
        for k in keys[:-1]:
            if k not in settings:
                settings[k] = {}
            settings = settings[k]
        settings[keys[-1]] = value
        return self._save_settings()

    def get_notifications_settings(self):
        """Get all notification settings"""
        return self.get("notifications", {})

    def set_notifications_enabled(self, enabled):
        """Enable/disable notifications"""
        return self.set("notifications.enabled", enabled)

    def set_notification_days(self, days):
        """Set days in advance for birthday notifications"""
        return self.set("notifications.days_in_advance", days)

    def set_check_interval(self, interval):
        """Set check interval for notifications (1h, 6h, daily)"""
        return self.set("notifications.check_interval", interval)

    def get_ui_settings(self):
        """Get all UI settings"""
        return self.get("ui", {})

    def set_theme(self, theme):
        """Set UI theme (light or dark)"""
        return self.set("ui.theme", theme)

    def get_theme(self):
        """Get current UI theme"""
        return self.get("ui.theme", "light")

    def set_tab_order(self, tab_order):
        """Set the order of tabs"""
        return self.set("ui.tab_order", tab_order)

    def get_tab_order(self):
        """Get the current tab order"""
        return self.get("ui.tab_order", ["Contacts", "Notes", "Settings"])

    def set_auto_save_interval(self, interval):
        """Set auto-save interval in seconds"""
        return self.set("ui.auto_save_interval", interval)

    def get_auto_save_interval(self):
        """Get auto-save interval in seconds"""
        return self.get("ui.auto_save_interval", 30)

    def get_color_palette(self):
        """Get the default color palette"""
        return self.get("colors.default_palette", self.DEFAULT_SETTINGS["colors"]["default_palette"])

    def reset_to_defaults(self):
        """Reset all settings to defaults"""
        self.settings = self.DEFAULT_SETTINGS.copy()
        return self._save_settings()

    def validate_settings(self):
        """Validate that all required settings exist"""
        required_keys = [
            "notifications.enabled",
            "notifications.days_in_advance",
            "notifications.check_interval",
            "ui.theme",
            "ui.tab_order",
            "colors.default_palette",
        ]
        for key in required_keys:
            if self.get(key) is None:
                return False
        return True
