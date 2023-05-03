import unittest
from load_user_from_csv import load_csv_file
from load_user_from_csv import set_url


class TestCase_loadCsvFile(unittest.TestCase):
    def test_load_csv_file(self):
        user_list = load_csv_file()
        self.assertEqual(len(user_list),1260)  # add assertion here

    def test_check_email(self):
        user_list = load_csv_file()
        for item in user_list:
            if item['Name'] == 'Mihai Popa':
                self.assertEqual(item['Email'], 'mpopa@computas.com')

    def test_update_email(self):
        user_list = load_csv_file()
        url = set_url(user_list[0])
        self.assertEqual(url, 'https://api.atlassian.com/users/557058:04945d26-04bc-486c-86cc-095f92c06e45/manage/email')

if __name__ == '__main__':
    unittest.main()

