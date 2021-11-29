import unittest
import requests


class TestStatus(unittest.TestCase):
    """class for checking if the links are valid"""
    def test_pages(self):
        with self.subTest(msg='test_open_pages'):
            expected_status = 200
            self.assertEqual(expected_status, requests.get('http://127.0.0.1:5000/').status_code)
            self.assertEqual(expected_status, requests.get('http://127.0.0.1:5000/bio').status_code)
            self.assertEqual(expected_status, requests.get('http://127.0.0.1:5000/repertoire').status_code)
            self.assertEqual(expected_status, requests.get('http://127.0.0.1:5000/events').status_code)
            self.assertEqual(expected_status, requests.get('http://127.0.0.1:5000/media').status_code)
            self.assertEqual(expected_status, requests.get('http://127.0.0.1:5000/contacts').status_code)
            self.assertEqual(expected_status, requests.get('http://127.0.0.1:5000/feedback').status_code)
            self.assertEqual(expected_status, requests.get('http://127.0.0.1:5000/admin').status_code)


if __name__ == "__main__":
    unittest.main()
