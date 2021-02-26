from django.test import TestCase
from django.urls import resolve

from ecomm.models import Category, Characteristic, CustomUser, Good, Image, Seller, Tag, User


class GoodsListViewTest(TestCase):

    def setUp(self) -> None:
        self.category = Category.objects.create(title='test_category')
        self.tag = Tag.objects.create(title='test_tag', category=self.category)
        self.user = User.objects.create_user(username='test_user')
        self.customuser = CustomUser.objects.get(id=self.user.id)
        self.seller = Seller.objects.create(customuser=self.customuser)

        number_of_goods = 13
        for good_num in range(number_of_goods):
            Good.objects.create(title=f'good {good_num}', price=1, quantity=(-1 + good_num),
                                tag=self.tag, seller=self.seller)

    def test_view_url_exists_at_desired_locations(self):
        resp = self.client.get('/goods/')
        self.assertEqual(resp.status_code, 200)

    def test_url_resolve_has_right_name(self):
        resp = resolve('/goods/')
        self.assertEqual(resp.view_name, 'goods_list_url')

    def test_view_uses_correct_template(self):
        resp = self.client.get('/goods/')
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'ecomm/good_list.html')

    def test_pagination_is_ten(self):
        resp = self.client.get('/goods/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] is True)
        self.assertTrue(len(resp.context['object_list']) == 10)

    def test_lists_all_goods(self):
        resp = self.client.get('/goods/' + '?tag=&page=2')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] is True)
        self.assertTrue(len(resp.context['object_list']) == 3)


class GoodsDetailViewTest(TestCase):

    def setUp(self) -> None:
        self.category = Category.objects.create(title='test_category')
        self.tag = Tag.objects.create(title='test_tag', category=self.category)
        self.user = User.objects.create_user(username='test_user')
        self.customuser = CustomUser.objects.get(id=self.user.id)
        self.seller = Seller.objects.create(customuser=self.customuser)
        self.test_good = Good.objects.create(title='test_good', price=1,
                                             quantity=1, tag=self.tag, seller=self.seller)
        self.characteristic = Characteristic.objects.create(good=self.test_good)
        self.image = Image.objects.create(good=self.test_good)

    def test_view_url_exists_at_desired_locations(self):
        resp = self.client.get(f'/goods/{self.test_good.id}/')
        self.assertEqual(resp.status_code, 200)

    def test_counter_is_represented(self):
        resp = self.client.get(f'/goods/{self.test_good.id}/')
        self.assertTrue(resp.context['counter'] != 0)
