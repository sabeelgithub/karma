from django.shortcuts import render,get_object_or_404,redirect
from .models import Products,Sub_Category,Category
from carts.models import CartItem,Cart
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.http import HttpResponse
from django.db.models import Q
from carts.views import _cart_id
# Create your views here.
def shop(request,sub_category_slug=None):
    sub_category = None
    products = None
    categories = None
    
    
    if sub_category_slug !=None:
        print("hoooy")
        sub_category = get_object_or_404(Sub_Category,slug=sub_category_slug)
        products = Products.objects.filter(sub_category=sub_category,is_available=True)
        categories = Category.objects.all()
        sub = Sub_Category.objects.all()
        paginator = Paginator(products,6)
        page= request.GET.get('page')
        paged_products = paginator.get_page(page)
        
    else:
        print('koi')
        categories = Category.objects.all()
        sub = Sub_Category.objects.all()
        products = Products.objects.all()
        paginator = Paginator(products,6)
        page= request.GET.get('page')
        paged_products = paginator.get_page(page)
    context = {
        'categories' : categories,
        'sub':sub,
        'products':paged_products,
        
    }
    return render(request,'shop/shop.html',context)
def search(request):
   categories = Category.objects.all()
   sub = Sub_Category.objects.all()
   products = None
   if 'keyword' in request.GET:
       keyword = request.GET['keyword']
       if keyword:
           products = Products.objects.order_by('-created_at').filter(Q(description__icontains=keyword)|Q(product_name__icontains=keyword))
           
           print('kooooi')
       else:
           return redirect('shop')
   context = {
          'products':products,
          'categories':categories,
          'sub':sub

        }       
   return render(request,'shop/shop.html',context)
   
def product_details(request,sub_category_slug,product_slug):
    try:
        single_product =Products.objects.get(sub_category__slug=sub_category_slug,slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
    except Exception as e:
        raise e
    
    context = {
        'single_product':single_product,
        'in_cart':in_cart,
       

    }
    return render(request,'shop/product_details.html',context)