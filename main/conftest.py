import pytest
from ecomm.models import Good, Characteristic, Image, Tag, Category, User, CustomUser, Seller
from django.contrib.auth.models import Permission
from django.db.models import Q


@pytest.fixture(autouse=True)
def enable_db_access_for_all_test(db):
    pass


@pytest.fixture()
def user(django_user_model):
    user = User.objects.create(
        username='test_user',
        email='test_user@m.ru',
        password='12345'
    )
    permissions = Permission.objects.get(codename='view_good')
    user.user_permissions.add(permissions)
    return user


@pytest.fixture()
def category():
    return Category.objects.create(title='test_category')


@pytest.fixture()
def tag(category):
    return Tag.objects.create(title='test_tag', category=category)


@pytest.fixture()
def customuser(user):
    return CustomUser.objects.get(user=user)


@pytest.fixture()
def seller(customuser):
    seller = Seller.objects.create(customuser=customuser)
    permissions_list = list(Permission.objects.filter(Q(codename='add_good') & Q(codename='change_good')))
    for permission in permissions_list:
        seller.customuser.user.user_permissions.add(permission)
    seller.save()
    return seller


@pytest.fixture()
def good(tag, seller):
    good = Good(
        title='test_good',
        price=10,
        quantity=1,
        tag=tag,
        seller=seller,
    )
    good.save()
    good.characteristics = Characteristic.objects.create(good=good)
    good.images = Image.objects.create(good=good)
    return good

