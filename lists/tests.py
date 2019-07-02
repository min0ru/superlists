from django.test import TestCase
from lists.models import Item, List


class ListModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        new_list = List.objects.create()
        first_item = Item.objects.create(text='First item', list=new_list)
        second_item = Item.objects.create(text='Second item', list=new_list)

        saved_list = List.objects.first()
        self.assertEqual(new_list, saved_list)

        saved_items = Item.objects.all().order_by('id')
        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]

        self.assertEqual(first_saved_item.list, new_list)
        self.assertEqual(second_saved_item.list, new_list)

        self.assertEqual(first_saved_item.text, first_item.text)
        self.assertEqual(second_saved_item.text, second_item.text)


class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


class NewListTest(TestCase):

    def test_can_save_a_POST_request(self):
        test_item_text = 'A new list item'
        self.client.post('/lists/new', data={'item_text': test_item_text})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, test_item_text)

    def test_redirect_after_POST(self):
        response = self.client.post('/lists/new', data={'item_text': 'Some item text'})
        self.assertRedirects(response, '/lists/the-only-list-in-the-world/')


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_all_items(self):
        test_items = ['Item 1', 'Item 2', 'Item 3']

        test_list = List.objects.create()

        for item in test_items:
            Item.objects.create(text=item, list=test_list)

        response = self.client.get('/lists/the-only-list-in-the-world/')

        for item in test_items:
            self.assertContains(response, item)
