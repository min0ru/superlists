from django.test import TestCase
from lists.models import Item


class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]

        self.assertEqual(first_saved_item.text, first_item.text)
        self.assertEqual(second_saved_item.text, second_item.text)


class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_POST_request(self):
        test_item_text = 'A new list item'
        self.client.post('/', data={'item_text': test_item_text})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, test_item_text)

    def test_redirect_after_POST(self):
        test_item_text = 'A new list item'
        response = self.client.post('/', data={'item_text': test_item_text})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.get('location'), '/')

    def test_only_saves_items_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)

    def test_displays_all_list_items(self):
        test_items = ['Item 1', 'Item 2', 'Item 3']

        for item in test_items:
            Item.objects.create(text=item)

        response = self.client.get('/')

        for item in test_items:
            self.assertIn(item, response.content.decode())
