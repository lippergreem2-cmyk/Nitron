# Utility functions for string manipulation
"""Utility functions for string manipulation.

This module currently provides a function to reverse a string.
"""

def reverse_string(s: str) -> str:
    """Return a new string with the characters of ``s`` in reverse order.

    Parameters
    ----------
    s : str
        The input string to reverse.

    Returns
    -------
    str
        The reversed string.

    Examples
    --------
    >>> reverse_string("abc")
    'cba'
    """
    # Using Python slicing which efficiently creates a reversed copy.
    return s[::-1]
