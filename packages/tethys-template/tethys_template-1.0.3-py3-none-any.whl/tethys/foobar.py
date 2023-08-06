"""Trivial functions for demonstration purposes."""
import requests


def foo() -> str:
    """Print 'bar' to the screen.

    Returns:
        str: The string literal 'bar'.
    """
    return "bar"


def fetch() -> int:
    """Return the status code of a GET request to github.com.

    Returns:
        int: 200 if successful, or some other value upon failure.
    """
    return requests.get("https://github.com").status_code
