import unittest
from selenium import webdriver


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # User opens to-do app
        self.browser.get('http://localhost:8000/')

        # He notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        self.fail('Forcing current test to fail!')

        # User invited to enter a to-do item straight away

        # He types "Buy peacock feathers into a text box

        # When he hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list

        # There is still a text box inviting him to add another item
        # He types "Use peacock feathers to make a fly"

        # The page updates again and now shows both items in list

        # User checks whether the site will remember his list
        # There is a text bar that has a unique URL for created to-do list with some explanatory text

        # He visits that URL, to-do list is still here


if __name__ == '__main__':
    unittest.main()
