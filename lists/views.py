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
    return redirect(f'/lists/{created_list.id}/')


def view_list(request, list_id):
    selected_list = List.objects.get(id=list_id)
    items = Item.objects.filter(list_id=list_id)
    return render(request, 'list.html', {'list': selected_list})


def add_item(request, list_id):
    if request.method == 'POST':
        Item.objects.create(
            text=request.POST.get('item_text'),
            list=List.objects.get(id=list_id)
        )
    return redirect(f'/lists/{list_id}/')
