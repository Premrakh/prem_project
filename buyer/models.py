from django.db import models

# Create your models here.
class Buyer(models.Model):
    genders=[
        ('male','male'),('female','female'),('other','other')
    ]
    first_name=models.CharField( max_length=50)
    last_name=models.CharField( max_length=50)
    email=models.EmailField(unique=True, max_length=254)
    password=models.CharField(max_length=50)
    address=models.CharField(max_length=100)
    gender=models.CharField(choices=genders, max_length=50)
    pic=models.FileField( upload_to="seller_pics", default='empty.jpg')
    
    def __str__(self):
        return self.first_name
    
class Cart(models.Model):
    p_name= models.CharField(max_length=150)
    price=models.FloatField(default=10.0)
    pic=models.FileField( upload_to="cart_products", default='empty.jpg')
    buyer=models.ForeignKey(Buyer , on_delete=models.CASCADE)
    
    def __str__(self):
        return self.p_name

class AllOrder(models.Model):
    p_name= models.CharField(max_length=150)
    price=models.FloatField(default=10.0)
    pic=models.FileField( upload_to="cart_products", default='empty.jpg')
    buyer=models.ForeignKey(Buyer , on_delete=models.CASCADE)
    date=models.DateField(auto_now_add=True)
    time=models.TimeField( auto_now_add=True)

    def __str__(self):
        return self.p_name

