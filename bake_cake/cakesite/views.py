from datetime import timedelta

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from django.http import HttpResponse

from .forms import CreateUserForm, CakeForm, OrderForm, CommentForm, LoginForm
from django.contrib import messages
from django.db import transaction
from .models import Cake, Order
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.exceptions import ValidationError


@transaction.atomic
def register(request):

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return render(request, 'registration/register_done.html', {'new_user': new_user})
    else:
        form = CreateUserForm()
    return render(request, 'registration/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)

                    return redirect('cakesite:private_office')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login or password')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('cakesite:login')


@transaction.atomic
@login_required
def create_cake_order_view(request):
    if request.method == 'POST':
        cake_form = CakeForm(request.POST)
        order_form = OrderForm(request.POST)
        if order_form.is_valid() and cake_form.is_valid():
            cd_cake = cake_form.cleaned_data
            cd_order = order_form.cleaned_data
            order = Order.objects.create(address=cd_order['address'],
                                         deliver_to=cd_order['deliver_to'],
                                         user=request.user,
                                         )
            cake = Cake.objects.create(levels_count=cd_cake['levels_count'],
                                       cake_form=cd_cake['cake_form'],
                                       topping=cd_cake['topping'],
                                       berries=cd_cake['berries'],
                                       decor=cd_cake['decor'],
                                       inscription=cd_cake['inscription'],
                                       promocode=cd_cake['promocode'],
                                       order=order,
                                       )
            cost = get_order_cost(order.id)
            order.cost = cost
            order.save()
            return redirect('cakesite:confirm_order', order_id=order.id)
    else:
        cake_form = CakeForm()
        order_form = OrderForm(initial={'address': request.user.address})
    return render(request, "create_order.html", {'cake_form': cake_form,
                                                 'order_form': order_form})


@login_required
def get_private_office(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, "private_office.html", {'orders': orders})


@login_required
def cancel_order(request, order_id):
    Order.objects.get(id=order_id).delete()
    return render(request, "order_cancellation.html")


@transaction.atomic
@login_required
def confirm_order_view(request, order_id):
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            storage = messages.get_messages(request)
            cd_comment = comment_form.cleaned_data
            order = Order.objects.get(id=order_id)
            order.comment = cd_comment['comment']
            order.save()
            return redirect('cakesite:confirm_order_done', order_id=order_id)
    else:
        comment_form = CommentForm()
        order = Order.objects.get(id=order_id)
        cake = Cake.objects.get(order=order)
        return render(request,
                      "confirm_order.html",
                      {'comment_form': comment_form,
                       'order': order,
                       'cake': cake})


@login_required
def confirm_order_done(request, order_id):
    return render(request, 'confirm_order_done.html')


def get_order_cost(order_id):
    cost = 0

    order = Order.objects.get(id=order_id)
    cake = Cake.objects.get(order=order)

    levels_count = {
        '1': 400,
        '2': 750,
        '3': 1100,
    }

    cost = cost + levels_count[cake.levels_count]

    cake_form = {
        'Квадрат': 600,
        'Круг': 400,
        'Прямоугольник': 1000,
    }

    cost = cost + cake_form[cake.cake_form]

    toppings = {
        'Без топпинга': 0,
        'Белый соус': 200,
        'Карамельный сироп': 180,
        'Кленовый сироп': 200,
        'Клубничный сироп': 300,
        'Черничный сироп': 350,
        'Молочный шоколад': 200,
    }

    for topping in cake.topping:
        cost = cost + toppings[topping]

    berries = {
        'Ежевика': 400,
        'Малина': 300,
        'Голубика': 450,
        'Клубника': 500,

    }

    for berry in cake.berries:
        cost = cost + berries[berry]

    decors = {
        'Фисташки': 300,
        'Безе': 400,
        'Фундук': 350,
        'Пекан': 300,
        'Маршмеллоу': 200,
        'Марципан': 280,

    }

    for decor in cake.decor:
        cost = cost + decors[decor]

    if cake.inscription:
        cost = cost + 500

    if cake.promocode == "ТОРТ":
        cost = cost * 0.8

    if order.deliver_to <= timezone.now() + timedelta(days=1):
        cost = cost * 1.2

    return cost
