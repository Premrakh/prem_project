from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
import random
from django.core.mail import send_mail
from django.conf import settings
from seller.models import *
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

# Create your views here.
def index(request):
    all_objects=Product.objects.all()    # all_objects=[obj1,obj2,obj3......]
    try:
        user_obj=Buyer.objects.get(email= request.session['buyer_email'])
        return render(request, 'index.html',{'user_data': user_obj ,'s_pros':all_objects})
    except:
        return render(request,'index.html',{'s_pros':all_objects})
def about(request):
    try:
        user_obj=Buyer.objects.get(email= request.session['buyer_email'])
        return render(request, 'about.html',{'user_data': user_obj})
    except:
        return render(request,'about.html')
def faqs(request):
    return render(request,'faqs.html')
def checkout(request):
    return render(request,'checkout.html')
def faqs(request):
    return render(request,'faqs.html')
def contact(request):
    return render(request,'contact.html')
def help(request):
    return render(request,'help.html')
def product(request):
    return render(request,'product.html')
def product2(request):
    return render(request,'product2.html')
def icons(request):
    return render(request,'icons.html')
def typography(request):
    return render(request,'typography.html')

#  Register ke liye ---------------------------------------------------------
def register(request):
    if request.method =='GET':
        return render(request,'register.html')
    else:
        try:
            u_raw=Buyer.objects.get(email=request.POST['email'])
            return render(request,'register.html',{'msg':'Email Already Exists'})
        except:
            global computer_otp
            computer_otp=random.randint(100000,999999)
            global u_list
            u_list=[request.POST['first_name'],request.POST['last_name'],request.POST['email'],request.POST['password'],request.POST['repassword']]
            subject='My GrocerySite'
            message=f'Your OTP is :{computer_otp}'
            from_email= settings.EMAIL_HOST_USER
            to_email=[request.POST['email']]
            send_mail(subject,message,from_email,to_email)
            return render(request,'otp.html')

def otp(request):
    if computer_otp== int(request.POST['u_otp']):
        Buyer.objects.create(
            first_name=u_list[0],
            last_name=u_list[1],
            email=u_list[2],
            password=u_list[3]
        )
        return render(request,'register.html',{'msg':'Create Sucessfully'})
    else:
        return render(request,'otp.html',{'msg':'enter valid OTP'})
    
    
# login process ------------------------------------------------
def login(request):
    if request.method=='GET':
        return render(request,'login.html')
    else:
        try:
            user_obj=Buyer.objects.get(email=request.POST['email'])
            if request.POST['password']==user_obj.password:
                request.session['buyer_email']=request.POST['email']
                return redirect('index')
            else:
                return render(request,'login.html',{'msg':'enter a valid password'})
        except:
            return render(request,'login.html',{'msg':'Email not Registered!!'})
        
def logout(request):
    del request.session['buyer_email']
    return render(request,'login.html')    

def edit_profile(request):
    e_obj=Buyer.objects.get(email=request.session['buyer_email'])
    if request.method=='GET':
        return render(request,'edit_profile.html',{'e_data':e_obj})
    else:
        e_obj.first_name=request.POST['first_name']
        e_obj.last_name=request.POST['last_name']
        e_obj.address=request.POST['address']
        e_obj.gender=request.POST['gender']
        e_obj.pic=request.FILES['pic']            #--------------------
        e_obj.save()
        return render(request,'edit_profile.html',{'msg':'Change Sucessfully !!','e_data':e_obj})

def forgot_password(request):
    if request.method=='GET':
        return render(request,'forgot_password.html')
    else:
        new_obj=Buyer.objects.get(email=request.POST['email'])
        subject='GrocerySite'
        message=f'Your Password is {new_obj.password}'
        from_email=settings.EMAIL_HOST_USER
        to_email=[new_obj.email]
        send_mail(subject,message,from_email,to_email)
        return render(request,'login.html')
    
def cart(request):
    try:
        user_obj=Buyer.objects.get(email=request.session['buyer_email'])
        global my_obj
        my_obj=Cart.objects.filter(buyer=user_obj)
        
        # count and amount cart page pe number of product and product amount
        # ke liye liye hai--------
        count=len(my_obj)
        global t_amount
        t_amount=0
        for i in my_obj:
            t_amount+=i.price
        
        # payment karvani process niche mujab    
        currency = 'INR'
        
        amount = t_amount*100 # Rs. 200
        if amount==0:
            return render(request,'cart.html',{'user_data': user_obj,   'my_product':my_obj, 'count':count,'amount':t_amount})
        else:
            
	# Create a Razorpay Order
            razorpay_order = razorpay_client.order.create(dict(amount=amount,
													currency=currency,
													payment_capture='0'))
        

             
        
	# order id of newly created order.
            razorpay_order_id = razorpay_order['id']
            callback_url = 'paymenthandler/'
        
	# we need to pass these details to frontend.
            context = {}
            context['razorpay_order_id'] = razorpay_order_id
            context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
            context['razorpay_amount'] = amount
            context['currency'] = currency
            context['callback_url'] = callback_url
            context.update({'user_data': user_obj,   'my_product':my_obj, 'count':count,'amount':t_amount})
            return render(request,'cart.html', context=context)
    except:
        return redirect('login')
    
def add_to_cart(request,pk):
    try:
        b_obj=Buyer.objects.get(email=request.session['buyer_email'])
        p_obj=Product.objects.get(id=pk)
        Cart.objects.create(
            p_name=p_obj.product_name,
            price=p_obj.price,
            pic=p_obj.pic,
            buyer=b_obj
        )
        return redirect('index')
    except:
        return render(request,'login.html')
 
def del_cart_product(request,pk):
    del_obj=Cart.objects.get(id=pk)           
    del_obj.delete()
    return redirect('cart')






# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
	auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):
    b_obj=Buyer.objects.get(email=request.session['buyer_email'])
	# only accept POST request.
    if request.method == "POST":
        try:
                     
			# get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
				'razorpay_order_id': razorpay_order_id,
				'razorpay_payment_id': payment_id,
				'razorpay_signature': signature
			}

			# verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
				params_dict)
            if result is not None:
                amount = t_amount*100 # Rs. 200
    
                try:       
					# capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)  
                    for i in my_obj:
                        AllOrder.objects.create(
                            p_name=i.p_name,
                            price=i.price,
                            pic=i.pic,
                            buyer=b_obj
                        )
                    for i in my_obj:
                        new_obj=Product.objects.get(product_name=i.p_name)
                        new_obj.product_stock -=1
                        new_obj.save()
                        i.delete()
                    # render success page on successful caputre of payment  
                    return render(request, 'paymentsuccess.html')
                except:
					# if there is an error while capturing payment.
                    return render(request, 'paymentfail.html')
            else:

				# if signature verification fails.
                return render(request, 'paymentfail.html')
        except:

			# if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
	# if other than POST request is made.
        return HttpResponseBadRequest()

def view_order(request):
    view_obj=AllOrder.objects.all()
    return render(request, 'view_order.html',{'all_product':view_obj})
    
