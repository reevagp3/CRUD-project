"""Utility functions for the application."""


def validate_item_name(name):
    """
    Validate item name.
    
    Args:
        name: The item name to validate
        
    Returns:
        str: Cleaned item name
        
    Raises:
        ValueError: If name is invalid
    """
    if not name or not isinstance(name, str):
        raise ValueError("Item name must be a non-empty string")
    
    name = name.strip()
    if not name:
        raise ValueError("Item name cannot be empty or whitespace only")
    
    if len(name) > 255:
        raise ValueError("Item name must be less than 255 characters")
    
    return name


def validate_item_id(item_id):
    """
    Validate item ID.
    
    Args:
        item_id: The item ID to validate
        
    Returns:
        int: The validated item ID
        
    Raises:
        ValueError: If ID is invalid
    """
    try:
        item_id = int(item_id)
    except (ValueError, TypeError):
        raise ValueError("Item ID must be a valid integer")
    
    if item_id <= 0:
        raise ValueError("Item ID must be a positive integer")
    
    return item_id
