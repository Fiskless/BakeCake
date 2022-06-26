from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from multiselectfield import MultiSelectField
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class CustomUser(AbstractUser):
    phone = PhoneNumberField('мобильный телефон')
    communication_contact = models.CharField('ссылка на социальную сеть',
                                             blank=True,
                                             null=True,
                                             max_length=100)
    address = models.CharField('Адрес доставки',
                               max_length=100,
                               null=True,
                               blank=True)

    consent_to_processing_db = models.BooleanField('согласие на обработку персональных данных', default=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ("Заявка обрабатывается", "заявка обрабатывается"),
        ("Готовим ваш торт", "готовим ваш торт"),
        ("Торт в пути", "торт в пути"),
        ("Торт у вас", "торт у вас")
    ]

    comment = models.TextField('Комментарий к заказу',
                               max_length=200,
                               blank=True,
                               null=True)
    address = models.CharField('Адрес доставки', max_length=100)
    deliver_to = models.DateTimeField("Дата и время доставки",
                                         db_index=True,
                                         default=timezone.now)
    order_status = models.CharField("Статус заказа", max_length=30,
                                    choices=ORDER_STATUS_CHOICES,
                                    default="Заявка обрабатывается",
                                    db_index=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                             related_name='orders',
                             verbose_name='пользователь')
    cost = models.PositiveSmallIntegerField('Стоимость торта', 
                                            null=True,
                                            blank=True)

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return self.address


class Cake(models.Model):

    LEVELS_COUNT_CHOICES = [
        ("1", "1 уровень"),
        ("2", "2 уровня"),
        ("3", "3 уровня"),
    ]

    CAKE_FORM_CHOICES = [
        ("Квадрат", "квадрат"),
        ("Круг", "круг"),
        ("Прямоугольник", "прямоугольник"),
    ]

    TOPPING_CHOICES = [
        ("Без топпинга", "без топпинга"),
        ("Белый соус", "белый соус"),
        ("Карамельный сироп", "карамельный сироп"),
        ("Кленовый сироп", "кленовый сироп"),
        ("Клубничный сироп", "клубничный сироп"),
        ("Черничный сироп", "черничный сироп"),
        ("Молочный шоколад", "молочный шоколад"),
    ]

    BERRIES_CHOICES = [
        ("Ежевика", "ежевика"),
        ("Малина", "малина"),
        ("Голубика", "голубика"),
        ("Клубника", "клубника"),
    ]

    DECOR_CHOICES = [
        ("Фисташки", "фисташки"),
        ("Безе", "безе"),
        ("Фундук", "фундук"),
        ("Пекан", "пекан"),
        ("Маршмеллоу", "маршмеллоу"),
        ("Марципан", "марципан"),
    ]

    levels_count = models.CharField('количество уровней',
                                    max_length=50,
                                    choices=LEVELS_COUNT_CHOICES,
                                    db_index=True)
    cake_form = models.CharField('форма торта',
                                 max_length=50,
                                 choices=CAKE_FORM_CHOICES,
                                 db_index=True
                                 )
    topping = MultiSelectField('топпинг', choices=TOPPING_CHOICES, max_length=50,)
    berries = MultiSelectField('ягоды',
                               max_length=50,
                               choices=BERRIES_CHOICES,
                               db_index=True, blank=True,
                               null=True,
                               )
    decor = MultiSelectField('декор',
                             max_length=50,
                             choices=DECOR_CHOICES,
                             db_index=True, blank=True,
                             null=True,
                             )
    inscription = models.CharField('надпись', max_length=50, blank=True,
                                   null=True
                                   )
    promocode = models.CharField('промокод',
                                 max_length=50,
                                 blank=True,
                                 null=True,
                                 )
    order = models.OneToOneField(Order, on_delete=models.CASCADE,
                                 verbose_name='заказ',
                                 related_name='cakes',
                                 )

    class Meta:
        verbose_name = 'торт'
        verbose_name_plural = 'торты'

    def __str__(self):
        return f'Торт для {self.order.user} по адресу {self.order.address}'

