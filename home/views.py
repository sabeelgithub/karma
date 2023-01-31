from django.shortcuts import render,redirect,get_object_or_404
from shop.models import Products
from authenticate.models import CustomUser
from order.models import Order,OrderProduct
from .models import UserProfile
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from authenticate.forms import CustomUserForm,UserProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    products = Products.objects.all()[:8]
    context={
        'products':products,
    }
    return render(request,'index.html',context)

@login_required(login_url='login')
def profile(request):
    return render(request,'profile.html')

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
    return render(request,'userdash.html',context)

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
    return render(request,'edit_profile.html',context)

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

    return render(request,'change_password.html')

@login_required(login_url='login')
def my_orders(request):
    orders = Order.objects.filter(user=request.user,is_ordered=True).order_by('-created_at')
    paginator = Paginator(orders,8)
    page= request.GET.get('page')
    paged_users = paginator.get_page(page)
    context = {
       'orders': paged_users, 
    }
    return render(request,'my_orders.html',context)

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
    grand_total = total + tax 
    grand_total_shipping=total + tax + shipping
    context = {
        'order_detail':order_detail,
        'orders':orders,
        'total':total,
        'tax':tax,
        'shipping':shipping,
        'grand_total':grand_total,
        'grand_total_shipping':grand_total_shipping,
    }
    return render(request,'order_details.html',context)