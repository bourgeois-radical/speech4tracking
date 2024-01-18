import unittest
# from unittest import TestCase
from unittest_parametrize import parametrize, param
from unittest_parametrize import ParametrizedTestCase
# from parameterized import parameterized
from pattern_recognizer import PatternRecognizerText2Speech
from typing import Union


class TestPatternRecognizer(ParametrizedTestCase):
    @parametrize(
        'user_input, expected',

        [
            # I would like to take to measurements
            param('I would like to take to measurements', 2, id='to_as_two'),
            param('I wanna take 1 measurement', 1, id='test_digit_input_1'),
            param('I wanna take 2 measurements', 2, id='test_digit_input_2'),
            param('I wanna take 3 measurements', 3, id='test_digit_input_3'),
            param('I wanna take 4 measurements', 4, id='test_digit_input_4'),

            param('I wanna take one measurements', 1, id='test_word_input_one'),
            param('I wanna take two measurements', 2, id='test_word_input_two'),
            param('I wanna take three measurements', 3, id='test_word_input_three'),
            param('I wanna take four measurements', 4, id='test_word_input_four'),

            param('I wanna take One measurement', 1, id='test_mixed_case_input_one'),
            param('I wanna take tWo measurements', 2, id='test_mixed_case_input_two'),
            param('I wanna take ThReE measurements', 3, id='test_mixed_case_input_three'),
            param('I wanna take fOUr measurements', 4, id='test_mixed_case_input_four'),

            param('I wanna take 0 measurements', ValueError, id='test_out_of_range_input_below'), # IndexError: list index out of range
            param('I wanna take 5 measurements', ValueError, id='test_out_of_range_input_above'), # IndexError: list index out of range
            param('I wanna take five measurements', ValueError, id='test_out_of_range_input_invalid'), # IndexError: list index out of range

            param('I wanna take [2] measurements', ValueError, id='test_invalid_input_type_list'), # ValueError don't need 2
            param("I wanna take {'three': 3} measurements", ValueError, id='test_invalid_input_type_dict'), # Exception: Something went wrong. More than one number was found.
            # TODO: if more than one number was found, how to restart the input. Should be this exception inside the main.py maybe?
        ])
    def test_recognize_number(self, user_input: str, expected: Union[int, ValueError]) -> None:
        # TODO: ask Roman why shouldn't I initialize an instance of a class here? Like pattern_recognizer = PatternRecognizerText2Speech()
        self.assertEqual(PatternRecognizerText2Speech.recognize_number(user_input), expected)


if __name__ == '__main__':
    unittest.main()
# python -m unittest pattern_recognizer_test.py
