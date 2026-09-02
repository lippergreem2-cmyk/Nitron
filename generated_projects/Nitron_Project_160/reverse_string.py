def reverse_string(s: str) -> str:
    """Return the reverse of the input string.

    Args:
        s: The string to reverse.

    Returns:
        The reversed string.
    """
    # Using slicing which correctly handles Unicode characters.
    return s[::-1]
