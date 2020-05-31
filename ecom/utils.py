import json
from .models import *

def cartnumber(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        print("cart number success")
        return cartItems
    else:
        items = []
        order = {
        'get_cart_total':0,
        'get_cart_items':0,
        }

        cartItems = order['get_cart_items']
        return cartItems

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    print('Cart', cart)
    items = []
    order = {
    'get_cart_total':0,
    'get_cart_items':0,
    }

    cartItems = order["get_cart_items"]
    for i in cart:
        cartItems += cart[i]["quantity"]

    for i in cart:
        try:
            product = Product.objects.get(id=i)
            total = (product.price * cart[i]["quantity"])

            order["get_cart_total"] += total
            order["get_cart_items"] += cart[i]["quantity"]

            item = {
                "product":{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'image':product.image,
                },
                "quantity": cart[i]["quantity"],
                "get_total":total
            }
            items.append(item)
        except:
            pass
    return {
    'cartItems':cartItems,
    'order':order,
    'items':items,
    }

def cartData(request):
    if request.user.is_authenticated:
        print("x")
        cartItems = cartnumber(request)
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        print("in cart data")
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
    return {
    'cartItems':cartItems,
    'order':order,
    'items':items,
    }

def guestOrder(request, data):
    print("user is not logged in..")

    print('cookies', request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

    customer, created = Customer.objects.get_or_create(
    email=email,
    )
    customer.name = name
    customer.save()

    order = Order.objects.create(
    customer=customer,
    complete = False,
    )

    for item in items:
        product = Product.objects.get(id=item['product']['id'])

        orderItem = OrderItem.objects.create(
        product=product,
        order=order,
        quantity=item['quantity']
        )
    return customer, order
