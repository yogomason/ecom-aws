from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/<str:pk>/', views.product, name='product_page'),
    path('create_product', views.createProduct, name="create_product"),
    path('update_product/<str:pk>/', views.update, name="update_product"),
    path('delete_product/<str:pk>/', views.delete, name="delete_product"),

    path('login/', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),
    path('logout/', views.logoutUser, name="logout"),

    path('user/', views.userpage, name="userpage"),

    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),

    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="update_item"),
]
