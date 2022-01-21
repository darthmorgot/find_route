from django.shortcuts import render


def home(request):
    context = {
        'title': 'Test page',
        'name': 'John',
    }
    return render(request, 'home.html', context=context)
