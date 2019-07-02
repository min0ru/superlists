from django.shortcuts import render, redirect
from lists.models import Item, List


def home_page(request):
    return render(request, 'home.html')


def new_list(request):
    if request.method == 'POST':
        created_list = List.objects.create()
        Item.objects.create(
            text=request.POST.get('item_text'),
            list=created_list)
    return redirect('/lists/the-only-list-in-the-world/')


def view_list(request):
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})
