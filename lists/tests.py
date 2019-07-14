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
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')

    def test_redirect_GET_to_home(self):
        response = self.client.get('/lists/new')
        self.assertRedirects(response, '/')


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        new_list = List.objects.create()
        response = self.client.get(f'/lists/{new_list.id}/')
        self.assertTemplateUsed(response, 'list.html')

    def test_passes_correct_list_to_template(self):
        List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        first_correct_item = Item.objects.create(text='First list First item', list=correct_list)
        second_correct_item = Item.objects.create(text='First list Second item', list=correct_list)

        wrong_list = List.objects.create()
        first_wrong_item = Item.objects.create(text='Second list First item', list=wrong_list)
        second_wrong_item = Item.objects.create(text='Second list Second item', list=wrong_list)

        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertContains(response, first_correct_item.text)
        self.assertContains(response, second_correct_item.text)

        self.assertNotContains(response, first_wrong_item.text)
        self.assertNotContains(response, second_wrong_item.text)


class NewItemTest(TestCase):

    def test_can_save_a_POST_request_to_an_existing_list(self):
        List.objects.create()
        correct_list = List.objects.create()

        item_text = 'A new item for correct list'
        self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text': item_text}
        )

        item_count = Item.objects.count()
        self.assertEqual(item_count, 1)

        item = Item.objects.first()
        self.assertEqual(item.text, item_text)

        self.assertEqual(item.list, correct_list)

    def test_redirects_to_list_view(self):
        List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text': 'A new item for an existing list'}
        )

        self.assertRedirects(response, f'/lists/{correct_list.id}/')
