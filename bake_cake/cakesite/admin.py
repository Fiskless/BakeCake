from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from import_export.fields import Field

from .models import Cake, Order, CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    pass


class OrderResource(resources.ModelResource):
    address = Field(attribute='address', column_name='Адрес доставки')
    deliver_to = Field(attribute='deliver_to',
                       column_name='Дата и время доставки')
    order_status = Field(attribute='order_status', column_name='Статус заказа')
    cost = Field(attribute='cost', column_name='Стоимость торта')
    comment = Field(attribute='comment', column_name='Комментарий к заказу')
    levels_count = Field(attribute='cakes__levels_count',
                         column_name='Количество уровней')
    cake_form = Field(attribute='cakes__cake_form',
                      column_name='Форма торта')
    topping = Field(attribute='cakes__topping',
                    column_name='Топпинг')
    berries = Field(attribute='cakes__berries',
                    column_name='Ягоды')
    decor = Field(attribute='cakes__decor',
                  column_name='Декор')
    inscription = Field(attribute='cakes__inscription',
                        column_name='надпись')

    class Meta:
        model = Order
        fields = ['address',
                  'deliver_to',
                  'order_status',
                  'cost',
                  'comment',
                  ]


class CakeInline(admin.TabularInline):
    model = Cake
    list_display = ['levels_count',
                    'cake_form',
                    'topping',
                    'berries',
                    'decor',
                    'inscription',
                    'promocode',
                    ]
    readonly_fields = ['levels_count',
                    'cake_form',
                    'topping',
                    'berries',
                    'decor',
                    'inscription',
                    'promocode',
                    ]


@admin.register(Order)
class OrderAdmin(ImportExportModelAdmin):
    resource_class = OrderResource
    readonly_fields = ('cost',)
    inlines = [CakeInline]
    list_display = ['address', 'deliver_to', 'order_status', 'cost']