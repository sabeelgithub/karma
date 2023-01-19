from django.shortcuts import render
from.models import Category,Sub_Category
from shop.models import Products
# Create your views here.
"""def category(request):
    categories = Category.objects.all()
    sub = Sub_Category.objects.all()
    products = Products.objects.all()
    
    context = {
        'categories' : categories,
        'sub':sub,
        'products':products
    }
    return render(request,'category.html',context)
"""


