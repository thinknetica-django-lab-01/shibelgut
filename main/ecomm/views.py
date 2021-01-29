from django.shortcuts import render
from django.views.generic import ListView, DetailView
from ecomm.models import Good


def index(request):
    turn_on_block = True
    current_username = request.user
    simple_string = 'Hello, world!'
    return render(request, 'ecomm/index.html', context={'turn_on_block': turn_on_block,
                                                        'current_username': current_username,
                                                        'simple_string': simple_string})


class GoodsList(ListView):
    model = Good
    context_object_name = 'goods_list'


class GoodsDetail(DetailView):
    context_object_name = 'goods'
    queryset = Good.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['goods_list'] = Good.objects.all()
        return context
