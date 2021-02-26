from django.test import TestCase
from ecomm.models import Category, Tag, Good, User, CustomUser, Seller
from django.core.exceptions import ValidationError


class GoodModelTest(TestCase):

    def setUp(self) -> None:
        self.category = Category.objects.create(title='test_category')
        self.tag = Tag.objects.create(title='test_tag', category=self.category)
        self.user = User.objects.create(username='test_user')
        self.customuser = CustomUser.objects.get(id=self.user.id)
        self.seller = Seller.objects.create(customuser=self.customuser)

    def test_cannot_save_empty_good_name(self):
        good = Good(price=10, quantity=1, tag=self.tag, seller=self.seller)
        with self.assertRaises(ValidationError):
            good.save()
            good.full_clean()

    def test_good_related_with_tag(self):
        good = Good(title='test_name', price=10, quantity=1, seller=self.seller)
        good.tag = self.tag
        good.save()
        self.assertIn(good, self.tag.goods.all())

    def test_string_representation(self):
        good = Good.objects.create(
            title='test_good',
            price=10,
            quantity=1,
            tag=self.tag,
            seller=self.seller
        )
        self.assertEqual(str(good), 'test_good')

    def test_get_absolute_url(self):
        good = Good.objects.create(
            title='test_name',
            price=10,
            quantity=0,
            tag=self.tag,
            seller=self.seller
        )
        self.assertEquals(good.get_absolute_url(), '/goods/1/')

    def test_good_is_available(self):
        good = Good.objects.create(
            title='test_name',
            price=10,
            quantity=1,
            tag=self.tag,
            seller=self.seller
        )
        self.assertEqual(good.is_available, True if good.quantity else False)


class CustomUserModelTest(TestCase):

    def test_CustomUser_post_save(self):
        user = User.objects.create_user(username='test_user')
        customuser = CustomUser.objects.first()
        self.assertEqual(user.id, customuser.id)

    def test_CustomUser_string_representation(self):
        User.objects.create_user(username='test_user')
        customuser = CustomUser.objects.first()
        self.assertEqual(str(customuser.user), 'test_user')

