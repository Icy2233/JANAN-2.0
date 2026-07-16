"""
Theme Manager
Manages dark theme and color schemes for the application
"""

import logging

logger = logging.getLogger(__name__)


class ThemeManager:
    """
    Manages application themes and color schemes
    """
    
    # Dark Theme Colors
    DARK_THEME = {
        'primary_bg': '#0a0e27',        # Main background
        'secondary_bg': '#1a1f3a',      # Secondary background
        'accent_primary': '#00d4ff',    # Primary accent (cyan)
        'accent_secondary': '#7c3aed',  # Secondary accent (purple)
        'text_primary': '#ffffff',      # Primary text
        'text_secondary': '#b0b0b0',    # Secondary text
        'border': '#2d3748',            # Border color
        'success': '#10b981',           # Success color
        'error': '#ef4444',             # Error color
        'warning': '#f59e0b',           # Warning color
        'info': '#3b82f6',              # Info color
    }
    
    # Light Theme Colors (optional)
    LIGHT_THEME = {
        'primary_bg': '#f8f9fa',
        'secondary_bg': '#e9ecef',
        'accent_primary': '#0084ff',
        'accent_secondary': '#7c3aed',
        'text_primary': '#000000',
        'text_secondary': '#495057',
        'border': '#dee2e6',
        'success': '#28a745',
        'error': '#dc3545',
        'warning': '#ffc107',
        'info': '#17a2b8',
    }
    
    def __init__(self, theme_name: str = 'dark'):
        """
        Initialize theme manager
        
        Args:
            theme_name (str): Theme to use ('dark' or 'light')
        """
        self.current_theme = theme_name
        self.theme_dict = self.get_theme(theme_name)
        logger.info(f"Theme Manager initialized with theme: {theme_name}")
    
    def get_theme(self, theme_name: str) -> dict:
        """
        Get theme dictionary
        
        Args:
            theme_name (str): Theme name ('dark' or 'light')
            
        Returns:
            dict: Theme colors
        """
        if theme_name.lower() == 'dark':
            return self.DARK_THEME.copy()
        elif theme_name.lower() == 'light':
            return self.LIGHT_THEME.copy()
        else:
            logger.warning(f"Unknown theme: {theme_name}, using dark theme")
            return self.DARK_THEME.copy()
    
    def switch_theme(self, theme_name: str) -> dict:
        """
        Switch to a different theme
        
        Args:
            theme_name (str): Theme name to switch to
            
        Returns:
            dict: New theme colors
        """
        self.current_theme = theme_name
        self.theme_dict = self.get_theme(theme_name)
        logger.info(f"Switched to theme: {theme_name}")
        return self.theme_dict
    
    def get_color(self, color_key: str) -> str:
        """
        Get a specific color from current theme
        
        Args:
            color_key (str): Color key name
            
        Returns:
            str: Hex color code
        """
        return self.theme_dict.get(color_key, '#ffffff')
    
    def get_all_colors(self) -> dict:
        """
        Get all colors from current theme
        
        Returns:
            dict: All theme colors
        """
        return self.theme_dict.copy()
    
    def custom_color(self, name: str, hex_code: str) -> None:
        """
        Add or override a custom color
        
        Args:
            name (str): Color name
            hex_code (str): Hex color code
        """
        self.theme_dict[name] = hex_code
        logger.info(f"Custom color added: {name} = {hex_code}")
    
    @staticmethod
    def validate_hex_color(hex_code: str) -> bool:
        """
        Validate hex color code
        
        Args:
            hex_code (str): Hex color code to validate
            
        Returns:
            bool: True if valid
        """
        if not hex_code.startswith('#'):
            return False
        
        if len(hex_code) not in [4, 7]:
            return False
        
        try:
            int(hex_code[1:], 16)
            return True
        except ValueError:
            return False
