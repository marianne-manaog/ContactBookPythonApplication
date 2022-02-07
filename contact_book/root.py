# This Python file contains a utility-type of function to get the contact book-related root directory as a string.

from pathlib import Path


def get_contact_book_root() -> str:
    return str(Path(__file__).parent.parent)
