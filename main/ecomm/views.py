from django.shortcuts import render


def index(request):
    context = {}
    return render(request, 'ecomm/index.html', context=context)
