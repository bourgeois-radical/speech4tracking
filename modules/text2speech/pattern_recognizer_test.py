import sys
import unittest
from unittest import TestCase
from modules.text2speech.pattern_recognizer import recognize_number


class TestRecognizeNumber(TestCase):

    def test_one(self):
        voice_input = 'I wanna take just one measurement'
        print(voice_input)
        self.assertEqual(recognize_number(voice_input), 1, 'Something went wrong')


if __name__ == '__main__':
    unittest.main()
