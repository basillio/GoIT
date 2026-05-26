"""
Color management module for Personal Assistant Bot
Handles color assignments and operations for contacts and notes
"""


class ColorManager:
    """Manages color assignments for contacts and notes"""

    DEFAULT_PALETTE = [
        "#FF6B6B",  # Red
        "#4ECDC4",  # Teal
        "#45B7D1",  # Blue
        "#FFA07A",  # Light Salmon
        "#98D8C8",  # Mint
        "#F7DC6F",  # Yellow
        "#BB8FCE",  # Purple
        "#85C1E2",  # Light Blue
        "#F8B88B",  # Peach
        "#A8E6CF",  # Light Green
    ]

    def __init__(self):
        self.palette = self.DEFAULT_PALETTE.copy()

    def get_palette(self):
        """Get the default color palette"""
        return self.palette.copy()

    def is_valid_color(self, color):
        """Validate if a color is in valid hex format"""
        if not color:
            return True
        if not isinstance(color, str):
            return False
        if not color.startswith("#"):
            return False
        if len(color) != 7:
            return False
        try:
            int(color[1:], 16)
            return True
        except ValueError:
            return False

    def get_color_by_index(self, index):
        """Get color from palette by index"""
        if 0 <= index < len(self.palette):
            return self.palette[index]
        return None

    def get_random_color(self):
        """Get a random color from the palette"""
        import random
        return random.choice(self.palette)

    def rgb_to_hex(self, r, g, b):
        """Convert RGB values to hex color"""
        return f"#{r:02x}{g:02x}{b:02x}"

    def hex_to_rgb(self, hex_color):
        """Convert hex color to RGB tuple"""
        if not self.is_valid_color(hex_color):
            return None
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def lighten_color(self, hex_color, factor=0.2):
        """Lighten a color by a given factor (0-1)"""
        rgb = self.hex_to_rgb(hex_color)
        if not rgb:
            return hex_color
        r, g, b = rgb
        r = min(255, int(r + (255 - r) * factor))
        g = min(255, int(g + (255 - g) * factor))
        b = min(255, int(b + (255 - b) * factor))
        return self.rgb_to_hex(r, g, b)

    def darken_color(self, hex_color, factor=0.2):
        """Darken a color by a given factor (0-1)"""
        rgb = self.hex_to_rgb(hex_color)
        if not rgb:
            return hex_color
        r, g, b = rgb
        r = max(0, int(r * (1 - factor)))
        g = max(0, int(g * (1 - factor)))
        b = max(0, int(b * (1 - factor)))
        return self.rgb_to_hex(r, g, b)

    def get_contrasting_text_color(self, hex_color):
        """Get contrasting text color (black or white) for a background color"""
        rgb = self.hex_to_rgb(hex_color)
        if not rgb:
            return "#000000"
        r, g, b = rgb
        # Calculate luminance
        luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
        # Return black for light backgrounds, white for dark backgrounds
        return "#000000" if luminance > 0.5 else "#FFFFFF"
