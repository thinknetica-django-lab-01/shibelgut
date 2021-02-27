from ecomm.models import Good, Category


g1 = Good(name='Laptop', price=1230, description='New model of laptop',
          rating=4, brand='Sony', is_available=True)
g1.id
g1.name
# 'Laptop'
g1.is_available
# True
g1.brand
# 'Sony'
g1.save()
g1.id
# 1
g2 = Good.objects.create(name='Headphone', price=22,
                         description='Wireless headphone', rating=5,
                         brand='Xiaomi', is_available=True)
g2.id
# 2
g1
# <Good: Laptop>
g2
# <Good: Headphone>
good = Good.objects.get(brand='Xiaomi')
good
# <Good: Headphone>
good = Good.objects.get(brand__iexact='xiaomi')
good
# <Good: Headphone>
good = Good.objects.filter(description__contains='wireless')
good
# <QuerySet [<Good: Headphone>]>
cat1 = Category(name='Electronic')
cat1
# <Category: Electronic>
cat1.id
cat1.save()
cat1.id
# 1
cat2 = Category.objects.create(name='Domestic appliances')
cat2.id
# 2
g1.categories.add(cat1)
g1.categories.all()
# <QuerySet [<Category: Electronic>]>
cat1.goods.all()
# <QuerySet [<Good: Laptop>]>
g2.categories.add(cat1)
g2.categories.all()
# <QuerySet [<Category: Electronic>]>
g1 = Good(name='Refrigerator', price=599.99,
          description='Refrigerator with new sytem NoFrost',
          rating=3, brand='Samsung', is_available=True)
g1
# <Good: Refrigerator>
g1.name
# 'Refrigerator'
g1.id
g1.save()
g1.id
# 4
cat3 = Category.objects.get(name__contains='domestic')
cat3.id
# 2
g1.categories.add(cat3)
g1.categories.all()
# <QuerySet [<Category: Domestic appliances>]>
g1
# <Good: Refrigerator>
good = Good.objects.all()
good
# <QuerySet [<Good: Laptop>, <Good: Headphone>, <Good: TV>, <Good: Refrigerator>]>
category = Category.objects.all()
category
# <QuerySet [<Category: Electronic>, <Category: Domestic appliances>]>
good_tv = Good.objects.get(name__iexact='tv')
good_tv
# <Good: TV>
good_tv.id
# 3
good_tv.categories.all()
# <QuerySet []>
cat1 = Category.objects.get(name__contains='electronic')
cat1.id
# 1
good_tv.categories.add(cat1)
good_tv.categories.all()
# <QuerySet [<Category: Electronic>]>
Good.objects.values()
# <QuerySet [{'id': 1, 'name': 'Laptop', 'price': Decimal('1230.00'),
# 'description': 'New model of laptop', 'rating': 4, 'brand': 'Sony',
# 'is_available': True},
# {'id': 2, 'name': 'Headphone', 'price': Decimal('22.00'),
# 'description': 'Wireless headphone', 'rating': 5, 'brand': 'Xiaomi',
# 'is_available': True},
# {'id': 3, 'name': 'TV', 'price': Decimal('799.99'),
# 'description': 'Screen diagonal is 120 inches', 'rating': 4, 'brand': 'LG',
# 'is_available': False},
# {'id': 4, 'name': 'Refrigerator', 'price': Decimal('599.99'),
# 'description': 'Refrigerator with new sytem NoFrost', 'rating': 3,
# 'brand': 'Samsung', 'is_available': True}]>
Good.objects.filter(categories__name__iexact='electronic')
# <QuerySet [<Good: Laptop>, <Good: Headphone>, <Good: TV>]>
Good.objects.filter(categories__name__contains='domestic')
# <QuerySet [<Good: Refrigerator>]>
