from django.shortcuts import render
from django.views.generic import ListView, DetailView
from ecomm.models import Good
from ecomm.forms import ProfileUserForm
from django.views.generic.edit import UpdateView


def index(request):
    turn_on_block = False
    current_username = request.user
    simple_string = 'Hello, world!'
    return render(request, 'ecomm/index.html', context={'turn_on_block': turn_on_block,
                                                        'current_username': current_username,
                                                        'simple_string': simple_string})


class GoodsListView(ListView):
    paginate_by = 10
    model = Good
    template_name = 'ecomm/good_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        goods = Good.objects.all()
        tags_list = []
        for good in goods:
            tags_list.append(good.tag.title)
        context['tags'] = list(set(tags_list))
        context['current_tag'] = self.request.GET.get('tag') if self.request.GET.get('tag') else ''

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        if tag_name := self.request.GET.get('tag'):
            tag_name = tag_name.replace('_', ' ')
            queryset = Good.objects.filter(tag__title__icontains=tag_name)

        return queryset


class GoodsDetailView(DetailView):
    context_object_name = 'goods'
    queryset = Good.objects.all()


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

