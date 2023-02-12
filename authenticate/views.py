from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib.auth import login
from .models import CustomUser
from home.models import UserProfile
from django.contrib import messages
from .verify import send_otp, verify_otp
from carts.models import Cart,CartItem
from carts.views import _cart_id
import requests
from django.http import HttpResponse
#verification
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

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
                messages.error(request, 'Phone already taken!!')
                return redirect('signup')
            elif CustomUser.objects.filter(email=email).exists():
                print('email taken')
                messages.error(request, 'Email already taken!!')
                return redirect('signup')
            else:
                 
                
                user = CustomUser.objects.create_user(first_name=firstname,last_name=lastname,email=email,password=password1,phone=phone)
                user.save()
                userprofile = UserProfile.objects.create(user_id=user.id)
                userprofile.save()
               
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
     return render(request,'authenticate/signup.html', context)
     
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
                if is_cart_item_exists:
                    print(is_cart_item_exists)
                    cart_item = CartItem.objects.filter(cart=cart)
                    # getting the product variation by cart id
                    product_variation = []
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))

                    # get the cart items from the user to access his product variation 
                    cart_item = CartItem.objects.filter(user=user)
                    print('hoi')
                    ex_var_list = []
                    id = []
                    for item in cart_item:
                        existing_variation = item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)
                        print('lo')

                    for pr in product_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            item_id = id[index]    
                            item = CartItem.objects.get(id=item_id)
                            item.quantity +=1
                            item.user = user
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()
                     
              except:
                print('enterd in to except')
                pass
              #user = auth.authenticate(email=email,password=password)
              auth.login(request,user)
              url = request.META.get('HTTP_REFERER')
              try:
                  query = requests.utils.urlparse(url).query
                  # next = /cart/checkout
                  params = dict(x.split('=')for x in query.split('&'))
                  if 'next' in params:
                      nextPage = params['next']
                      return redirect(nextPage)
              
              except:
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
        return render(request,'authenticate/login.html')
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
    return render(request,'authenticate/mobile.html')


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

    return render(request, 'authenticate/verify_code.html')

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
     return render(request,'authenticate/mobilelogin.html')
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

      return render(request,'authenticate/verify_codelogin.html')
    
def forgotPassword(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST['email']
        if CustomUser.objects.filter(email=email).exists():
            user = CustomUser.objects.get(email__exact=email)

            # Reset password email
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            messaage = render_to_string('authenticate/password-reset.html',{
                'user': user,
                'domain' : current_site,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : default_token_generator.make_token(user),
            })
            to_mail = email
            print(email)
            send_male= EmailMessage(mail_subject, messaage, to=[to_mail])
            print('last chathi')
            print(send_male)
            send_male.send()
            
            messages.success(request, "Password reset email has been sent to your email. Please reset your account")
            return redirect('login')
        else:
            messages.error(request, 'Account does not exists')
            return redirect('forgotPassword')
    return render(request, 'authenticate/forgotPassword.html')


def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser._default_manager.get(pk=uid)
    except:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')

    else:
        messages.error(request, 'This link has been expired!')
        return redirect('login')
def resetPassword(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = CustomUser.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successfully ')
            return redirect('login')

        else:
            messages.error(request, 'Password does not match!')
            return redirect('resetPassword')
    else:
     return render(request,'authenticate/resetPassword.html')
