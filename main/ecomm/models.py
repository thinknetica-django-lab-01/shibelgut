from django.db import models
from django.shortcuts import reverse
from datetime import datetime, date


class Category(models.Model):
    title = models.CharField(default='default title', max_length=150, verbose_name='Наименование категории',
                             blank=False, db_index=True)

    def __str__(self):
        return '{}'.format(self.title)

    class Meta:
        ordering = ['title']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Tag(models.Model):
    title = models.CharField(default='default title', max_length=150, verbose_name='Наименование тэга', blank=False,
                             db_index=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='tags', verbose_name='Категория')

    def __str__(self):
        return '{}'.format(self.title)

    class Meta:
        ordering = ['title']
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'


class Good(models.Model):
    title = models.CharField(default='default title', max_length=150, verbose_name='Наименование товара', blank=False,
                             db_index=True)
    price = models.DecimalField(default=10, max_digits=7, decimal_places=2, verbose_name='Стоимость товара',
                                blank=False, db_index=True)
    description = models.TextField(default='default description', max_length=500, verbose_name='Описание товара',
                                   blank=False)
    brand = models.CharField(default='default brand', max_length=150, verbose_name='Брэнд', blank=False, db_index=True)
    quantity = models.IntegerField(default=0, verbose_name='Количество')
    issue_date = models.DateField(default=date(2021, 1, 1), verbose_name='Дата изготовления', blank=True, db_index=True)
    vendor_code = models.CharField(default='default vendor code', max_length=254, verbose_name='Артикул товара',
                                   blank=False, db_index=True)
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата опубликования', db_index=True)
    tag = models.ForeignKey('Tag', default=1, on_delete=models.CASCADE, related_name='goods', verbose_name='Тэг')
    seller = models.ForeignKey('Seller', default=1, on_delete=models.CASCADE, related_name='goods', blank=True,
                               verbose_name='Продавец')
    # is_available = models.BooleanField(default=False, verbose_name='Наличие товара', db_index=True)
    # shipping_charge = models.DecimalField(default=0, max_digits=7, decimal_places=2, db_index=True)
    rating = models.IntegerField(default=0, verbose_name='Рэйтинг товара', blank=True, db_index=True)

    # def __init__(self, shipping_percent, commission_percent, *args, **kwargs):
    #     self.__shipping = shipping_percent
    #     self.__shipping_charge = None
    #     self.__commission = commission_percent
    #     self.__order_commission = None
    #     super().__init__(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.title)

    def get_absolute_url(self):
        return reverse('goods_detail_url', kwargs={'id': self.id})

    # Наличие товара на складе
    @property
    def is_available(self):
        if self.quantity > 0:
            return True
        return False

    # Стоимость доставки товара
    # @property
    # def shipping(self):
    #     return self.__shipping
    #
    # @shipping.setter
    # def shipping(self, percent):
    #     self.__shipping_charge = percent
    #     self.__shipping_charge = None
    #
    # @property
    # def shipping_charge(self):
    #     if self.__shipping_charge is None:
    #         self.__shipping_charge = round(self.__shipping * self.price / 100, 2)
    #     return self.__shipping_charge

    # Комиссия маркетплейса
    # @property
    # def commission(self):
    #     return self.__commission
    #
    # @commission.setter
    # def commission(self, percent):
    #     self.__commission = percent
    #     self.__order_commission = None
    #
    # @property
    # def order_commission(self):
    #     if self.__order_commission is None:
    #         self.__order_commission = round(self.__commission * self.price / 100, 2)
    #     return self.__order_commission

    class Meta:
        ordering = ['title']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Image(models.Model):
    upload_path = 'goods_images/'
    image_1 = models.ImageField(upload_to=upload_path, verbose_name='Фото 1', null=True)
    image_2 = models.ImageField(upload_to=upload_path, verbose_name='Фото 2', null=True)
    image_3 = models.ImageField(upload_to=upload_path, verbose_name='Фото 3', null=True)
    image_4 = models.ImageField(upload_to=upload_path, verbose_name='Фото 4', null=True)
    image_5 = models.ImageField(upload_to=upload_path, verbose_name='Фото 5', null=True)
    good = models.OneToOneField(Good, on_delete=models.CASCADE, primary_key=True, related_name='images',
                                verbose_name='Товар')

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'


class Characteristic(models.Model):
    color = models.CharField(default='default color', max_length=100, blank=False, db_index=True)
    size = models.IntegerField(default='default size')
    length = models.DecimalField(default='default length', max_digits=7, decimal_places=2)
    width = models.DecimalField(default='default width', max_digits=7, decimal_places=2)
    height = models.DecimalField(default='default height', max_digits=7, decimal_places=2)
    good = models.OneToOneField(Good, on_delete=models.CASCADE, primary_key=True, related_name='characteristics',
                                verbose_name='Товар')

    def __str__(self):
        return 'Color: {}'.format(self.color)

    class Meta:
        verbose_name = 'Характеристика'
        verbose_name_plural = 'Характеристики'


class User(models.Model):
    nickname = models.CharField(default='', max_length=150, verbose_name='Ник', blank=False,
                                db_index=True)
    email = models.EmailField(max_length=254, verbose_name='Электронная почта', blank=False, unique=True)
    password = models.CharField(max_length=150, verbose_name='Пароль', blank=False)
    first_name = models.CharField(max_length=150, verbose_name='Имя', blank=False, db_index=True)
    last_name = models.CharField(max_length=150, verbose_name='Фамилия', blank=False, db_index=True)
    reg_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрация')
    SELLER = 'S'
    CUSTOMER = 'C'
    ROLE_CHOICES = (
        (SELLER, 'Продавец'),
        (CUSTOMER, 'Покупатель'),
    )
    role = models.CharField(max_length=1, choices=ROLE_CHOICES, blank=True, verbose_name='Роль', db_index=True)
    last_visit_date = models.DateTimeField(auto_now_add=True, verbose_name='Последний визит')
    active = models.BooleanField(verbose_name='Активный', db_index=True)
    personal = models.BooleanField(default=False, verbose_name='Статус персонала', db_index=True)
    num_failed_logins = models.IntegerField(default=0, verbose_name='Количество неудачных входов')

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def get_absolute_url(self):
        return reverse('user-detail', kwargs={'pk': self.pk})

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    class Meta:
        ordering = ['last_name']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Review(models.Model):
    text = models.TextField(max_length=500, blank=False)
    date = models.DateTimeField(auto_now_add=True, db_index=True)
    good = models.ForeignKey('Good', on_delete=models.CASCADE, related_name='reviews', blank=True, verbose_name='Товар')
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='reviews', blank=True,
                                verbose_name='Пользователь')

    def __str__(self):
        return 'Text: {}'.format(self.text)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Customer(models.Model):
    upload_path = 'customers/'
    photo = models.ImageField(upload_to=upload_path, verbose_name='Фото профиля', null=True)
    phone = models.CharField(max_length=150, verbose_name='Телефон', blank=False, unique=True)
    birthday = models.DateField(default=date(1970, 1, 1), verbose_name='День рождения', blank=True, db_index=True)
    MAN = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = (
        (MAN, 'Мужской'),
        (FEMALE, 'Женский'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=MAN, verbose_name='Пол', db_index=True)
    country = models.CharField(default='', max_length=150, verbose_name='Страна', db_index=True)
    city = models.CharField(default='', max_length=150, verbose_name='Город', db_index=True)
    address = models.CharField(default='', max_length=150, verbose_name='Адрес', db_index=True)
    goods = models.ManyToManyField('Good', related_name='customers', blank=True, verbose_name='Товары')
    purchase_date = models.DateTimeField(default=datetime.now, verbose_name='Дата покупки', db_index=True)
    user = models.OneToOneField(User, default=1, on_delete=models.CASCADE, primary_key=True, related_name='customer',
                                verbose_name='Пользователь')

    def __str__(self):
        return 'Name: {} {}'.format(self.user.first_name, self.user.last_name)

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'


class Seller(models.Model):
    upload_path = 'sellers/'
    photo = models.ImageField(upload_to=upload_path, verbose_name='Фото профиля', null=True)
    phone = models.CharField(default='default phone', max_length=150, verbose_name='Телефон', blank=False, unique=True)
    company_name = models.CharField(default='default name', max_length=150, verbose_name='Название компании',
                                    blank=False, db_index=True)
    legal_entity = models.CharField(default='default legal entity', max_length=150, verbose_name='Юридическое лицо',
                                    blank=False, db_index=True)
    country = models.CharField(default='', max_length=150, verbose_name='Страна', db_index=True)
    city = models.CharField(default='', max_length=150, verbose_name='Город', db_index=True)
    address = models.CharField(default='', max_length=150, verbose_name='Адрес', db_index=True)
    manufacturer = models.CharField(default='', max_length=150, verbose_name='Производитель', db_index=True)
    manufacturer_country = models.CharField(default='', max_length=150, verbose_name='Страна происхождения',
                                            db_index=True)
    user = models.OneToOneField(User, default=1, on_delete=models.CASCADE, primary_key=True, related_name='seller',
                                verbose_name='Пользователь')

    def __str__(self):
        return 'Company name: {}'.format(self.company_name)

    class Meta:
        ordering = ['company_name']
        verbose_name = 'Продавец'
        verbose_name_plural = 'Продавцы'
