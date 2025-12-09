"""
Color Theme Configuration for MediMonitor Application
Supports both Light and Dark modes with professional blue/green color scheme
"""

# Light Theme Colors
LIGHT_THEME = {
    "primary": "#1E88E5",        # Professional blue
    "primary_hover": "#1565C0",  # Darker blue for hover
    "accent": "#43A047",         # Professional green
    "accent_hover": "#388E3C",   # Darker green for hover
    "error": "#D32F2F",          # Professional red
    "error_hover": "#c62828",    # Darker red for hover
    "text_primary": "#333333",   # Dark text
    "text_secondary": "#666666", # Gray text
    "background": "#f5f5f5",     # Light gray background
    "card_background": "white",  # White cards
    "border": "#e0e0e0",         # Light border
    "status_bg": "#e0e0e0",      # Status bar background
    "input_border": "#bdbdbd",   # Input border
}

# Dark Theme Colors
DARK_THEME = {
    "primary": "#42A5F5",        # Lighter blue for dark mode
    "primary_hover": "#1E88E5",  # Original blue
    "accent": "#66BB6A",         # Lighter green for dark mode
    "accent_hover": "#43A047",   # Original green
    "error": "#EF5350",          # Lighter red for dark mode
    "error_hover": "#D32F2F",    # Original red
    "text_primary": "#FFFFFF",   # White text
    "text_secondary": "#B0B0B0", # Light gray text
    "background": "#1E1E1E",     # Dark background
    "card_background": "#2D2D2D", # Dark gray cards
    "border": "#3F3F3F",         # Dark border
    "status_bg": "#3F3F3F",      # Status bar background
    "input_border": "#4F4F4F",   # Input border
}

# Get color by theme
def get_colors(is_dark_mode: bool) -> dict:
    """
    Returns the appropriate color palette based on theme mode.
    
    Args:
        is_dark_mode (bool): True for dark theme, False for light theme
        
    Returns:
        dict: Color dictionary with all theme colors
    """
    return DARK_THEME if is_dark_mode else LIGHT_THEME
