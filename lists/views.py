from django.shortcuts import render, redirect
from lists.models import Item


def home_page(request):
    if request.method == 'POST':
        new_item_text = request.POST.get('item_text', '')

        new_item = Item()
        new_item.text = new_item_text
        new_item.save()

        return redirect('/')

    context = {}
    return render(request, 'home.html', context)
