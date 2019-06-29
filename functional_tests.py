from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest


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
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # User invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # He types "Buy peacock feathers" into a text box
        todo_1_text = 'Buy peacock feathers'
        inputbox.send_keys(todo_1_text)

        # When he hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == todo_1_text for row in rows)
        )

        # There is still a text box inviting him to add another item
        # He types "Use peacock feathers to make a fly"
        self.fail('Finish the test!')

        # The page updates again and now shows both items in list

        # User checks whether the site will remember his list
        # There is a text bar that has a unique URL for created to-do list with some explanatory text

        # He visits that URL, to-do list is still here


if __name__ == '__main__':
    unittest.main()
