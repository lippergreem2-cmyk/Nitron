def is_prime(n: int) -> bool:
    """Return True if *n* is a prime number, otherwise False.

    The implementation uses the 6k ± 1 optimization:
    - All primes greater than 3 can be written in the form 6k ± 1.
    - We first filter out numbers <= 1, even numbers, and multiples of 3.
    - Then we test divisibility only for numbers of the form 6k‑1 and 6k+1 up to √n.
    """
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True
