"""Utility functions for string manipulation."""

def reverse_string(s: str) -> str:
    """Return a new string with the characters of *s* in reverse order.

    The function works with any Unicode string and preserves the original
    string unchanged.

    Args:
        s: The string to reverse.

    Returns:
        A new string containing the characters of *s* reversed.
    """
    # Pythonic way using slicing; works for empty strings as well.
    return s[::-1]
