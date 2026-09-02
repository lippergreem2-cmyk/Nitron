import unittest
from nitron_project import reverse_string


class TestReverseString(unittest.TestCase):
    def test_regular(self):
        self.assertEqual(reverse_string("hello"), "olleh")

    def test_empty(self):
        self.assertEqual(reverse_string(""), "")

    def test_palindrome(self):
        self.assertEqual(reverse_string("madam"), "madam")

    def test_unicode(self):
        self.assertEqual(reverse_string("ñáé"), "éáñ")


if __name__ == "__main__":
    unittest.main()
