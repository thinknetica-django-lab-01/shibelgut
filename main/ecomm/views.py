from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from ecomm.models import Good, CustomUser, Image, Characteristic
from ecomm.forms import *
from django.views.generic.edit import UpdateView, CreateView
from django.forms import inlineformset_factory


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
        context['current_username'] = self.request.user

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        characteristics = Characteristic.objects.get(good_id=self.kwargs.get('pk'))
        images = Image.objects.get(good_id=self.kwargs.get('pk'))
        context['characteristic'] = characteristics
        context['image'] = images
        context['current_username'] = self.request.user

        return context


class ProfileUserUpdate(UpdateView):
    model = CustomUser
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


class GoodCreateView(CreateView):
    model = Good
    form_class = GoodCreateForm
    template_name = 'ecomm/good_create.html'
    success_url = '/goods/add/'

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        characteristic_form = CharacteristicFormset()
        image_form = ImageFormset()

        return self.render_to_response(self.get_context_data(
            form=form, characteristic_form=characteristic_form, image_form=image_form))

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        characteristic_form = CharacteristicFormset(self.request.POST)
        image_form = ImageFormset(self.request.POST)

        if form.is_valod() and characteristic_form.is_valid() and image_form.is_valid():
            return self.form_valid(form, characteristic_form, image_form)

        return self.form_valid(form, characteristic_form, image_form)

    def form_valid(self, form, characteristic_form, image_form):
        self.object = form.save()
        characteristic_form.instance = self.object
        characteristic_form.save()
        image_form.instance = self.object
        image_form.save()

        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(GoodCreateView, self).get_context_data(**kwargs)
        characteristic_formhelper = CharacteristicFormHelper()
        image_formhelper = ImageFormHelper()

        if self.request.POST:
            context['form'] = GoodCreateForm(self.request.POST)
            context['characteristic_form'] = CharacteristicFormset(self.request.POST)
            context['characteristic_formhelper'] = characteristic_formhelper
            context['image_form'] = ImageFormset(self.request.POST)
            context['image_formhelper'] = image_formhelper
        else:
            context['form'] = GoodCreateForm()
            context['characteristic_form'] = CharacteristicFormset()
            context['characteristic_formhelper'] = characteristic_formhelper
            context['image_form'] = ImageFormset()
            context['image_formhelper'] = image_formhelper

        context['current_username'] = self.request.user

        return context


class GoodUpdateView(UpdateView):
    model = Good
    form_class = GoodUpdateForm
    template_name = 'ecomm/good_update.html'
    success_url = '/goods/<int:pk>/edit/'

    def get_context_data(self, **kwargs):
        context = super(GoodUpdateView, self).get_context_data(**kwargs)

        if pk := self.kwargs['pk']:
            good = get_object_or_404(Good, pk=pk)
        else:
            good = Good()

        good_form = GoodUpdateForm(instance=good)
        CharacteristicFormset = inlineformset_factory(Good, Characteristic, exclude=('good',), can_delete=False, max_num=5)
        ImageFormset = inlineformset_factory(Good, Image, exclude=('good',), can_delete=False, max_num=5)
        characteristic_formset = CharacteristicFormset(instance=good)
        image_formset = ImageFormset(instance=good)

        if self.request.method == 'POST':
            good_form = GoodUpdateForm(self.request.POST)

            if pk:
                good_form = GoodUpdateForm(self.request.POST, instance=good)

            characteristic_formset = CharacteristicFormset(self.request.POST, self.request.FILES)
            image_formset = ImageFormset(self.request.POST, self.request.FILES)

            if good_form.is_valid():
                created_good = good_form.save(commit=False)
                characteristic_formset = CharacteristicFormset(self.request.POST, self.request.FILES, instance=created_good)
                image_formset = ImageFormset(self.request.POST, self.request.FILES, instance=created_good)

                if characteristic_formset.is_valid() and image_formset.is_valid():
                    created_good.save()
                    characteristic_formset.save()
                    image_formset.save()

                    return redirect(created_good.get_absolute_url())

        context = {
            'good_form': good_form,
            'characteristic_formset': characteristic_formset,
            'image_formset': image_formset,
            'good_id': good.id,
            'current_username': self.request.user
        }

        return context

