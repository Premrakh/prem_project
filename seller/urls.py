from django.urls import path 
from .views import *
urlpatterns = [
    path('',seller_index, name='seller_index'),
    path('seller_register/',seller_register, name='seller_register'),
    path('add_product/',add_product, name='add_product'),
    path('my_products/',my_products, name='my_products'),
    path('seller_login/',seller_login, name='seller_login'),
    path('seller_edit_profile/',seller_edit_profile, name='seller_edit_profile'),
    path('seller_otp/',seller_otp,name='seller_otp'),
    path('seller_logout/',seller_logout,name='seller_logout'),
    path('edit_product/<int:pk>',edit_product,name='edit_product'),
    path('delete_product/<int:pk>',delete_product,name='delete_product')
]
