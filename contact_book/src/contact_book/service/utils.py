# This Python file contains the contacts' service with the functions to perform CRUD operations to create, read, update,
# and delete contacts, as well as search for a particular one based on a keyword/string.

import json
from tkinter import END
from typing import Dict

import pandas as pd

from contact_book.root import get_contact_book_root
from contact_book.src.contact_book.constants import (
    FILE_NAME_CONTACTS_DICT, ONE_VALUE, ROOT_DIR_CONTACTS_DICT_FILE,
    ZERO_VALUE)

root_dir = get_contact_book_root()


def get_contacts_dict(
        contacts_file_root_dir: str = ROOT_DIR_CONTACTS_DICT_FILE,
        contacts_file_name: str = FILE_NAME_CONTACTS_DICT
) -> Dict:
    """
    Get dictionary of contacts from input .txt file

    :param contacts_file_root_dir: the root directory where the file with the saved contacts is stored.
    :param contacts_file_name: the .txt file with the saved contacts.

    :return: a dictionary with the saved contacts having the following keys:
            "id" (list of integers), "forename" (list of strings), "surname" (list of strings),
            "email_address" (list of strings), "mobile_number" (list of strings)
    """

    with open(root_dir + '/' + contacts_file_root_dir + contacts_file_name) as contacts_dict_file:
        contacts_dict = json.load(contacts_dict_file)
    return contacts_dict


def save_contacts_dict(
        modified_contacts_dict: Dict,
        contacts_file_root_dir: str = ROOT_DIR_CONTACTS_DICT_FILE,
        contacts_file_name: str = FILE_NAME_CONTACTS_DICT
) -> None:
    """
    Save new dictionary of contacts to output .txt file based on the CRUD operation performed (except for reading
    , i.e., create, update, or delete)

    :param modified_contacts_dict: the modified dictionary of contacts to be saved.
    :param contacts_file_root_dir: the root directory where the file with the saved contacts is stored.
    :param contacts_file_name: the .txt file with the saved contacts.

    :return: a dictionary with the saved contacts having the following keys:
            "id" (list of integers), "forename" (list of strings), "surname" (list of strings),
            "email_address" (list of strings), "mobile_number" (list of strings)
    """

    json.dump(modified_contacts_dict, open(root_dir + '/' + contacts_file_root_dir + contacts_file_name, 'w'))


def convert_contacts_dict_to_df(contacts_dict: Dict) -> pd.DataFrame:
    """
    Convert a dictionary of contacts to a pandas dataframe

    :param contacts_dict:

    :return: a pandas dataframe of contacts having the following columns:
            "id", "forename", "surname", "email_address", "mobile_number"
    """

    contacts_df_from_dict = pd.DataFrame.from_dict(contacts_dict)
    return contacts_df_from_dict


def check_forename_or_surname_availability(application) -> None:  # pragma: no cover
    if application.forename_field.get() == "" or application.surname_field.get() == "":
        return


def insert_contacts_into_box(application) -> None:  # pragma: no cover
    """
    Get contacts from the list of contacts 'contacts_list' and insert them into the 'contacts_box' for them to be
    displayed on the GUI correctly.

    :param application: the application passed as a context from which the 'contacts_list' and 'contacts_box' are taken.
                'contacts_list' is a list of tuples of two elements for each contact (id, 'Forename Surname'),
                e.g., [(1, 'Kate Beckett'), (2, 'Richard Castle'), etc.]. 'contacts_box' is a Listbox from the Python
                library 'tkinter'.

    Note:
         The contacts from the 'contacts_list' are inserted into the 'contacts_box' in the 'application'.
    """

    application.contacts_box.delete(ZERO_VALUE, END)

    if application.contacts_list:
        # 'contact_id' is the id number (int) of the contact considered
        # 'contact_tuple' is a tuple of two elements per each contact (id, 'Forename Surname')
        for contact_id, contact_tuple in enumerate(application.contacts_list):
            application.contacts_box.insert(contact_id, contact_tuple[ONE_VALUE])


def clear_window_frame(application) -> None:  # pragma: no cover
    """
    Clear the window frame on the GUI.

    :param application: the application passed as a context from which the 'user_operation_frame' and 'contacts_box' are taken.
    """

    clear_window_frame_contacts_fields(application)
    create_gui_buttons(application)
    application.user_operation_frame.focus()
    application.contacts_box.selection_clear(ZERO_VALUE, END)
    application.contacts_box_running_index = ZERO_VALUE


def clear_window_frame_contacts_fields(application) -> None:  # pragma: no cover
    """
    Clear the contact fields on the GUI.

    :param application: the application passed as a context from which the 'contact_fields' are taken.
    """

    for contact_field in application.contacts_fields:
        contact_field.set("")


def create_gui_buttons(application, create_contact=True) -> None:  # pragma: no cover
    """
    Create buttons on the GUI for the user to perform the required CRUD operations.

    :param application: the application passed as a context. The buttons are created on its main window.
    :param create_contact: True if a new contact had to be created (showing 'Create' button alone on the GUI),
                            False otherwise (showing all buttons except for 'Create' on the GUI).
    """

    if create_contact:
        application.button_to_update_contact.grid_remove()
        application.button_to_delete_contact.grid_remove()
        application.button_to_clear_frame.grid_remove()
        application.button_to_create_contact.grid()
    else:
        application.button_to_create_contact.grid_remove()
        application.button_to_update_contact.grid()
        application.button_to_delete_contact.grid()
        application.button_to_clear_frame.grid()
