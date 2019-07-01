from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
import time

MAX_WAIT_SECONDS = 10


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(
                    row_text,
                    [row.text for row in rows]
                )
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT_SECONDS:
                    raise e
                time.sleep(0.1)

    def post_new_item(self, item_text):
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys(item_text)
        inputbox.send_keys(Keys.ENTER)

    def test_can_start_a_list_and_retrieve_it_later(self):
        # User opens to-do app
        self.browser.get(self.live_server_url)

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
        self.post_new_item(todo_1_text)

        # When he hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list
        self.wait_for_row_in_list_table(f'1: {todo_1_text}')

        # There is still a text box inviting him to add another item
        # He types "Use peacock feathers to make a fly"
        todo_2_text = 'Use peacock feathers to make a fly'
        self.post_new_item(todo_2_text)

        # The page updates again and now shows both items in list
        self.wait_for_row_in_list_table(f'1: {todo_1_text}')
        self.wait_for_row_in_list_table(f'2: {todo_2_text}')

        # User checks whether the site will remember his list
        # There is a text bar that has a unique URL for created to-do list with some explanatory text

        # He visits that URL, to-do list is still here

        # FT is unfinished yet
        self.fail('FT should fail here because it\'s not finished yet!')
