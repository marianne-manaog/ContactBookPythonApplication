# This Python file contains the application window-related class, which enables to set its parameters and load the
# saved contacts on it. The design and implementation of the GUI via tkinter were partly inspired by the work of
# https://github.com/rhdalton/Python-Contact-book-application.

from tkinter import Frame, StringVar

from contact_book.src.contact_book.constants import (
    DIMENSIONS_FORMAT_WINDOW_FRAME, HEIGHT_MAIN_WINDOW_FRAME,
    PADDING_X_OUTER_FRAME, PADDING_Y_OUTER_FRAME,
    TEXT_FONT_AND_SIZE_FORMAT_WINDOW_FRAME,
    TEXT_FONT_AND_SIZE_MAIN_WINDOW_FRAME, TITLE_MAIN_WINDOW_FRAME,
    WIDTH_MAIN_WINDOW_FRAME, ZERO_VALUE)
from contact_book.src.contact_book.gui import contacts_user_interface
from contact_book.src.contact_book.service.contacts_service import \
    ContactsService


class ApplicationWindow(Frame):
    """
    A class to set application window's properties, including geometric (width, height, resizing)
    and formatting-related parameters (font, title, contacts' fields), and load the list of contacts
    saved in the contacts_dict.txt file.
    """

    def __init__(self, application, *args, **kwargs):

        Frame.__init__(self, *args, **kwargs)
        self.application = application

        # Define geometry of main window frame
        self.application.geometry(
            DIMENSIONS_FORMAT_WINDOW_FRAME.format(WIDTH_MAIN_WINDOW_FRAME, HEIGHT_MAIN_WINDOW_FRAME)
        )

        # Set font and title of main window frame
        self.application.option_add(TEXT_FONT_AND_SIZE_FORMAT_WINDOW_FRAME, TEXT_FONT_AND_SIZE_MAIN_WINDOW_FRAME)
        self.application.title(TITLE_MAIN_WINDOW_FRAME)

        # Add outer frame with required padding
        self.main_frame = Frame(self.application)
        self.main_frame.grid(row=ZERO_VALUE, column=ZERO_VALUE, padx=PADDING_X_OUTER_FRAME, pady=PADDING_Y_OUTER_FRAME)

        # Set fields for tkinter GUI
        self.id_field = StringVar()
        self.forename_field = StringVar()
        self.surname_field = StringVar()
        self.email_address_field = StringVar()
        self.mobile_number_field = StringVar()

        # Define list of fields to populate with contacts' details
        self.contacts_fields = []
        self.contacts_fields.append(self.id_field)
        self.contacts_fields.append(self.forename_field)
        self.contacts_fields.append(self.surname_field)
        self.contacts_fields.append(self.email_address_field)
        self.contacts_fields.append(self.mobile_number_field)

        # Initialise empty list of contacts to display them
        self.contacts_list = []
        self.contacts_box_running_index = ZERO_VALUE

        # Show GUI into main window frame
        contacts_user_interface.get_user_interface(self)

        # Instantiate the object by feeding 'application' as context to the 'ContactsService' class to be
        # able to consume it and leverage its 'load_contacts_list' method
        contact_service_object = ContactsService(self)

        # Populate list of contacts with the saved ones
        contact_service_object.load_contacts_list()
