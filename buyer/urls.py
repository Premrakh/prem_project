from django.urls import path 
from .views import *

urlpatterns = [
    path('',index, name='index'),
    path('about/',about, name='about'),
    path('contact/',contact, name='contact'),
    path('faqs/',faqs, name='faqs'),
    path('help/',help, name='help'),
    path('product/',product, name='product'),
    path('product2/',product2, name='product2'),
    path('icons/',icons, name='icons'),
    path('typography/',typography, name='typography'),
    path('register/',register, name='register'),
    path('otp/',otp, name='otp'),
    path('login/',login, name='login'),
    path('logout/',logout, name='logout'),
    path('edit_profile/',edit_profile, name='edit_profile'),
    path('forgot_password/',forgot_password, name='forgot_password'),
    path('cart/',cart, name='cart'),
    path('add_to_cart/<int:pk>',add_to_cart, name='add_to_cart'),
    path('del_cart_product/<int:pk>',del_cart_product, name='del_cart_product'),
    path('cart/paymenthandler/', paymenthandler, name='paymenthandler'),
    path('view_order/',view_order, name='view_order'),

]
