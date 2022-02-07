import unittest
from pandas.testing import assert_frame_equal

import json

import pandas as pd

from contact_book.root import get_contact_book_root

from contact_book.src.contact_book.service.contacts_service import (
    convert_contacts_dict_to_df,
    get_contacts_dict,
    save_contacts_dict
)


project_root_dir = get_contact_book_root()
root_dir_dummy_contacts_dict = '/tests/contact_book/dummy_data/'
file_name_dummy_contacts_dict = 'dummy_contacts_dict.txt'

concatenated_root_dirs_and_file_name = project_root_dir + root_dir_dummy_contacts_dict + file_name_dummy_contacts_dict

with open(concatenated_root_dirs_and_file_name) as dummy_contacts_dict_file:
    expected_dummy_contacts_dict = json.load(dummy_contacts_dict_file)


class TestUtils(unittest.TestCase):

    def test_get_contacts_dict(self):

        result_dummy_contacts_dict = get_contacts_dict(
            contacts_file_root_dir=root_dir_dummy_contacts_dict,
            contacts_file_name=file_name_dummy_contacts_dict
        )

        self.assertEqual(expected_dummy_contacts_dict, result_dummy_contacts_dict)

    def test_save_contacts_dict(self):

        json.dump(expected_dummy_contacts_dict, open(concatenated_root_dirs_and_file_name, 'w'))

        save_contacts_dict(
            modified_contacts_dict=expected_dummy_contacts_dict,
            contacts_file_root_dir=root_dir_dummy_contacts_dict,
            contacts_file_name=file_name_dummy_contacts_dict
        )

        with open(concatenated_root_dirs_and_file_name) as result_saved_dummy_contacts_file:
            result_saved_dummy_contacts_dict = json.load(result_saved_dummy_contacts_file)

        self.assertEqual(expected_dummy_contacts_dict, result_saved_dummy_contacts_dict)

    def test_convert_contacts_dict_to_df(self):

        expected_df = pd.DataFrame({
                    'id': [13, 14, 15],
                    'forename': ["Richard", "Wolfgang", "Erwin"],
                    'surname': ["Feynman", "Pauli", "Schrodinger"],
                    'email_address': [
                        "rick.feynman@mytopquantummail.com",
                        "wolfy.pauli@mybestquantummail.com",
                        "erwin.schrodinger@mycatsmailmaybe.com"],
                    'mobile_number': ["00000000021", "00000000022", "00000000023"]
        })

        result_df_from_dict = convert_contacts_dict_to_df(expected_dummy_contacts_dict)

        assert_frame_equal(expected_df, result_df_from_dict)
