# This Python file enables to get the user interface with the required visible fields ("Forename", "Surname",
# "Email address", "Mobile number") and buttons for the user to perform CRUD operations, as well as search for a
# particular contact. The design and implementation of the GUI via tkinter were partly inspired by the work of
# # https://github.com/rhdalton/Python-Contact-book-application.

from tkinter import (EW, NSEW, RAISED, SINGLE, VERTICAL, Button, E, Entry,
                     Frame, Label, Listbox, N, S, Scrollbar, W)

from contact_book.src.contact_book.constants import (
    BG_COLOUR, CLEAR_FIELD_LABEL, CREATE_FIELD_LABEL,
    EMAIL_ADDRESS_FIELD_LABEL, EVENT_PATTERN_LIST_BOX_LABEL,
    FORENAME_FIELD_LABEL, MOBILE_NUMBER_FIELD_LABEL, ONE_VALUE,
    PADDING_X_BUTTON, PADDING_Y_BUTTON, REMOVE_FIELD_LABEL, ROW_SPAN,
    SEARCH_BOX_MESSAGE, SURNAME_FIELD_LABEL, TWO_VALUE, UPDATE_FIELD_LABEL,
    WIDTH_VISIBLE_CONTACT_FIELD, ZERO_VALUE)
from contact_book.src.contact_book.service.contacts_service import \
    ContactsService
from contact_book.src.contact_book.service.utils import clear_window_frame


def get_user_interface(application) -> None:
    """
    A function to get the user interface of the 'application', along with its fields to be displayed on the GUI.
    """

    # Instantiate the object by feeding 'application' as context to the 'ContactsService' class to be
    # able to consume it and leverage its CRUD methods
    contact_service_object = ContactsService(application)

    # Add hidden field to save ID number for each of the contacts in the list
    Entry(application.main_frame, text=application.id_field, width=ZERO_VALUE).grid(row=ONE_VALUE, column=ZERO_VALUE)

    # Add visible field to save forename for each of the contacts in the list
    Label(application.main_frame, text=FORENAME_FIELD_LABEL).grid(row=ZERO_VALUE, column=ZERO_VALUE, sticky=W)
    Entry(
        application.main_frame,
        text=application.forename_field,
        width=WIDTH_VISIBLE_CONTACT_FIELD
    ).grid(row=ONE_VALUE, column=ZERO_VALUE)

    # Add visible field to save surname for each of the contacts in the list
    row_value_surname_field = TWO_VALUE + ONE_VALUE
    Label(application.main_frame, text=SURNAME_FIELD_LABEL).grid(row=TWO_VALUE, column=ZERO_VALUE, sticky=W)
    Entry(
        application.main_frame,
        text=application.surname_field,
        width=WIDTH_VISIBLE_CONTACT_FIELD
    ).grid(row=row_value_surname_field, column=ZERO_VALUE)

    # Add visible field to save email address for each of the contacts in the list
    row_value_email_address_field = row_value_surname_field + TWO_VALUE
    Label(
        application.main_frame,
        text=EMAIL_ADDRESS_FIELD_LABEL
    ).grid(row=row_value_email_address_field - ONE_VALUE, column=ZERO_VALUE, sticky=W)
    Entry(
        application.main_frame,
        text=application.email_address_field,
        width=WIDTH_VISIBLE_CONTACT_FIELD
    ).grid(row=row_value_email_address_field, column=ZERO_VALUE)

    # Add visible field to save mobile number for each of the contacts in the list
    row_value_mobile_number_field = row_value_email_address_field + TWO_VALUE
    Label(
        application.main_frame,
        text=MOBILE_NUMBER_FIELD_LABEL
    ).grid(row=row_value_mobile_number_field - ONE_VALUE, column=ZERO_VALUE, sticky=W)
    Entry(
        application.main_frame,
        text=application.mobile_number_field,
        width=WIDTH_VISIBLE_CONTACT_FIELD
    ).grid(row=row_value_mobile_number_field, column=ZERO_VALUE)

    # Add frame for buttons on CRUD ('Create', 'Read' (by clicking on a contact in the list), 'Update', 'Delete')
    # operations the user can perform from the GUI. 'Clear' is also made available.
    row_value_action_frame = row_value_mobile_number_field + TWO_VALUE
    application.user_operation_frame = Frame(application.main_frame)
    application.user_operation_frame.grid(row=row_value_action_frame, column=ZERO_VALUE, sticky=EW)

    # Button to 'Create' a contact
    application.button_to_create_contact = Button(
        application.user_operation_frame,
        text=CREATE_FIELD_LABEL,
        command=lambda: contact_service_object.create_contact_on_gui(),
        relief=RAISED,
        bg=BG_COLOUR
    )
    application.button_to_create_contact.grid(row=ZERO_VALUE, column=ZERO_VALUE, pady=PADDING_Y_BUTTON)

    # Button to 'Update' a contact
    application.button_to_update_contact = Button(
        application.user_operation_frame,
        text=UPDATE_FIELD_LABEL,
        command=lambda: contact_service_object.update_contact_on_gui(),
        relief=RAISED,
        bg=BG_COLOUR
    )
    application.button_to_update_contact.grid(
        row=ZERO_VALUE,
        column=ZERO_VALUE,
        pady=PADDING_Y_BUTTON,
        padx=PADDING_X_BUTTON)
    application.button_to_update_contact.grid_remove()

    # Button to 'Delete' a contact
    application.button_to_delete_contact = Button(
        application.user_operation_frame,
        text=REMOVE_FIELD_LABEL,
        command=lambda: contact_service_object.remove_contact_on_gui(),
        relief=RAISED,
        bg=BG_COLOUR
    )
    application.button_to_delete_contact.grid(
        row=ZERO_VALUE,
        column=ONE_VALUE,
        pady=PADDING_Y_BUTTON,
        padx=PADDING_X_BUTTON)
    application.button_to_delete_contact.grid_remove()

    # Button to 'Clear' the fields
    application.button_to_clear_frame = Button(
        application.user_operation_frame,
        text=CLEAR_FIELD_LABEL,
        command=lambda: clear_window_frame(application=application),
        relief=RAISED,
        bg=BG_COLOUR
    )
    application.button_to_clear_frame.grid(
        row=ZERO_VALUE,
        column=TWO_VALUE,
        pady=PADDING_Y_BUTTON,
        padx=PADDING_X_BUTTON)
    application.button_to_clear_frame.grid_remove()

    # Add the 'Listbox' containing the contacts with a scroll bar
    side_scroll_bar = Scrollbar(application.main_frame, orient=VERTICAL)
    application.contacts_box = Listbox(
        application.main_frame,
        exportselection=ZERO_VALUE,
        yscrollcommand=side_scroll_bar.set,
        width=WIDTH_VISIBLE_CONTACT_FIELD - TWO_VALUE,
        selectmode=SINGLE
    )
    application.contacts_box.bind(EVENT_PATTERN_LIST_BOX_LABEL, lambda event: contact_service_object.choose_contact())
    side_scroll_bar.config(command=application.contacts_box.yview)
    application.contacts_box.grid(
        row=ONE_VALUE,
        column=ONE_VALUE,
        rowspan=ROW_SPAN,
        padx=(WIDTH_VISIBLE_CONTACT_FIELD - PADDING_X_BUTTON, ZERO_VALUE),
        sticky=NSEW
    )
    side_scroll_bar.grid(row=ONE_VALUE, column=TWO_VALUE, rowspan=ROW_SPAN, sticky=N+S+E)

    # TODO: To be enabled/integrated on the GUI (functionality is working in
    # 'Search' box to look for a contact based on a string/keyword
    Label(application.main_frame, text=SEARCH_BOX_MESSAGE).grid(
        row=ZERO_VALUE,
        column=ONE_VALUE,
        sticky=W,
        padx=(WIDTH_VISIBLE_CONTACT_FIELD + PADDING_X_BUTTON, ZERO_VALUE)
    )
    application_main_frame_to_search = Entry(application.main_frame)
    application_main_frame_to_search.grid(
        row=ZERO_VALUE,
        column=ONE_VALUE,
        sticky=W,
        padx=(WIDTH_VISIBLE_CONTACT_FIELD + PADDING_X_BUTTON, ZERO_VALUE)
    )
    application_main_frame_to_search.focus_set()
