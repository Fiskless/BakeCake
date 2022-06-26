from django.urls import path
from django.views.generic import TemplateView
from . import views


app_name = "cakesite"

urlpatterns = [
    path('', views.user_login, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register, name='register'),
    path('private_office/', views.get_private_office, name='private_office'),
    path('create_order/', views.create_cake_order_view, name='create_order'),
    path('order_cancellation/<int:order_id>/', views.cancel_order, name='order_cancellation'),
    path('confirm_order/<int:order_id>/', views.confirm_order_view, name='confirm_order'),
    path('confirm_order/<int:order_id>/done/', views.confirm_order_done, name='confirm_order_done'),
]
