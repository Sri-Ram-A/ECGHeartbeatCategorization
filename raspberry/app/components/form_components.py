import customtkinter as ctk
from components.colors import get_colors

# --- Backward Compatibility & Default Theme ---
# These are used for convenience; they default to light theme
_colors = get_colors(is_dark_mode=False)
PRIMARY_COLOR = _colors["primary"]
ACCENT_COLOR = _colors["accent"]
TEXT_COLOR = _colors["text_primary"]
SECONDARY_TEXT_COLOR = _colors["text_secondary"]
BG_COLOR = _colors["background"]
CARD_BG_COLOR = _colors["card_background"]
ERROR_COLOR = _colors["error"]

# --- Font Sizes (centralized for consistency) ---
FONT_TITLE = 28
FONT_SUBTITLE = 16
FONT_ENTRY = 15
FONT_BUTTON = 16
FONT_INFO = 15
FONT_SMALL = 12


def create_title_label(parent, text, colors=None):
    """Create a consistent title label."""
    if colors is None:
        colors = get_colors(False)
    return ctk.CTkLabel(parent, text=text,font=ctk.CTkFont(size=FONT_TITLE, weight="bold"),text_color=colors["text_primary"])


def create_subtitle_label(parent, text, colors=None):
    """Create a consistent subtitle/description label."""
    if colors is None:
        colors = get_colors(False)
    return ctk.CTkLabel(parent, text=text,font=ctk.CTkFont(size=FONT_SUBTITLE),text_color=colors["text_secondary"])


def create_label_entry(parent, text, placeholder, entry_var=None, show_char=None, colors=None):
    """
    Creates a labeled entry field (Frame, Label, Entry).
    
    Args:
        parent: Parent frame
        text: Label text
        placeholder: Placeholder text for entry
        entry_var: Optional tk.StringVar for binding
        show_char: Optional character to show (for passwords)
        colors: Optional color dict, defaults to light theme
        
    Returns:
        tuple: (frame, entry) for accessing the entry widget
    """
    if colors is None:
        colors = get_colors(False)
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    frame.pack(fill="x", pady=(0, 20))
    ctk.CTkLabel(frame, text=text,font=ctk.CTkFont(size=FONT_INFO, weight="bold"),text_color=colors["text_primary"]).pack(anchor="w", pady=(0, 8))
    entry = ctk.CTkEntry(frame, width=380, height=45,
                placeholder_text=placeholder,textvariable=entry_var,
                font=ctk.CTkFont(size=FONT_ENTRY),
                border_width=1,border_color=colors["input_border"],
                corner_radius=8,
                show=show_char
            )
    entry.pack(fill="x")
    return frame, entry


def create_main_button(parent, text, command, colors=None, width=380):
    """
    Creates the primary action button.
    
    Args:
        parent: Parent frame
        text: Button text
        command: Command to execute on click
        colors: Optional color dict, defaults to light theme
        width: Button width (default 380)
        
    Returns:
        CTkButton: The button widget
    """
    if colors is None:
        colors = get_colors(False)
    
    return ctk.CTkButton(parent, text=text,
                         width=width, height=48,
                         font=ctk.CTkFont(size=FONT_BUTTON, weight="bold"),
                         fg_color=colors["primary"],
                         hover_color=colors["primary_hover"],
                         corner_radius=8,
                         command=command)


def create_accent_button(parent, text, command, colors=None, width=380):
    """
    Creates an accent (green) action button.
    
    Args:
        parent: Parent frame
        text: Button text
        command: Command to execute on click
        colors: Optional color dict, defaults to light theme
        width: Button width (default 380)
        
    Returns:
        CTkButton: The button widget
    """
    if colors is None:
        colors = get_colors(False)
    
    return ctk.CTkButton(parent, text=text,
                         width=width, height=48,
                         font=ctk.CTkFont(size=FONT_BUTTON, weight="bold"),
                         fg_color=colors["accent"],
                         hover_color=colors["accent_hover"],
                         corner_radius=8,
                         command=command)


def create_link_button(parent, text, command, colors=None):
    """
    Creates a link-style button for navigation.
    
    Args:
        parent: Parent frame
        text: Button text
        command: Command to execute on click
        colors: Optional color dict, defaults to light theme
        
    Returns:
        CTkButton: The button widget
    """
    if colors is None:
        colors = get_colors(False)
    
    return ctk.CTkButton(parent, text=text,
                         font=ctk.CTkFont(size=FONT_INFO, weight="bold", underline=True),
                         text_color=colors["primary"],
                         fg_color="transparent",
                         hover_color=colors["background"],
                         command=command)


def create_card(parent, title, colors=None):
    """
    Creates a styled card frame.
    
    Args:
        parent: Parent frame
        title: Card title
        colors: Optional color dict, defaults to light theme
        
    Returns:
        CTkFrame: The card frame ready for content
    """
    if colors is None:
        colors = get_colors(False)
    
    card = ctk.CTkFrame(parent, fg_color=colors["card_background"], 
                        corner_radius=12, border_width=1, border_color=colors["border"])
    card.pack(fill="x", pady=(0, 20))
    
    # Title
    ctk.CTkLabel(card, text=title, 
                 font=ctk.CTkFont(size=FONT_SUBTITLE, weight="bold"),
                 text_color=colors["primary"]).pack(anchor="w", padx=20, pady=(15, 10))
    
    # Divider
    ctk.CTkFrame(card, height=1, fg_color=colors["border"]).pack(fill="x", padx=10, pady=(0, 10))
    
    # Content frame
    content = ctk.CTkFrame(card, fg_color="transparent")
    content.pack(fill="both", expand=True, padx=20, pady=(0, 15))
    
    return card, content


def create_info_row(parent, label, value, colors=None):
    """
    Creates an info display row (label: value).
    
    Args:
        parent: Parent frame
        label: Label text
        value: Value text
        colors: Optional color dict, defaults to light theme
    """
    if colors is None:
        colors = get_colors(False)
    
    row = ctk.CTkFrame(parent, fg_color="transparent")
    row.pack(fill="x", pady=5)
    
    ctk.CTkLabel(row, text=label, text_color=colors["text_secondary"],
                 font=ctk.CTkFont(size=FONT_INFO)).pack(side="left")
    ctk.CTkLabel(row, text=value, 
                 font=ctk.CTkFont(size=FONT_INFO, weight="bold"),
                 text_color=colors["text_primary"]).pack(side="right")


class ErrorLabel(ctk.CTkLabel):
    """
    Dedicated label for displaying error messages with appropriate styling.
    
    Usage:
        error_label = ErrorLabel(parent)
        error_label.set_error("Something went wrong!")
        error_label.clear()  # Clear the error
    """
    def __init__(self, parent, colors=None):
        if colors is None:
            colors = get_colors(False)
        self.colors = colors
        
        super().__init__(parent, text="",
                 text_color=colors["error"],
                 font=ctk.CTkFont(size=FONT_SMALL))
        self.pack(pady=(0, 15))

    def set_error(self, message):
        """Display an error message."""
        self.configure(text=f"⚠ {message}")

    def clear(self):
        """Clear the error message."""
        self.configure(text="")


class StatusLabel(ctk.CTkLabel):
    """
    Dedicated label for displaying success/status messages.
    
    Usage:
        status_label = StatusLabel(parent)
        status_label.set_success("Operation completed!")
        status_label.clear()  # Clear the message
    """
    def __init__(self, parent, colors=None):
        if colors is None:
            colors = get_colors(False)
        self.colors = colors
        
        super().__init__(parent, text="",
                 text_color=colors["accent"],
                 font=ctk.CTkFont(size=FONT_INFO, weight="bold"))
        self.pack(pady=(0, 15))

    def set_success(self, message):
        """Display a success message."""
        self.configure(text=f"✔ {message}")

    def clear(self):
        """Clear the status message."""
        self.configure(text="")