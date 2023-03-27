from django.db import models

# Create your models here.
class Seller(models.Model):
    genders=[('male','male'),('female','female'),('other','other')]  
    
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    email=models.EmailField(unique=True, max_length=254)
    password=models.CharField( max_length=50)
    address=models.CharField(max_length=100)
    gender=models.CharField(choices=genders, max_length=50)
    pic=models.FileField( upload_to='seller_pics',default='empty.jpg')
    
    def __str__(self):
        return self.first_name
    
class Product(models.Model):
    product_name=models.CharField( max_length=50)
    des= models.CharField( max_length=150)
    price=models.FloatField(default=10.0)
    product_stock=models.IntegerField(default=0)
    pic=models.FileField(upload_to='product_pics', default='empty.jpg')
    selller=models.ForeignKey(Seller, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.product_name
    