from datetime import datetime

from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import reverse


class Category(models.Model):
    """
    Class describing a model of good category
    :param title: Category name
    """
    title = models.CharField(max_length=150, verbose_name='Наименование категории',
                             blank=False, db_index=True)

    def __str__(self) -> str:
        return '{}'.format(self.title)

    def get_absolute_url(self) -> str:
        return '/%s/' % self.title

    class Meta:
        ordering = ['title']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Tag(models.Model):
    """
    Class describing a model of good tag
    :param title: Tag name
    :param category: Category related to tag
    """
    title = models.CharField(max_length=150, verbose_name='Наименование тэга',
                             blank=False, db_index=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE,
                                 related_name='tags', verbose_name='Категория')

    def __str__(self) -> str:
        return '{}'.format(self.title)

    def get_absolute_url(self) -> str:
        return '/%s/' % self.title

    class Meta:
        ordering = ['title']
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'


class Good(models.Model):
    """
    Class describing a model of goods
    :param title: Good name
    :param price: Good price
    :param description: Good description
    :param brand: Good brand
    :param quantity: Good quantity in stock
    :param issue_date: Date of good issue
    :param vendor_code: Product identification number
    :param tag: Tag related to good
    :param seller: Seller related to good
    :param rating: Good rating
    :param counter: Good view counter
    """
    title = models.CharField(max_length=150, verbose_name='Наименование товара',
                             blank=False, db_index=True)
    price = models.DecimalField(max_digits=7, decimal_places=2,
                                verbose_name='Стоимость товара', blank=False, db_index=True)
    description = models.TextField(max_length=500, verbose_name='Описание товара',
                                   blank=False)
    brand = models.CharField(max_length=150, verbose_name='Брэнд', blank=False,
                             db_index=True)
    quantity = models.IntegerField(verbose_name='Количество')
    issue_date = models.DateField(null=True, verbose_name='Дата изготовления',
                                  blank=True, db_index=True)
    vendor_code = models.CharField(null=True, max_length=254, verbose_name='Артикул товара',
                                   blank=False, db_index=True)
    pub_date = models.DateTimeField(auto_now_add=True, null=True,
                                    verbose_name='Дата опубликования', db_index=True)
    tag = ArrayField(models.CharField(max_length=150), size=10, blank=True, verbose_name='Тэги')
    seller = models.ForeignKey('Seller', on_delete=models.CASCADE, related_name='goods',
                               blank=True, verbose_name='Продавец')
    # is_available = models.BooleanField(default=False, verbose_name='Наличие товара',
    #                                    db_index=True)
    # shipping_charge = models.DecimalField(default=0, max_digits=7, decimal_places=2,
    #                                       db_index=True)
    rating = models.IntegerField(null=True, verbose_name='Рэйтинг товара', blank=True,
                                 db_index=True)
    counter = models.IntegerField(default=0, verbose_name='Количество просмотров')

    # def __init__(self, shipping_percent, commission_percent, *args, **kwargs):
    #     self.__shipping = shipping_percent
    #     self.__shipping_charge = None
    #     self.__commission = commission_percent
    #     self.__order_commission = None
    #     super().__init__(*args, **kwargs)

    def __str__(self) -> str:
        return '{}'.format(self.title)

    def get_absolute_url(self) -> str:
        return reverse('goods_detail_url', args=[self.id])

    # Availability of goods in stock
    @property
    def is_available(self) -> bool:
        if self.quantity > 0:
            return True
        return False

    # Shipping cost
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

    # Marketplace commission
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
    """
    Class describing a model of good images
    :param image_1: Good image 1
    :param image_2: Good image 2
    :param image_3: Good image 3
    :param image_4: Good image 4
    :param image_5: Good image 5
    :param good: Good related to set of images
    """
    upload_path = 'goods_images/'
    good = models.OneToOneField(Good, on_delete=models.CASCADE,
                                related_name='images', verbose_name='Товар')
    image_1 = models.ImageField(upload_to=upload_path, verbose_name='Фото 1', null=True)
    image_2 = models.ImageField(upload_to=upload_path, verbose_name='Фото 2', null=True)
    image_3 = models.ImageField(upload_to=upload_path, verbose_name='Фото 3', null=True)
    image_4 = models.ImageField(upload_to=upload_path, verbose_name='Фото 4', null=True)
    image_5 = models.ImageField(upload_to=upload_path, verbose_name='Фото 5', null=True)

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'


class Characteristic(models.Model):
    """
    Class describing a model of good characteristics
    :param color: Good color
    :param size: Good size
    :param length: Good length
    :param width: Good width
    :param height: Good height
    :param good: Good related to set of characteristics
    """
    good = models.OneToOneField(Good, on_delete=models.CASCADE,
                                related_name='characteristics', verbose_name='Товар')
    color = models.CharField(max_length=100, null=True, blank=False, db_index=True)
    size = models.IntegerField(null=True)
    length = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    width = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    height = models.DecimalField(max_digits=7, decimal_places=2, null=True)

    def __str__(self) -> str:
        return 'Color: {}'.format(self.color)

    class Meta:
        verbose_name = 'Характеристика'
        verbose_name_plural = 'Характеристики'


class CustomUser(models.Model):
    """
    Class describing a model of custom user
    :param user: CustomUser related to User (AbstractUser)
    :param role: CustomUser role
    :param num_failed_logins: Number of failed login of CustomUser
    :param photo: CustomUser photo
    :param phone: CustomUser phone
    :param birthday: CustomUser birthday
    :param gender: CustomUser gender
    :param country: Country in which CustomUser lives
    :param city: City in which CustomUser lives
    :param address: CustomUser address
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    SELLER = 'S'
    CUSTOMER = 'C'
    ROLE_CHOICES = (
        (SELLER, 'Продавец'),
        (CUSTOMER, 'Покупатель'),
    )
    role = models.CharField(max_length=1, choices=ROLE_CHOICES, null=True, blank=True,
                            verbose_name='Роль', db_index=True)
    num_failed_logins = models.IntegerField(null=True,
                                            verbose_name='Количество неудачных входов')
    upload_path = 'users/'
    photo = models.ImageField(upload_to=upload_path, verbose_name='Фото профиля',
                              null=True)
    phone = models.CharField(max_length=150, verbose_name='Телефон', null=True,
                             blank=True, unique=True)
    birthday = models.DateField(verbose_name='День рождения', null=True,
                                blank=True, db_index=True)
    MAN = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = (
        (MAN, 'Мужской'),
        (FEMALE, 'Женский'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=MAN,
                              null=True, blank=True, verbose_name='Пол', db_index=True)
    country = models.CharField(max_length=150, null=True, blank=True,
                               verbose_name='Страна', db_index=True)
    city = models.CharField(max_length=150, null=True, blank=True,
                            verbose_name='Город', db_index=True)
    address = models.CharField(max_length=150, null=True, blank=True,
                               verbose_name='Адрес', db_index=True)

    def __str__(self) -> str:
        return 'Username: {}'.format(self.user.username)

    def get_absolute_url(self) -> str:
        return '/%i/' % self.user.pk

    class Meta:
        # ordering = ['user.username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


@receiver(post_save, sender=User)
def create_user_customuser(sender: User, instance: User, created: bool, **kwargs) -> None:
    if created:
        CustomUser.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_customuser(sender: User, instance: User, **kwargs) -> None:
    instance.customuser.save()


class Review(models.Model):
    """
    Class decsribing a model of good review
    :param text: Review text
    :param date: Review date
    :param good: Good related to review
    :param user: CustomUser related to review
    """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,
                                related_name='reviews', blank=True, verbose_name='Пользователь')
    text = models.TextField(max_length=500, blank=False)
    date = models.DateTimeField(auto_now_add=True, null=True, db_index=True)
    good = models.ForeignKey('Good', on_delete=models.CASCADE,
                             related_name='reviews', blank=True, verbose_name='Товар')

    def __str__(self) -> str:
        return 'Username: {}'.format(self.user.user.username)

    def get_absolute_url(self) -> str:
        return '/%i/' % self.good.pk

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Customer(models.Model):
    """
    Class describing a model of customer
    :param goods: Goods list related to customer
    :param purchase_date: Purchase date of goods
    :param customuser: CustomUser related to customer
    """
    customuser = models.OneToOneField(CustomUser, on_delete=models.CASCADE,
                                      related_name='customer', verbose_name='Пользователь')
    goods = models.ManyToManyField('Good', related_name='customers',
                                   blank=True, verbose_name='Товары')
    purchase_date = models.DateTimeField(default=datetime.now, null=True,
                                         verbose_name='Дата покупки', db_index=True)

    def __str__(self) -> str:
        return 'Username: {}'.format(self.customuser.user.username)

    def get_absolute_url(self) -> str:
        return '/%i/' % self.customuser.user.pk

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'


class Seller(models.Model):
    """
    Class describing a model of seller
    :param company_name: Company name
    :param legal_entity: Type of legal entity
    :param manufacturer: Goods manufacturer
    :param manufacturer_country: Manufacturer country
    :param customuser: CustomUser related to seller
    """
    customuser = models.OneToOneField(CustomUser, on_delete=models.CASCADE,
                                      related_name='seller', verbose_name='Пользователь')
    company_name = models.CharField(max_length=150, null=True,
                                    verbose_name='Название компании', blank=False, db_index=True)
    legal_entity = models.CharField(max_length=150, null=True,
                                    verbose_name='Юридическое лицо', blank=False, db_index=True)
    manufacturer = models.CharField(max_length=150, null=True,
                                    verbose_name='Производитель', db_index=True)
    manufacturer_country = models.CharField(max_length=150, null=True,
                                            verbose_name='Страна происхождения', db_index=True)

    def __str__(self) -> str:
        return 'Username: {}'.format(self.customuser.user.username)

    def get_absolute_url(self) -> str:
        return '/%i/' % self.customuser.user.pk

    class Meta:
        ordering = ['company_name']
        verbose_name = 'Продавец'
        verbose_name_plural = 'Продавцы'


class Subscriber(models.Model):
    """
    Class describing a model of subscriber
    :param is_subscribed: Subscription availability
    :param user: CustomUser related to User (AbstractUser)
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='user', verbose_name='Пользователь')
    is_subscribed = models.BooleanField(default=False, verbose_name='Подписчик')

    def __str__(self) -> str:
        return self.user.username

    class Meta:
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'
