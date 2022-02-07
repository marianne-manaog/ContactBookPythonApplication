import unittest

from contact_book.src.contact_book.service.binary_search import binary_search, find_contact


class TestBinarySearch(unittest.TestCase):

    def test_binary_search(self):

        dummy_sorted_list_of_strings = ['Cooper', 'Hofstadter', 'Fowler', 'Wolowitz']
        dummy_string_to_be_searched = 'Cooper'

        expected_index = 0
        result_index = binary_search(dummy_sorted_list_of_strings, dummy_string_to_be_searched)

        self.assertEqual(expected_index, result_index)

    def test_find_contact_found(self):

        dummy_sorted_list_of_strings = ['Cooper', 'Hofstadter', 'Fowler', 'Wolowitz']
        dummy_string_to_be_searched = 'Cooper'

        input_index = 0
        expected_boolean = True

        result_boolean = find_contact(dummy_sorted_list_of_strings, dummy_string_to_be_searched, input_index)

        self.assertEqual(expected_boolean, result_boolean)

    def test_find_contact_not_found(self):

        dummy_sorted_list_of_strings = ['Cooper', 'Hofstadter', 'Fowler', 'Wolowitz']
        dummy_string_to_be_searched = 'Kripke'

        input_index = None
        expected_boolean = False

        result_boolean = find_contact(dummy_sorted_list_of_strings, dummy_string_to_be_searched, input_index)

        self.assertEqual(expected_boolean, result_boolean)
