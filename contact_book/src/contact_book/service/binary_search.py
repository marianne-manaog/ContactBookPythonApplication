# This Python file implements the binary search algorithm to search through a list of contacts by a keyword (e.g., a
# surname)

import logging
from typing import List

from contact_book.src.contact_book.service.utils import get_contacts_dict


def binary_search(
        sorted_list_of_strings: List[str],
        string_to_be_searched: str,
        low_value: int = 0,
        high_value: int = None
):
    """
    A function to perform a binary search of a string in a list of strings.
    :param sorted_list_of_strings: a sorted list of strings, e.g., a list of contacts' surnames in alphabetical
                                        order.
    :param string_to_be_searched: the string to be searched, e.g., the surname of a contact.
    :param low_value: 0 by default.
    :param high_value: None by default.
    :return: the index corresponding to the string to be searched.
    """

    if low_value < 0:
        logging.error(f"low_value is {low_value}, but it cannot be negative")

    if high_value is None:
        high_value = len(sorted_list_of_strings)

    while low_value < high_value:

        middle_value = int((low_value + high_value)/2)
        if sorted_list_of_strings[middle_value] < string_to_be_searched:
            low_value = middle_value + 1
        else:
            high_value = middle_value

    return low_value


def find_contact(
        list_of_strings: List[str],
        string_to_be_searched: str,
        index_of_element_if_found: int = None
) -> bool:
    """
    A function to find a contact (string) in a list of contacts (list of strings).
    :param list_of_strings: a list of strings, e.g., a list of contacts.
    :param string_to_be_searched: a string to be searched, e.g., the surname of a contact.
    :param index_of_element_if_found: an integer corresponding to the index of an element (e.g., a surname) if found;
                                    by default, it is set to None.
    :return: a boolean (True if the contact were found in the given list, False otherwise)
    """

    contact_found = False
    if string_to_be_searched in list_of_strings:
        logging.info(f"The surname searched ({string_to_be_searched}) was found in the contacts' list and "
                     f"corresponds to the index number {index_of_element_if_found}.")
        contact_found = True
        return contact_found
    else:
        logging.error(f"The surname searched ({string_to_be_searched}) was not found in the contacts' list.")
        return contact_found


if __name__ == "__main__":

    contacts_dict = get_contacts_dict()

    # Sort surnames in alphabetical order
    list_to_be_searched = sorted(contacts_dict['surname'])

    # Surname to be searched
    input_string_to_be_searched = str(input("Enter surname to search: "))

    index_of_element = binary_search(list_to_be_searched, input_string_to_be_searched)

    find_contact(list_to_be_searched, input_string_to_be_searched, index_of_element)
