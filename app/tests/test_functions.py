import unittest
from unittest.mock import patch
from io import StringIO
from app.functions import get_username, get_password


class TestFunctions(unittest.TestCase):

    def test_get_username(self):
        expected_output = "test_user"
        with patch('builtins.input', return_value=expected_output):
            self.assertEqual(get_username(), expected_output)

    def test_get_password(self):
        expected_output = "test_password"
        with patch('builtins.input', return_value=expected_output):
            self.assertEqual(get_password(), expected_output)


if __name__ == '__main__':
    unittest.main()
