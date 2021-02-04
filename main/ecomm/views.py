from django.shortcuts import render
from django.views.generic import ListView, DetailView
from ecomm.models import Good, User
from ecomm.forms import ProfileUserForm
from django.core.paginator import Paginator
from django.views.generic.edit import UpdateView


def index(request):
    turn_on_block = False
    current_username = request.user
    simple_string = 'Hello, world!'
    return render(request, 'ecomm/index.html', context={'turn_on_block': turn_on_block,
                                                        'current_username': current_username,
                                                        'simple_string': simple_string})


class GoodsListView(ListView):
    context_object_name = 'goods_list'
    paginate_by = 10
    queryset = Good.objects.all()
    template_name = 'ecomm/good_list.html'

    def get_context_data(self, **kwargs):
        context = super(GoodsListView, self).get_context_data(**kwargs)
        goods = Good.objects.all()
        tags_list = []
        for good in goods:
            tags_list.append(good.tag.title)
        tags_list = list(set(tags_list))

        if self.request.GET.get('tag'):
            tag_search = self.request.GET.get('tag').replace('_', ' ')
            context['tag_search'] = tag_search
            print(tag_search)
            goods = Good.objects.filter(tag__title__icontains=tag_search)
            print(goods)

        paginator = Paginator(goods, self.paginate_by)
        page_number = self.request.GET.get('page', 1)
        page = paginator.get_page(page_number)

        is_paginated = page.has_other_pages()
        if page.has_previous():
            prev_url = '?page={}'.format(page.previous_page_number())
        else:
            prev_url = ''

        if page.has_next():
            next_url = '?page={}'.format(page.next_page_number())
        else:
            next_url = ''

        current_username = self.request.user

        context = {
            'page_object': page,
            'tags_list': tags_list,
            'is_paginated': is_paginated,
            'next_url': next_url,
            'prev_url': prev_url,
            'current_username': current_username,
        }
        return context


class GoodsDetailView(DetailView):
    context_object_name = 'goods'
    queryset = Good.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_username'] = self.request.user
        context['goods_list'] = Good.objects.all()
        return context


class ProfileUserUpdate(UpdateView):
    model = User
    form_class = ProfileUserForm
    template_name = 'ecomm/profile_update.html'
    success_url = '/accounts/profile/'

    def get_context_data(self, **kwargs):
        context = super(ProfileUserUpdate, self).get_context_data(**kwargs)
        context['current_username'] = self.request.user
        return context

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        clean = form.cleaned_data
        context = {}
        return super(ProfileUserUpdate, self).form_valid(form)

