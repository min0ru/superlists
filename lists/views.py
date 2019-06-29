from django.shortcuts import render, HttpResponse


def home_page(request):
    return HttpResponse('<html><head><title>To-Do lists</title></html>')

