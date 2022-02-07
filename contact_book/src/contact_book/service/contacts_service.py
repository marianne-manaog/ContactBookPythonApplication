# This Python file contains the contacts' service with the functions to perform CRUD operations to create, read, update,
# and delete contacts, as well as search for a particular one based on a keyword/string.

# The design and implementation of the GUI via tkinter were partly inspired by the work of
# https://github.com/rhdalton/Python-Contact-book-application; nevertheless, whilst that GitHub repository implemented
# 'spaghetti'-like functions and used a SQLite3 database, this contact service has been created to be more modular, by
# implementing a class ('ContactsService') and reading the data from an input .txt file, such that the methods
# defined in this file (under the class 'ContactsService') leverage Python-based (instead of SQL-based) CRUD operations,
# as assessed in this assignment. Furthermore, the codes have been decoupled further by creating separate 'constants.py'
# and 'utils.py' files to facilitate maintainability and reusability of constants/fixed parameters and utility-type
# of functions.

from collections import deque
from typing import Dict

import pandas as pd

from contact_book.root import get_contact_book_root
from contact_book.src.contact_book.constants import (ONE_VALUE, TWO_VALUE,
                                                     ZERO_VALUE)

from .utils import (check_forename_or_surname_availability, clear_window_frame,
                    clear_window_frame_contacts_fields,
                    convert_contacts_dict_to_df, create_gui_buttons,
                    get_contacts_dict, insert_contacts_into_box,
                    save_contacts_dict)

root_dir = get_contact_book_root()


class ContactsService:
    """
    A contacts service class that implements the business logic and enables to perform CRUD operations for the user
    to interact with the application and maintain their contacts' list.
    """

    def __init__(self, application):
        self.application = application

    def load_contacts_list(self) -> None:  # pragma: no cover
        """
        Extract the dictionary of contacts and add it to the 'contacts_list' and then to the 'contacts_box' of
        the application.
        """

        # Clear list of contacts
        self.application.contacts_list.clear()

        contacts_dict = get_contacts_dict()
        contacts_df_from_dict = convert_contacts_dict_to_df(contacts_dict)

        # Sort contacts in alphabetical order based on their surnames
        contacts_df_from_dict.sort_values(by=['surname'], inplace=True, ascending=True)

        # 'row' is a tuple of three elements (id as int, forename as str, surname as str), e.g., (1, 'Kate', 'Beckett')
        contacts_deque = deque()
        for index, row in contacts_df_from_dict.iterrows():
            # Add each id, forename, and surname of each contact to the 'contacts_deque'
            contacts_deque.append((row[ZERO_VALUE], row[ONE_VALUE] + " " + row[TWO_VALUE]))

        self.application.contacts_list = list(contacts_deque)

        insert_contacts_into_box(self.application)

    def choose_contact(self) -> None:  # pragma: no cover
        """
        Choose the contact corresponding to the user's click on the GUI.
        """

        # 'index' is an int denoting the contact's position in tkinter's Listbox
        index = self.application.contacts_box.curselection()[ZERO_VALUE] + ONE_VALUE

        # Check if chosen 'index' were not the running one in the contact box
        if index != self.application.contacts_box_running_index:
            self.application.contacts_box_running_index = index

            # 'chosen_id' is an int (e.g., 4) indicating the id of the chosen contact.
            # 'application.contacts_list' is a list of tuples of two elements for each contact, e.g.,
            # [(1, 'Kate Beckett'), (2, 'Richard Castle'), etc.].
            chosen_id = (self.application.contacts_list[index - ONE_VALUE][ZERO_VALUE],)
            contacts_dict = get_contacts_dict()

            # Initialise placeholder/empty pandas series for 'contact_chosen'
            contact_chosen = pd.Series(
                data=[ZERO_VALUE, "", "", "", ""],
                index=['id', 'forename', 'surname', 'email_address', 'mobile_number']
            )
            for key, val in contacts_dict.items():
                if key == 'id':
                    contacts_df_from_dict = convert_contacts_dict_to_df(contacts_dict)
                    contact_chosen = contacts_df_from_dict[
                        contacts_df_from_dict['id'] == chosen_id[ZERO_VALUE]
                    ].iloc[ZERO_VALUE]
                    break

            for i in range(len(self.application.contacts_fields)):
                # Populate the contact's fields with the details of the chosen contact
                self.application.contacts_fields[i].set(contact_chosen[i])

            create_gui_buttons(self.application, create_contact=False)

    @staticmethod
    def create_contact_logic(
            contacts_dict: Dict,
            forename_to_create: str,
            surname_to_create: str,
            email_address_to_create: str,
            mobile_number_to_create: str
    ) -> Dict:
        """
        Append a contact to create to existing dictionary of contacts

        :param contacts_dict: the initial dictionary of contacts.
        :param forename_to_create: the forename of the contact to create.
        :param surname_to_create: the surname of the contact to create.
        :param email_address_to_create: the email address of the contact to create.
        :param mobile_number_to_create: the mobile number of the contact to create.
        :return: the updated dictionary of contacts with the new contact created as well
        """

        # Add new contact to 'contacts_dict'
        contacts_dict['id'].append(max(contacts_dict['id']) + ONE_VALUE)
        contacts_dict['forename'].append(forename_to_create)
        contacts_dict['surname'].append(surname_to_create)
        contacts_dict['email_address'].append(email_address_to_create)
        contacts_dict['mobile_number'].append(mobile_number_to_create)

        return contacts_dict

    def create_contact_on_gui(self) -> None:  # pragma: no cover
        """
        Create a contact and show it on the GUI.
        """

        check_forename_or_surname_availability(self.application)

        # Get inputs from users defining contact to create
        forename_to_create = self.application.forename_field.get()
        surname_to_create = self.application.surname_field.get()
        email_address_to_create = self.application.email_address_field.get()
        mobile_number_to_create = self.application.mobile_number_field.get()

        contacts_dict = get_contacts_dict()

        updated_contacts_dict = self.create_contact_logic(
            contacts_dict,
            forename_to_create,
            surname_to_create,
            email_address_to_create,
            mobile_number_to_create
        )

        save_contacts_dict(updated_contacts_dict)

        clear_window_frame_contacts_fields(self.application)
        self.load_contacts_list()

    @staticmethod
    def update_contact_logic(
            contact_to_update: pd.DataFrame,
            forename_to_update: str,
            surname_to_update: str,
            email_address_to_update: str,
            mobile_number_to_update: str
    ) -> pd.DataFrame:
        """
        Update the details (forename, surname, email address, and mobile number) of a contact

        :param contact_to_update: the initial pandas dataframe of the contact to update.
        :param forename_to_update: the forename of the contact to update.
        :param surname_to_update: the surname of the contact to update.
        :param email_address_to_update: the email address of the contact to update.
        :param mobile_number_to_update: the mobile number of the contact to update.
        :return: the contact with their updated details
        """

        contact_to_update.iloc[ZERO_VALUE, contact_to_update.columns.get_loc('forename')] = forename_to_update
        contact_to_update.iloc[ZERO_VALUE, contact_to_update.columns.get_loc('surname')] = surname_to_update
        contact_to_update.iloc[ZERO_VALUE, contact_to_update.columns.get_loc('email_address')] = email_address_to_update
        contact_to_update.iloc[ZERO_VALUE, contact_to_update.columns.get_loc('mobile_number')] = mobile_number_to_update

        return contact_to_update

    def update_contact_on_gui(self) -> None:  # pragma: no cover
        """
        Update a contact and show it on the GUI.
        """

        check_forename_or_surname_availability(self.application)

        id_to_update = self.application.id_field.get()
        forename_to_update = self.application.forename_field.get()
        surname_to_update = self.application.surname_field.get()
        email_address_to_update = self.application.email_address_field.get()
        mobile_number_to_update = self.application.mobile_number_field.get()

        contacts_dict = get_contacts_dict()
        contacts_df_from_dict = convert_contacts_dict_to_df(contacts_dict)

        contact_to_update = contacts_df_from_dict[contacts_df_from_dict['id'] == int(id_to_update)]

        # Update contact's forename, surname, email address, and mobile number based on new inputs from user on the GUI
        updated_contact = self.update_contact_logic(
            contact_to_update,
            forename_to_update,
            surname_to_update,
            email_address_to_update,
            mobile_number_to_update
        )

        # Replace previous version of a contact with its updated version based on user's inputs on the GUI
        contacts_df_from_dict[contacts_df_from_dict['id'] == int(id_to_update)] = updated_contact

        contacts_dict_from_df = contacts_df_from_dict.to_dict(orient='list')
        save_contacts_dict(contacts_dict_from_df)

        clear_window_frame(self.application)
        self.load_contacts_list()

    @staticmethod
    def remove_contact_logic(
            contacts_dict: Dict,
            index_of_id_to_be_removed: int
    ) -> Dict:
        """
        Remove a contact from an existing dictionary of contacts

        :param contacts_dict: the initial dictionary of contacts.
        :param index_of_id_to_be_removed: the index of the id of the contact to remove.
        :return: the updated dictionary of contacts without the contact removed

        Note: a list has been used with the 'pop' method, as 'deque' does not have a 'pop' method to remove items by
                their index. The 'del' method available for a 'deque' to do so has the same time complexity as the
                'pop' method for lists in the worst case scenario (O(n)).
        """

        contacts_dict['id'].pop(index_of_id_to_be_removed)
        contacts_dict['forename'].pop(index_of_id_to_be_removed)
        contacts_dict['surname'].pop(index_of_id_to_be_removed)
        contacts_dict['email_address'].pop(index_of_id_to_be_removed)
        contacts_dict['mobile_number'].pop(index_of_id_to_be_removed)

        return contacts_dict

    def remove_contact_on_gui(self) -> None:  # pragma: no cover
        """
        Remove a contact and ensure it is no longer visible on the GUI.
        """

        id_to_be_removed = int(self.application.id_field.get())

        contacts_dict = get_contacts_dict()

        index_of_id_to_be_removed = contacts_dict['id'].index(id_to_be_removed)

        # Remove contact based on the index of its ID
        updated_contacts_dict = self.remove_contact_logic(
            contacts_dict,
            index_of_id_to_be_removed
        )

        save_contacts_dict(updated_contacts_dict)

        clear_window_frame(self.application)
        self.load_contacts_list()
