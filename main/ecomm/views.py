from django.shortcuts import render


def index(request):
    turn_on_block = True
    current_username = request.user
    return render(request, 'ecomm/index.html', context={'turn_on_block': turn_on_block, 'current_username': current_username})
