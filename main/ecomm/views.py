from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import Group, Permission
from django.core.cache import cache
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView
from main.settings import EMAIL_HOST_USER

from ecomm.forms import *
from ecomm.models import Characteristic, CustomUser, Good, Image, Seller, Subscriber
from ecomm.tasks import send_email_new_goods


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


# @method_decorator(cache_page(60 * 5), name='dispatch')
class GoodsDetailView(DetailView):
    context_object_name = 'goods'
    queryset = Good.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        self.object.counter += 1
        self.object.save()
        characteristics = Characteristic.objects.get(good_id=self.kwargs.get('pk'))
        images = Image.objects.get(good_id=self.kwargs.get('pk'))
        counter = cache.get_or_set(f'{self.object.pk}_counter', self.object.counter, 60)
        context['characteristic'] = characteristics
        context['image'] = images
        context['current_username'] = self.request.user
        context['counter'] = counter
        return context


@method_decorator(login_required, name='dispatch')
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
        return super(ProfileUserUpdate, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class GoodCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'ecomm.add_good'
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
        # characteristic_form = CharacteristicFormset(self.request.POST)
        # image_form = ImageFormset(self.request.POST)

        if form.is_valid():
            return self.form_valid(form)

        return self.form_valid(form)

    def form_valid(self, form):
        self.object = form.save()
        # characteristic_form.instance = self.object
        # characteristic_form.save()
        # image_form.instance = self.object
        # image_form.save()

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


@method_decorator(login_required, name='dispatch')
class GoodUpdateView(PermissionRequiredMixin, UserPassesTestMixin, UpdateView):
    permission_required = 'ecomm.change_good'
    model = Good
    form_class = GoodUpdateForm
    template_name = 'ecomm/good_update.html'
    success_url = '/goods/<int:pk>/edit/'

    def test_func(self):
        return self.request.user.id == self.get_object().seller_id

    def get_context_data(self, **kwargs):
        context = super(GoodUpdateView, self).get_context_data(**kwargs)

        good = get_object_or_404(Good, pk=self.kwargs.get('pk'))

        good_form = GoodUpdateForm(instance=good)
        CharacteristicFormset = inlineformset_factory(
            Good, Characteristic, exclude=('good',), can_delete=False, max_num=5
        )
        ImageFormset = inlineformset_factory(
            Good, Image, exclude=('good',), can_delete=False, max_num=5
        )
        characteristic_formset = CharacteristicFormset(instance=good)
        image_formset = ImageFormset(instance=good)

        if self.request.method == 'POST':
            good_form = GoodUpdateForm(self.request.POST)

            if self.get_object():
                good_form = GoodUpdateForm(self.request.POST, instance=good)

            characteristic_formset = CharacteristicFormset(self.request.POST, self.request.FILES)
            image_formset = ImageFormset(self.request.POST, self.request.FILES)

            if good_form.is_valid():
                created_good = good_form.save(commit=False)
                characteristic_formset = CharacteristicFormset(
                    self.request.POST, self.request.FILES, instance=created_good
                )
                image_formset = ImageFormset(
                    self.request.POST, self.request.FILES, instance=created_good
                )

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


def send_confirmation_email(recipient_email, context):
    template = loader.get_template(template_name='ecomm/emails/signup_success.html')
    html_content = template.render(context=context)
    msg = EmailMultiAlternatives(
        subject='Confirm your email',
        body=html_content,
        from_email=EMAIL_HOST_USER,
        to=[recipient_email])
    msg.content_subtype = 'html'
    msg.send()


def create_common_users_group():
    common_users_group, created = Group.objects.get_or_create(name='Common Users')
    if created:
        common_users_group.permissions.add(
            Permission.objects.get(codename__icontains='view_good')
        )

    return common_users_group


@receiver(post_save, sender=User)
def create_user(sender, instance, created, **kwargs):
    if created:
        instance.groups.add(create_common_users_group())

        send_confirmation_email([instance.email, ], {'recipient_email': instance.email})


@receiver(post_save, sender=Good)
def create_new_goods(sender, instance, created, **kwargs):
    if created:
        goods = Good.objects.get(pk=instance.id)
        send_email_new_goods.delay(goods.title)


@receiver(post_save, sender=Seller)
def create_seller(sender, instance, **kwargs):
    sellers_group, created = Group.objects.get_or_create(name='Sellers')
    instance.customuser.user.groups.add(sellers_group)
    if created:
        permissions_queryset = Permission.objects.filter(
            codename__icontains='good').exclude(codename__icontains='delete_good')
        sellers_group.permissions.set(permissions_queryset)


def send_subscription_email(recipient_email, context):
    template = loader.get_template(template_name='ecomm/emails/goods_subscription.html')
    html_content = template.render(context=context)
    msg = EmailMultiAlternatives(
        subject='Subscription to new goods',
        body=html_content,
        from_email=EMAIL_HOST_USER,
        to=[recipient_email])
    msg.content_subtype = 'html'
    msg.send()


@login_required
def get_subscription(request):
    form = SubscriptionForm()

    context = {
        'form': form,
        'current_username': request.user
    }

    if User.objects.filter(user__is_subscribed=True, id=request.user.id):
        context['is_subscribed'] = True
    else:
        if request.method == 'POST':
            form = SubscriptionForm(request.POST)
            if form.is_valid():
                subscriber, created = Subscriber.objects.get_or_create(user=request.user)
                if created:
                    send_subscription_email(request.user.email, {'username': request.user.username})
                    subscriber.is_subscribed = True
                    subscriber.save()
                    return render(request, 'ecomm/subscription_success.html')

    return render(request, 'ecomm/subscription.html', context)


@method_decorator(login_required, name='dispatch')
class SellerCreateView(CreateView):
    model = Seller
    form_class = SellerCreateForm
    template_name = 'ecomm/profile_seller.html'
    success_url = '/accounts/profile/seller/'

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            return self.form_valid(form)

        return self.form_valid(form)

    def form_valid(self, form):
        self.object = form.save()

        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(SellerCreateView, self).get_context_data(**kwargs)

        if self.request.POST:
            context['form'] = SellerCreateForm(self.request.POST)
            seller = Seller.objects.get(id=self.request.user.id)
            create_seller(Seller, seller)
            context['is_seller'] = True
        else:
            context['form'] = SellerCreateForm()

        context['current_username'] = self.request.user

        return context


# @sensitive_post_parameters()
# @csrf_protect
# @never_cache
# def user_login(request):
#
#     redirect_to = ''
#
#     if request.GET:
#         redirect_to = request.GET['next']
#
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             clean_data = form.cleaned_data
#             try:
#                 user = User.objects.get(email__iexact=clean_data['email'])
#             except User.DoesNotExist:
#                 messages.error(request, 'User does not exist!')
#                 if redirect_to == '':
#                     return redirect(settings.LOGIN_REDIRECT_URL, messages)
#                 return redirect(redirect_to, messages)
#             else:
#                 if user.is_active:
#                     if user.check_password(clean_data['password']):
#                         auth_login(request, user,
#                                    backend='django.contrib.auth.backends.ModelBackend')
#                         if redirect_to == '':
#                             return redirect('/')
#                         return redirect(redirect_to)
#
#                     messages.error(request, 'Invalid password!')
#                     if redirect_to == '':
#                         return redirect(settings.LOGIN_REDIRECT_URL, messages)
#                     return redirect(redirect_to, messages)
#
#                 messages.error(request, 'User is blocked!')
#                 if redirect_to == '':
#                     return redirect(settings.LOGIN_REDIRECT_URL, messages)
#                 return redirect(redirect_to, messages)
#
#     form = LoginForm()
#
#     return render(request, 'ecomm/login.html', {'form': form})
#
#
# def user_logout(request):
#     auth_logout(request)
#     return redirect('/')
