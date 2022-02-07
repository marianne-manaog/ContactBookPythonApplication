import unittest
from pandas.testing import assert_frame_equal

import json
import pandas as pd

from contact_book.src.contact_book.gui.application_window import ApplicationWindow
from contact_book.src.contact_book.service.contacts_service import ContactsService

from contact_book.root import get_contact_book_root


project_root_dir = get_contact_book_root()
root_dir_dummy_contacts_dict = '/tests/contact_book/dummy_data/'
file_name_dummy_contacts_dict = 'dummy_contacts_dict.txt'
file_name_dummy_contacts_dict_prior_to_one_contact_removal = 'dummy_contacts_dict_prior_to_one_contact_removal.txt'
file_name_dummy_contacts_dict_w_new_contact_created = 'dummy_contacts_dict_w_new_contact_created.txt'
file_name_dummy_contacts_dict_wo_contact_removed = 'dummy_contacts_dict_wo_contact_removed.txt'

concatenated_root_dirs_and_file_name = project_root_dir + root_dir_dummy_contacts_dict + file_name_dummy_contacts_dict
concatenated_root_dirs_and_file_name_prior_to_one_contact_removal = \
    project_root_dir + root_dir_dummy_contacts_dict + file_name_dummy_contacts_dict_prior_to_one_contact_removal
concatenated_root_dirs_and_file_name_w_new_contact_created = project_root_dir + root_dir_dummy_contacts_dict + \
                                                             file_name_dummy_contacts_dict_w_new_contact_created
concatenated_root_dirs_and_file_name_wo_contact_removed = project_root_dir + root_dir_dummy_contacts_dict + \
                                                             file_name_dummy_contacts_dict_wo_contact_removed

with open(concatenated_root_dirs_and_file_name) as dummy_contacts_dict_file:
    expected_dummy_contacts_dict = json.load(dummy_contacts_dict_file)

with open(concatenated_root_dirs_and_file_name_prior_to_one_contact_removal) \
        as dummy_contacts_dict_file_prior_to_removal:
    expected_dummy_contacts_dict_prior_to_removal = json.load(dummy_contacts_dict_file_prior_to_removal)

with open(concatenated_root_dirs_and_file_name_w_new_contact_created) as dummy_contacts_dict_file_w_new_contact_created:
    expected_dummy_contacts_dict_w_new_contact_created = json.load(dummy_contacts_dict_file_w_new_contact_created)

with open(concatenated_root_dirs_and_file_name_wo_contact_removed) as dummy_contacts_dict_file_wo_contact_removed:
    expected_dummy_contacts_dict_wo_contact_removed = json.load(dummy_contacts_dict_file_wo_contact_removed)

contacts_service_object = ContactsService(ApplicationWindow)

DUMMY_ID = 55
DUMMY_FORENAME = 'Sheldon'
DUMMY_SURNAME = 'Cooper'
DUMMY_EMAIL_ADDRESS = 'sheldor@myphdmail.com'
DUMMY_MOBILE_NUMBER = '00000000073'


class TestContactService(unittest.TestCase):

    def test_create_contact(self):

        result_updated_contacts_dict = contacts_service_object.create_contact_logic(
            expected_dummy_contacts_dict,
            DUMMY_FORENAME,
            DUMMY_SURNAME,
            DUMMY_EMAIL_ADDRESS,
            DUMMY_MOBILE_NUMBER
        )

        self.assertEqual(expected_dummy_contacts_dict_w_new_contact_created, result_updated_contacts_dict)

    def test_update_contact(self):

        contact_to_update = pd.DataFrame({
            'id': [DUMMY_ID],
            'forename': ["Leonard"],
            'surname': ["Hofstadter"],
            'email_address': ["dr.hofstadter@myd&dmail.com"],
            'mobile_number': ["00000000074"]
        })

        expected_updated_contact = pd.DataFrame({
            'id': [DUMMY_ID],
            'forename': [DUMMY_FORENAME],
            'surname': [DUMMY_SURNAME],
            'email_address': [DUMMY_EMAIL_ADDRESS],
            'mobile_number': [DUMMY_MOBILE_NUMBER]
        })

        result_updated_contact = contacts_service_object.update_contact_logic(
            contact_to_update,
            DUMMY_FORENAME,
            DUMMY_SURNAME,
            DUMMY_EMAIL_ADDRESS,
            DUMMY_MOBILE_NUMBER
        )

        assert_frame_equal(expected_updated_contact, result_updated_contact)

    def test_remove_contact(self):

        # index '2' corresponding to contact of id '15' to be removed
        index_to_be_removed = 2

        result_dict_wo_contact_removed = contacts_service_object.remove_contact_logic(
            contacts_dict=expected_dummy_contacts_dict_prior_to_removal,
            index_of_id_to_be_removed=index_to_be_removed
        )

        self.assertEqual(expected_dummy_contacts_dict_wo_contact_removed, result_dict_wo_contact_removed)
