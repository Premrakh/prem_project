from django.shortcuts import render , redirect
from .models import *
import random
from django.conf import settings
from django.core.mail import send_mail
# Create your views here.

def seller_index(request):
    try:
        s_obj=Seller.objects.get(email=request.session['seller_email'])
        return render(request,'seller_index.html',{'s_data':s_obj})
    except:
        return render(request,'seller_login.html')
def add_product(request):
    # add_product page pe sellername & pic dikhne ke liye s_obj likha
    s_obj=Seller.objects.get(email=request.session['seller_email'])
    if request.method=='GET':
        return render(request,'add_product.html',{'s_data':s_obj})
    else:
        Product.objects.create(
            product_name=request.POST['product_name'],
            des=request.POST['des'],
            price=request.POST['price'],
            product_stock=request.POST['product_stock'],
            pic=request.FILES['pic'],
            selller=s_obj
        )
        return render(request,'add_product.html',{'msg':'Product Added Successfully !!','s_data':s_obj})


def seller_edit_profile(request):
    return render(request,'seller_edit_profile.html')

def seller_register(request):
    if request.method=='GET':
        return render(request,'seller_register.html')
    else:
        try:
            seller_data=Seller.objects.get(email=request.POST['email'])
            return render(request,'seller_register.html',{'msg':'Email already Exists'})
        except:
            global computer_otp
            computer_otp=random.randint(100000,999999)
            global u_list
            u_list=[request.POST['first_name'],request.POST['last_name'],request.POST['email'],request.POST['password']]    
            subject='GrocerySite'
            message=f'Seller your OTP is {computer_otp}'
            from_email=settings.EMAIL_HOST_USER
            to_email=[request.POST['email']]
            send_mail(subject,message,from_email,to_email)
            return render(request,'seller_otp.html')
        
def seller_otp(request):
    if request.method=='GET':
        return render(request,'seller_otp.html')
    else:
        if computer_otp==int(request.POST['u_otp']):
            Seller.objects.create(
                first_name=u_list[0],
                last_name=u_list[1],
                email=u_list[2],
                password=u_list[3],
                
            )
            return render(request,'seller_register.html',{'msg':'Register Sucessfully'})
        else:
            return render(request,'seller_otp.html',{'msg':'Invalid OTP'})

def seller_login(request):
    if request.method=='GET':
        return render(request,'seller_login.html')
    else:
        try:
            s_obj=Seller.objects.get(email=request.POST['email'])
            if request.POST['password']==s_obj.password:
                request.session['seller_email']=request.POST['email']
                return redirect('seller_index')
            else:
                return render(request,'seller_login.html',{'msg':"Password mismatch"})
        except:
            return render(request,'seller_login.html',{'msg':'Email Not Registerd !!'})   

def seller_logout(request):
    del request.session['seller_email']    
    return render(request,'seller_login.html')

def my_products(request):
    s_obj=Seller.objects.get(email=request.session['seller_email'])
    
   # FOREIGN KEY WALI FILED HAI TO OBJECT DENA HAI---------------
    my_pro=Product.objects.filter(selller=s_obj)
    return render(request,'my_products.html',{'seller_product':my_pro,'s_data':s_obj})

def seller_edit_profile(request):
    s_obj=Seller.objects.get(email=request.session['seller_email'])
    if request.method=='GET':
        return render(request,'seller_edit_profile.html',{'s_data':s_obj})
    else:
        e_obj = Seller.objects.get(email=request.session["seller_email"])
        e_obj.first_name=request.POST['first_name']
        e_obj.last_name=request.POST['last_name']
        e_obj.address=request.POST['address']
        e_obj.gender=request.POST['gender']
        e_obj.pic=request.FILES['pic']
        e_obj.save()
        return render(request,'seller_edit_profile.html',{'msg':'Change Successfully !!','s_data':s_obj})
    
def edit_product(request,pk):
    pro_edit=Product.objects.get(id=pk)
    s_obj=Seller.objects.get(email=request.session["seller_email"])
    if request.method=='GET':
        return render(request, 'edit_product.html',{'pro_edit':pro_edit,'s_data':s_obj})
    else:
        pro_edit.product_name=request.POST['product_name']
        pro_edit.des=request.POST['des']
        pro_edit.price=request.POST['price']
        pro_edit.product_stock=request.POST['product_stock']
        pro_edit.pic=request.FILES['pic']
        pro_edit.save()
        return render(request,'edit_product.html',{'pro_edit':pro_edit,'msg':'Edit Successfully!!','s_data':s_obj})
    
def delete_product(request,pk):
    del_pro=Product.objects.get(id=pk)
    del_pro.delete()
    return redirect("my_products")