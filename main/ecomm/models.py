from django.db import models


class Seller(models.Model):
    name = models.CharField(max_length=150, unique=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.name)


class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return '{}'.format(self.name)


class Tag(models.Model):
    name = models.CharField(max_length=150, unique=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.name)


class Good(models.Model):
    name = models.CharField(max_length=150, unique=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, db_index=True)
    description = models.TextField(max_length=500)
    rating = models.PositiveIntegerField(db_index=True)
    brand = models.CharField(max_length=150, db_index=True)
    is_available = models.BooleanField(db_index=True)
    categories = models.ManyToManyField('Category', blank=True, related_name='goods')

    def __str__(self):
        return '{}'.format(self.name)

    def __init__(self, percent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__percentage = percent
        self.__order_percentage = None

    @property
    def percentage(self):
        return self.__percentage

    @percentage.setter
    def percentage(self, value):
        self.__percentage = value
        self.__order_percentage = None

    @property
    def order_percentage(self):
        if self.__order_percentage is None:
            self.__order_percentage = round((self.__percentage * self.price)/100, 2)
        return self.__order_percentage


class Customer(models.Model):
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=150)
    name = models.CharField(max_length=150, db_index=True)
    phone = models.CharField(max_length=150, unique=True)
    age = models.IntegerField(db_index=True)
    country = models.CharField(max_length=150, db_index=True)
    city = models.CharField(max_length=150, db_index=True)
    address = models.CharField(max_length=150, db_index=True)
    goods = models.ManyToManyField('Good', blank=True, related_name='customers')

    def __str__(self):
        return 'Email: {}, name: {}'.format(self.email, self.name)

