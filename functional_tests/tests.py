from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
import time

MAX_WAIT_SECONDS = 4


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

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # First user starts a new to-do list
        self.browser.get(self.live_server_url)
        first_user_todo_text = 'Buy peacock feathers'
        self.post_new_item(first_user_todo_text)
        self.wait_for_row_in_list_table(f'1: {first_user_todo_text}')

        # First user notices that his list has a unique URL
        first_user_list_url = self.browser.current_url
        self.assertRegex(first_user_list_url, '/lists/.+')

        # Second user comes to the site

        ## We use a new browser session to make sure that no information
        ## of the previous user is coming from cookies etc
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Second user visits home page
        # There is no sign of previous user information
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn(first_user_todo_text, page_text)

        # Second user starts a new list by entering a new item
        second_user_todo_text = 'Buy milk'
        self.post_new_item(second_user_todo_text)
        self.wait_for_row_in_list_table(f'1: {second_user_todo_text}')

        # Second user gets his own unique URL
        second_user_url = self.browser.current_url
        self.assertRegex(second_user_url, '/lists/.+')
        self.assertNotEqual(first_user_list_url, second_user_url)

        # Again, there is no trace of first user's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn(first_user_todo_text, page_text)
        self.assertIn(second_user_todo_text, page_text)

    def test_layout_and_styling(self):
        # User is visiting home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 786)

        # He notices that input box is centered
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            self.browser.get_window_size()['width'] / 2,
            delta=10
        )

        # He starts a new list and sees that input is centered there too
        item_text = 'testing'
        self.post_new_item(item_text)
        self.wait_for_row_in_list_table(f'1: {item_text}')

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            self.browser.get_window_size()['width'] / 2,
            delta=10
        )

