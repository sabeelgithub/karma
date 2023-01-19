from django.shortcuts import render
from shop.models import Products
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator

# Create your views here.
def index(request):
    products = Products.objects.all()[:8]
    context={
        'products':products,
    }
    return render(request,'index.html',context)
