from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from authenticate.models import CustomUser
from django.contrib import messages
from category.models import Category,Sub_Category
from shop.models import Products,Variation
from .forms import Update_categoryForm,CategoryForm,Update_sub_categoryForm,Sub_CategoryForm,ProductForm,Update_ProductForm,VariationForm,Update_VariationForm
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.db.models import Q

# Create your views here.
def adminlogin(request):
    if 'email' in request.session:
        return redirect('dashbord')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email,password=password)
        if user is not None:
            if user.is_superuser:
                request.session['email'] = email
                auth.login(request,user)
                print('admin loggined')
                return redirect('dashbord')
            else:
                print('Not authorized')
                messages.error(request, 'Invalid username or password !!')
                return redirect('adminlogin')
                
        else:
            return redirect('adminlogin')    
    else:
        return render(request,'adminlogin.html')
def dashbord(request):
    if 'email' in request.session:
        return render(request,'dashbord.html')
    else:
        return redirect('adminlogin')
   
def adminlogout(request):
    if 'email' in request.session:
        request.session.flush()
    print('admin logoutted')
    auth.logout(request)
    return redirect('adminlogin')
def users(request):
    users = CustomUser.objects.all()
    paginator = Paginator(users,8)
    page= request.GET.get('page')
    paged_users = paginator.get_page(page)
    context = {
        'users': paged_users

    }
    return render(request,'users.html',context)

def blockuser(request, id): 
      user = CustomUser.objects.get(id=id)
      if user.is_active:
        user.is_active = False
        user.save()

      else:
         user.is_active = True
         user.save()

      return redirect('users')
def admincategory(request):
    categories = Category.objects.all()
    paginator = Paginator(categories,6)
    page= request.GET.get('page')
    paged_categories = paginator.get_page(page) 
    context = {
        'categories':paged_categories,
    }
    return render(request,'admincategory.html',context)
def delete_category(request,id):
    dlt = Category.objects.get(pk=id)
    dlt.delete()
    return redirect('admincategory')
    
def update_category(request,id):
    if request.method == 'POST':
        update =Category.objects.get(pk=id)
        form = Update_categoryForm(request.POST,instance=update)
        if form.is_valid():
          form.save()
          return redirect('admincategory')
        else:
            messages.error(request, 'category already exsist!!!')
            return redirect('update_category',id)
    else:
        update = Category.objects.get(pk=id)
        form = Update_categoryForm(instance=update)
        context={
            'form':form
        }
        return render(request,'update_category.html',context)

    
def add_category(request):
    if request.method == 'POST':
      form = CategoryForm(request.POST)
      if form.is_valid() :
         
         form.save()
         messages.success(request, 'Category added successfully.')
         return redirect('admincategory')
      else:
         messages.error(request, 'category already exisist!!!')
         return redirect('add_category')
         

    
    form = CategoryForm()
    context={
        'form':form
    }
    return render(request,'add_category.html',context)
def adminsub_category(request):
    sub = Sub_Category.objects.all()
    paginator = Paginator(sub,6)
    page= request.GET.get('page')
    paged_sub = paginator.get_page(page) 
    context = {
        'sub':paged_sub,  
    }
    return render(request,'adminsub_category.html',context)
def delete_sub_category(request,id):
    dlt = Sub_Category.objects.get(pk=id)
    dlt.delete()
    return redirect('adminsub_category')
def update_sub_category(request,id):
    if request.method == 'POST':
        update =Sub_Category.objects.get(pk=id)
        form = Update_sub_categoryForm(request.POST,instance=update)
        if form.is_valid():
          form.save()
          return redirect('adminsub_category')
        else:
            messages.error(request, 'category already exsist!!!')
            return redirect('update_sub_category',id)
    else:
        update = Sub_Category.objects.get(pk=id)
        form = Update_sub_categoryForm(instance=update)
        context={
            'form':form
        }
    return render(request,'update_sub_category.html',context)
def add_sub_category(request):
   
    if request.method == 'POST':
      
      form = Sub_CategoryForm(request.POST)
      

      if form.is_valid():
         form.save()
         messages.success(request, 'Category added successfully.')
         return redirect('adminsub_category')
      else:
         messages.error(request, 'category already exisist!!!')
         return redirect('add_sub_category')
         
    form = Sub_CategoryForm()
    context={
        'form':form
    }
    return render(request,'add_sub_category.html',context)
#admin product
def adminproduct(request):
    products = Products.objects.all()
    paginator = Paginator(products,3)
    page= request.GET.get('page')
    paged_products = paginator.get_page(page)
    context = {
        'products':paged_products
    }
    return render(request,'adminproduct.html',context)
def add_product(request):
    if request.method == 'POST':
      form = ProductForm(request.POST,request.FILES)
      if form.is_valid() :
         
         form.save()
         messages.success(request, 'Product added successfully.')
         return redirect('adminproduct')
      else:
         messages.error(request, 'product already exisist!!!')
         return redirect('add_product')
         

    
    form = ProductForm()
    context={
        'form':form
    }
    return render(request,'add_product.html',context)
def delete_product(request,id):
    dlt = Products.objects.get(pk=id)
    dlt.delete()
    return redirect('adminproduct')
def update_product(request,id):
    if request.method == 'POST':
        update =Products.objects.get(pk=id)
        form = Update_ProductForm(request.POST,request.FILES,instance=update)
        if form.is_valid():
          form.save()
          return redirect('adminproduct')
        else:
            messages.error(request, 'category already exsist!!!')
            return redirect('update_product',id)
    else:
        update = Products.objects.get(pk=id)
        form = Update_ProductForm(instance=update)
        context={
            'form':form
        }
    return render(request,'update_product.html',context)
def admin_search(request):
   users = None
   categories = None
   sub = None
   products = None
   

   if 'keyword' in request.GET:
       keyword = request.GET['keyword']
       if keyword:
           users = CustomUser.objects.order_by('-first_name').filter(Q(first_name__icontains=keyword)|Q(last_name__icontains=keyword))
           categories = Category.objects.order_by('-category_name').filter(Q(slug__icontains=keyword)|Q(category_name__icontains=keyword))
           sub = Sub_Category.objects.order_by('-sub_category_name').filter(Q(slug__icontains=keyword)|Q(sub_category_name__icontains=keyword))
           products = Products.objects.order_by('-created_at').filter(Q(description__icontains=keyword)|Q(product_name__icontains=keyword))
           
           
           print('kooooi')
    #    else:
        #    return redirect('users')
   context = {
           'users':users,
           'categories':categories,
           'sub':sub,
           'products':products,

         }       
   return render(request,'admin_search.html',context)
 

 # variation
def variation(request):
    variation = Variation.objects.all()
    paginator = Paginator(variation,7)
    page= request.GET.get('page')
    paged_categories = paginator.get_page(page) 
    context = {
        'variation' : paged_categories,
    }
    return render(request,'variation.html',context)
def delete_variation(request,id):
    dlt = Variation.objects.get(pk=id)
    dlt.delete()
    return redirect('variation')
def add_variation(request):
    if request.method == 'POST':
      form = VariationForm(request.POST)
      if form.is_valid() :
         
         form.save()
         messages.success(request, 'variation added successfully.')
         return redirect('variation')
      else:
         messages.error(request, 'variation already exisist!!!')
         return redirect('add_variation')
         

    
    form = VariationForm()
    context={
        'form':form
    }
    return render(request,'add_product.html',context)
def update_variation(request,id):
    if request.method == 'POST':
        update =Variation.objects.get(pk=id)
        form = Update_VariationForm(request.POST,instance=update)
        if form.is_valid():
          form.save()
          return redirect('variation')
        else:
            messages.error(request, 'category already exsist!!!')
            return redirect('update_variation',id)
    else:
        update = Variation.objects.get(pk=id)
        form = Update_VariationForm(instance=update)
        context={
            'form':form
        }
    return render(request,'update_variation.html',context)