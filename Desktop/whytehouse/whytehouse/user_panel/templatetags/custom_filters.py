from django import template
import re

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Get an item from a dictionary using a key"""
    if dictionary is None:
        return 0
    return dictionary.get(key, 0)

@register.filter
def format_duration(duration_str):
    """Convert '5 Days 4 Nights' to '☀️ 5 / 🌙 4'"""
    if not duration_str:
        return ''
    
    # Extract days and nights using regex
    days_match = re.search(r'(\d+)\s*[Dd]', duration_str)
    nights_match = re.search(r'(\d+)\s*[Nn]', duration_str)
    
    days = days_match.group(1) if days_match else '0'
    nights = nights_match.group(1) if nights_match else str(int(days) - 1) if days != '0' else '0'
    
    return f'☀️ {days} / 🌙 {nights}'

@register.filter
def get_days(duration_str):
    """Extract days from duration string"""
    if not duration_str:
        return 0
    match = re.search(r'(\d+)\s*[Dd]', duration_str)
    return int(match.group(1)) if match else 0

@register.filter
def get_nights(duration_str):
    """Extract nights from duration string"""
    if not duration_str:
        return 0
    match = re.search(r'(\d+)\s*[Nn]', duration_str)
    if match:
        return int(match.group(1))
    # If no nights specified, calculate as days - 1
    days = get_days(duration_str)
    return days - 1 if days > 0 else 0
