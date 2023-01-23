from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib.auth import login
from .models import CustomUser
from django.contrib import messages
from .verify import send_otp, verify_otp
from carts.models import Cart,CartItem
from carts.views import _cart_id

# Create your views here.
def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        #phone = request.POST['mobilenumber']
        phone = request.session['phone_number']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if CustomUser.objects.filter(phone=phone).exists():
                print('phone no taken')
                return redirect('signup')
            elif CustomUser.objects.filter(email=email).exists():
                print('email taken')
                messages.error(request, 'Email already taken!!')
                return redirect('signup')
            else:
    
                user = CustomUser.objects.create_user(first_name=firstname,last_name=lastname,email=email,password=password1,phone=phone)
                user.save()
                
                print('user created')

                
                return redirect('login')
            
        else:
            messages.error(request, 'Password not matching!!')
            print('password not matching')
            return redirect('signup')
    else:
     mobile = request.session['phone_number']
     context = {
         'mobile':mobile
     }  
     return render(request,'signup.html', context)
     
def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        #boss = CustomUser.objects.get(email=email)
        user = auth.authenticate(email=email,password=password)
        if user is not None:
            if user.is_active:
              try:
                print('enterd in to try')
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                print(is_cart_item_exists)
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)
                    print(cart_item)
                    for item in cart_item:
                        item.user = user
                        item.save()
                     
              except:
                print('enterd in to except')
                pass
              #user = auth.authenticate(email=email,password=password)
              auth.login(request,user)
              print('logged in')
              return redirect('home')
            else:
              print('user blocked')
              messages.error(request, 'You are Blocked !!')
              return redirect('login')
        else:
            print(' not logged in')
            messages.error(request, 'Invalid username or password !!')
            return redirect('login')
    else:    
        return render(request,'login.html')
def logout(request):
    print('logout')
    auth.logout(request)
    return redirect('home') 
    
def mobile(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        phone =  request.POST['mobilenumber']
        try:
            boss = CustomUser.objects.get(phone = phone)
            print('phone already taken')
            messages.error(request, 'number already taken!!')
            return redirect('mobile')
        except:
            request.session['phone_number'] = phone
            send_otp(phone)
            return redirect(verify_code)
    return render(request,'mobile.html')


def verify_code(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        otp = request.POST.get('otp')
        mobile = request.session['phone_number']
        verify = verify_otp(mobile, otp)
        print(verify)
        if verify:
            return redirect('signup')
        else:
            messages.error(request, 'Incorrect OTP, try again!!')
            print('incorrect otp')
            return redirect(verify_code)

    return render(request, 'verify_code.html')

def mobilelogin(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        phone =  request.POST['mobilenumber']
        if CustomUser.objects.filter(phone=phone).exists():
                request.session['phone_number'] = phone
                send_otp(phone)
                print('number exist')
                return redirect(verify_codelogin)
        else:
            messages.error(request, 'invalid mobile number!!')
            return redirect('mobilelogin')
    else:    
     return render(request,'mobilelogin.html')
def verify_codelogin(request):
    if request.user.is_authenticated:
        return redirect('home') 
    if request.method == 'POST':
        otp = request.POST.get('otp')
        mobile = request.session['phone_number']
        user = CustomUser.objects.get(phone=mobile)
        verify = verify_otp(mobile, otp)
        print(verify)
        if verify:
            if user.is_active:
               auth.login(request,user)
               print('loginned')
               return redirect('home')
            else:
                print('user blocked')
                messages.error(request, 'You are blocked!!')
                return redirect('login')

        
        else:
            messages.error(request, 'Incorrect OTP, try again!!')
            print('incorrect otp')
            return redirect(verify_codelogin)
    else:

      return render(request,'verify_codelogin.html')