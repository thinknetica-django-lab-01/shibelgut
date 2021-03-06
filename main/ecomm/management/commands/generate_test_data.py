from random import choice, randint

from django.contrib.auth.models import Permission, User
from django.core.management.base import BaseCommand, CommandError

from ecomm.models import Category, Characteristic, CustomUser, Good, Image, Seller, Tag


NUMBER_CATEGORIES = 1


class Command(BaseCommand):
    help = 'Create test data for models of ecomm project'

    def add_arguments(self, parser):
        parser.add_argument(
            '--num_tags',
            type=int,
            help='Indicates the number of tags to be created'
        )
        parser.add_argument(
            '--num_sellers',
            type=int,
            help='Indicates the number of sellers to be created'
        )
        parser.add_argument(
            '--num_goods',
            type=int,
            help='Indicates the number of goods to be created'
        )

    def handle(self, *args, **options):
        try:
            num_tags = int(options['num_tags'])
            num_sellers = int(options['num_sellers'])
            num_goods = int(options['num_goods'])
        except ValueError as err:
            raise CommandError(self.style.ERROR('Error of command parsing: %s' % str(err)))

        num_categories = NUMBER_CATEGORIES if num_tags <= 3 else num_tags // 3
        num_users = num_sellers * 4
        # num_customers = num_users - num_sellers

        permissions = [
            Permission.objects.get(codename='add_good'),
            Permission.objects.get(codename='change_good'),
            Permission.objects.get(codename='view_good'),
        ]

        categories = [
            Category.objects.get_or_create(
                title=f'test_category_{i}')[0]
            for i in range(1, num_categories + 1)
        ]

        tags = [
            Tag.objects.get_or_create(
                title=f'test_tag_{i}',
                category=choice(categories))[0]
            for i in range(1, num_tags + 1)
        ]

        users = [
            User.objects.create_user(
                username=f'test_user_{i}',
                email=f'test_user_{i}@gmail.com',
                password='12345')
            for i in range(1, num_users + 1)
        ]

        customusers = [CustomUser.objects.get(user=user) for user in users]

        sellers = [Seller.objects.create(customuser=customuser) for customuser in customusers]

        # sellers = []
        # for _ in range(num_sellers):
        #     random_customuser = choice(customusers)
        #     seller = Seller.objects.create(customuser=random_customuser)
        #     sellers.append(seller)
        #     # customusers.remove(random_customuser)

        # customers = [
        #     Customer.objects.create(customuser=customuser)
        #     for customuser in customusers
        # ]

        for seller in sellers:
            seller.customuser.user.user_permissions.add(permissions[0])
            seller.customuser.user.user_permissions.add(permissions[1])
            seller.save()

        for i in range(1, num_goods + 1):
            good = Good.objects.create(
                title=f'test good {i}',
                price=randint(10, 1000),
                quantity=randint(1, 20),
                tag=choice(tags),
                seller=choice(sellers)
            )
            Characteristic.objects.create(good=good)
            Image.objects.create(good=good)

            self.stdout.write(self.style.SUCCESS('Good \'%s\' was successfully created' % str(good)))
