from django.shortcuts import render


def home_page(request):
    context = {}
    if request.method == 'POST':
        new_item_text = request.POST.get('item_text', '')
        context['new_item_text'] = new_item_text
    return render(request, 'home.html', context)
