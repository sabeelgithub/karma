from django.shortcuts import render,redirect,get_object_or_404
from shop.models import Products
from authenticate.models import CustomUser
from order.models import Order,OrderProduct,Address
from .models import UserProfile
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from authenticate.forms import CustomUserForm,UserProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import AddressForm
# from datetime import datetime,timedelta,date
from datetime import date
from datetime import timedelta

# Create your views here.
def index(request):
    products = Products.objects.all()[:8]
    context={
        'products':products,
    }
    return render(request,'index.html',context)


@login_required(login_url='login')
def userdash(request):
    orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id,is_ordered=True)
    user=request.user
    orders_count = orders.count()
    userprofile = UserProfile.objects.get(user_id=request.user.id)
    context={
        'orders_count':orders_count,
        'user':user,
        'userprofile':userprofile 
    }
    return render(request,'profile/userdash.html',context)

@login_required(login_url='login')
def edit_profile(request):
    userprofile = get_object_or_404(UserProfile,user=request.user)
    if request.method == 'POST':
        user_form = CustomUserForm(request.POST,instance=request.user)
        profile_form = UserProfileForm(request.POST,request.FILES,instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'Your profile has been updated')
            return redirect('edit_profile')
        else:
            return redirect('edit_profile')
    else:
        user_form = CustomUserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    context= {
        'user_form':user_form,
        'profile_form':profile_form,
        'userprofile':userprofile,
        }
    return render(request,'profile/edit_profile.html',context)

@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        user = CustomUser.objects.get(email__exact=request.user.email)
        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                #auth.logout(request)
                messages.success(request,'Password updated successfully')
                return redirect('change_password')
            else:
                messages.error(request,'Please enter valid current password')
                return redirect('change_password')
        else:
            messages.error(request,'Password does not match!')
            return redirect('change_password')

    return render(request,'profile/change_password.html')

@login_required(login_url='login')
def my_orders(request):
    orders = Order.objects.filter(user=request.user,is_ordered=True).order_by('-id')
    paginator = Paginator(orders,8)
    page= request.GET.get('page')
    paged_users = paginator.get_page(page)
    today = date.today()
    for order in orders:
     add = order.updated_at + timedelta(days=7)

    context = {
       'orders': paged_users, 
       'today':today,
       'add':add,
    }
    return render(request,'profile/my_orders.html',context)

@login_required(login_url='login')
def order_details(request,order_id):
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)
    orders = Order.objects.get(order_number=order_id)
    total=0
    for i in order_detail:
           total += i.product_price * i.quantity
    tax = (2*total)/100
    shipping = (2*total)/100
    print('check')
    
    
    context = {
        'order_detail':order_detail,
        'orders':orders,
        'total':total,
        'tax':tax,
        'shipping':shipping,
       
    }
    return render(request,'profile/order_details.html',context)

@login_required(login_url='login')
def myAddress(request):
  current_user = request.user
  address = Address.objects.filter(user=current_user)
  paginator = Paginator(address,3)
  page= request.GET.get('page')
  paged_address = paginator.get_page(page)
  
  context = {
    'address':paged_address,
  }
  return render(request,'profile/myAddress.html', context)

@login_required(login_url='login')
def addAddress(request):
    if request.method == 'POST':
        form = AddressForm(request.POST,request.FILES,)
        if form.is_valid():
            print('form is valid')
            detail = Address()
            detail.user = request.user
            detail.first_name =form.cleaned_data['first_name']
            detail.last_name = form.cleaned_data['last_name']
            detail.phone =  form.cleaned_data['phone']
            detail.email =  form.cleaned_data['email']
            detail.address_line1 =  form.cleaned_data['address_line1']
            detail.address_line2  = form.cleaned_data['address_line2']
            detail.state =  form.cleaned_data['state']
            detail.city =  form.cleaned_data['city']
            detail.save()
            messages.success(request,'Address added Successfully')
            return redirect('myAddress')
        else:
            messages.success(request,'Form is Not valid')
            return redirect('myAddress')
    else:
        form = AddressForm()
        context={
            'form':form
        }    
    return render(request,'profile/addAddress.html',context)

@login_required(login_url='login')
def deleteAddress(request,id):
    address=Address.objects.get(id = id)
    messages.success(request,"Address Deleted")
    address.delete()
    return redirect('myAddress')

@login_required(login_url='login')
def editAddress(request, id):
  address = Address.objects.get(id=id)
  if request.method == 'POST':
    form = AddressForm(request.POST, instance=address)
    if form.is_valid():
      form.save()
      messages.success(request , 'Address Updated Successfully')
      return redirect('myAddress')
    else:
      messages.error(request , 'Invalid Inputs!!!')
      return redirect('myAddress')
  else:
      form = AddressForm(instance=address)
      
  context = {
            'form' : form,
        }
  return render(request , 'profile/editAddress.html' , context)




#checkout
def deleteCheckoutAddress(request,id):
    address=Address.objects.get(id = id)
    messages.success(request,"Address Deleted")
    address.delete()
    return redirect('checkout')



def AddCheckoutAddress(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            print('form is valid')
            detail = Address()
            detail.user = request.user
            detail.first_name =form.cleaned_data['first_name']
            detail.last_name = form.cleaned_data['last_name']
            detail.phone =  form.cleaned_data['phone']
            detail.email =  form.cleaned_data['email']
            detail.address_line1 =  form.cleaned_data['address_line1']
            detail.address_line2  = form.cleaned_data['address_line2']
            detail.state =  form.cleaned_data['state']
            detail.city =  form.cleaned_data['city']
            detail.save()
            messages.success(request,'Address added Successfully')
            return redirect('checkout')
        else:
            messages.success(request,'Form is Not valid')
            return redirect('checkout')
  


def error_404(request,exception):
    return render(request,'404.html', status=403)


