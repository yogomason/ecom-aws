from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group

import datetime

import json

from django.contrib.auth.decorators import login_required

from .decorators import *
from .models import *
from .forms import *
from .utils import *
# Create your views here.


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    print(data)
    order.transaction_id = transaction_id
    print('Total:', total, 'cart total:',order.get_cart_total)
    if total == order.get_cart_total:
        print(order.complete)
        order.complete = True
        print(order.complete)
    order.save()
    ShippingAddress.objects.create(
        customer=customer,
        order=order,
        name=data['form']['name'],
        address=data['shipping']['address'],
        address2=data['shipping']['address2'],
        city=data['shipping']['city'],
        postcode=data['shipping']['postcode'],
    )

    return JsonResponse('Payment complete', safe=False)



def userpage(request):
    return render(request, 'ecom/user.html')
# @login_required(login_url='login')

def home(request):
    print(request.user)
    if request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create(user=request.user)
    cookieData = cartData(request)
    cartItems = cookieData['cartItems']
    products = Product.objects.all()
    total_products = products.count()

    context = {
        'products': products,
        'total_products': total_products,
        'cartItems': cartItems,
    }

    return render(request, 'ecom/home.html', context)

def product(request, pk):
    cookieData = cartData(request)
    cartItems = cookieData['cartItems']
    product = Product.objects.get(id=pk)

    context = {
        'product': product,
        'cartItems': cartItems,
    }

    return render(request, 'ecom/product.html', context)

def createProduct(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/')

    context = {
        'form': form,
        'product': product,
    }
    return render(request, 'ecom/productForm.html',context)

@allowed_users(allowed_roles=['Admin'])
def update(request, pk):
    product = Product.objects.get(id=pk)

    form = ProductForm(instance=product)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
        return redirect('/')

    context = {
    'form': form
    }

    return render(request, 'ecom/updateProduct.html', context)

def delete(request, pk):
    cartItems = cartnumber(request)
    product = Product.objects.get(id=pk)

    if request.method == 'POST':
        product.delete()
        return redirect('/')

    context = {
    'product': product,
    }

    return render(request, 'ecom/delete.html', context)


@unauthenticated_user
def loginPage(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.info(request, 'Username OR password is incorrect')

	return render(request, 'ecom/login.html',)

def logoutUser(request):
	logout(request)
	return redirect('login')


def cart(request):
    cookieData = cartData(request)
    cartItems = cookieData['cartItems']
    order = cookieData['order']
    items = cookieData['items']

    context = {
    'items':items,
    'order': order,
    'cartItems': cartItems
    }

    return render(request, 'ecom/cart.html', context)


def checkout(request):
    cookieData = cartData(request)
    cartItems = cookieData['cartItems']
    order = cookieData['order']
    items = cookieData['items']

    context = {
    'items':items,
    'order': order,
    'cartItems': cartItems
    }
    return render(request, 'ecom/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    print(data)
    x = data['productId']
    print(x)
    action = data['action']
    productId = x['product']

    print('Action:', action)
    print('productId:', productId)

    customer = request.user.customer
    print(customer)
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action== 'add':
        orderItem.quantity += 1
        print("quantity",orderItem.quantity)
    elif action == 'remove':
        orderItem.quantity -= 1


    orderItem.save()
    print("saved")

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='Customer')
            user.groups.add(group)
            customer, created = Customer.objects.get_or_create(user=user)
            messages.success(request, 'Account created for ' + username)
            return redirect('login')
    context = {
    'form':form
    }
    return render(request, 'ecom/register.html', context)
