from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User,auth
from authenticate.models import CustomUser
from django.contrib import messages
from category.models import Category,Sub_Category
from shop.models import Products,Variation
from order.models import Order,Payment,Coupon,OrderProduct
from .forms import Update_categoryForm,CategoryForm,Update_sub_categoryForm,Sub_CategoryForm,ProductForm,Update_ProductForm,VariationForm,Update_VariationForm,CouponForm
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.db.models import Q
from django.db.models.functions import Cast
from django.db.models import Sum, Q, FloatField
from datetime import datetime,timedelta,date
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import xlwt
#from django.contrib.admin.views.decorators import is_superuser_required
#from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required



# Create your views here.
def adminlogin(request):
    if request.user.is_superuser:
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
        return render(request,'adminpanel/adminlogin.html')

 
def adminlogout(request):
    if 'email' in request.session:
        request.session.flush()
    print('admin logoutted')
    auth.logout(request)
    return redirect('adminlogin')

@staff_member_required(login_url = 'adminLogin')
def users(request):
    users = CustomUser.objects.all()
    paginator = Paginator(users,8)
    page= request.GET.get('page')
    paged_users = paginator.get_page(page)
    context = {
        'users': paged_users

    }
    return render(request,'adminpanel/users.html',context)

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
    return render(request,'adminpanel/admincategory.html',context)
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
        return render(request,'adminpanel/update_category.html',context)

    
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
    return render(request,'adminpanel/add_category.html',context)
def adminsub_category(request):
    sub = Sub_Category.objects.all()
    paginator = Paginator(sub,6)
    page= request.GET.get('page')
    paged_sub = paginator.get_page(page) 
    context = {
        'sub':paged_sub,  
    }
    return render(request,'adminpanel/adminsub_category.html',context)
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
    return render(request,'adminpanel/update_sub_category.html',context)
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
    return render(request,'adminpanel/add_sub_category.html',context)
#admin product
def adminproduct(request):
    products = Products.objects.all().order_by('-id')
    paginator = Paginator(products,3)
    page= request.GET.get('page')
    paged_products = paginator.get_page(page)
    context = {
        'products':paged_products
    }
    return render(request,'adminpanel/adminproduct.html',context)
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
    return render(request,'adminpanel/add_product.html',context)
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
    return render(request,'adminpanel/update_product.html',context)






def admin_search(request):
   users = None
   categories = None
   sub = None
   products = None
   variations=None
   orders=None
   

   if 'keyword' in request.GET:
       keyword = request.GET['keyword']
       if keyword:
           users = CustomUser.objects.order_by('-first_name').filter(Q(first_name__icontains=keyword)|Q(last_name__icontains=keyword))
           categories = Category.objects.order_by('-category_name').filter(Q(slug__icontains=keyword)|Q(category_name__icontains=keyword))
           sub = Sub_Category.objects.order_by('-sub_category_name').filter(Q(slug__icontains=keyword)|Q(sub_category_name__icontains=keyword))
           products = Products.objects.order_by('-created_at').filter(Q(description__icontains=keyword)|Q(product_name__icontains=keyword))
           variations = Variation.objects.order_by('-created_at').filter(Q(variation_category__icontains=keyword)|Q(variation_value__icontains=keyword))
           orders = Order.objects.order_by('-created_at').filter(Q(order_number__icontains=keyword)|Q(payment__payment_method__icontains=keyword))
           coupons = Coupon.objects.order_by('-valid_from').filter(Q(code__icontains=keyword)|Q(discount__icontains=keyword))
           
           print('kooooi')
    #    else:
        #    return redirect('users')
   context = {
           'users':users,
           'categories':categories,
           'sub':sub,
           'products':products,
           'variations':variations,
           'orders':orders,
           'coupons':coupons,

         }       
   return render(request,'adminpanel/admin_search.html',context)
 

 # variation
def variation(request):
    variation = Variation.objects.all()
    paginator = Paginator(variation,7)
    page= request.GET.get('page')
    paged_variation = paginator.get_page(page) 
    context = {
        'variation' : paged_variation,
    }
    return render(request,'adminpanel/variation.html',context)
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
    return render(request,'adminpanel/add_variation.html',context)
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
    return render(request,'adminpanel/update_variation.html',context)

# oreder history
def orders(request):
    orders = Order.objects.filter(is_ordered=True).order_by('-id')
    paginator = Paginator(orders,7)
    page= request.GET.get('page')
    paged_orders = paginator.get_page(page) 

    context = {
        'orders': paged_orders,
       
    }
    return render(request,'adminpanel/orders.html',context)

def update_order(request, id):
  if request.method == 'POST':
    order = get_object_or_404(Order, id=id)
    status = request.POST.get('status')
    order.status = status 
    order.save()
    if status  == "Delivered":
      try:
          payment = Payment.objects.get(payment_id = order.order_number, status = False)
          print(payment)
          if payment.payment_method == 'Cash on Delivery':
              payment.status = True
              payment.save()
      except:
          pass
    order.save()
    
  return redirect('orders')


#coupon
def coupon(request):
    coupons = Coupon.objects.all()
    paginator = Paginator(coupons,7)
    page= request.GET.get('page')
    paged_coupon = paginator.get_page(page) 
    context = {
        'coupons':paged_coupon
    }
    return render(request,'adminpanel/coupon.html',context)


def addCoupon(request):
    if request.method == 'POST':
      form = CouponForm(request.POST)
      if form.is_valid() :
         
         form.save()
         messages.success(request, 'Coupon added successfully.')
         return redirect('coupon')
      else:
         messages.error(request, 'Coupon already exisist!!!')
         return redirect('addCoupon')
      
    form = CouponForm()
    context={
        'form':form
    }
    return render(request,'adminpanel/addCoupon.html',context)  


def deleteCoupon(request,id):
    dlt = Coupon.objects.get(pk=id)
    dlt.delete()
    return redirect('coupon')

def updateCoupon(request,id):
    if request.method == 'POST':
        update = Coupon.objects.get(pk=id)
        form = CouponForm(request.POST,instance=update)
        if form.is_valid():
          form.save()
          return redirect('coupon')
        else:
            messages.error(request, 'Coupon already exsist!!!')
            return redirect('updateCoupon',id)
    else:
        update = Coupon.objects.get(pk=id)
        form = CouponForm(instance=update)
        context={
            'form':form
        }
    return render(request,'adminpanel/updateCoupon.html',context)





#dashbord
def dashbord(request):
    today = datetime.today()
    today_date = today.strftime("%Y-%m-%d")
    month = today.month
    year = today.strftime("%Y")
    one_week = datetime.today() - timedelta(days=7)
    order_count_in_month = Order.objects.filter(created_at__year = year,created_at__month=month, is_ordered=True).count() 
    print('lo',order_count_in_month)
    order_count_in_day =Order.objects.filter(created_at = today, is_ordered=True).count()
    order_count_in_week = Order.objects.filter(created_at__gte = one_week, is_ordered=True).count()
    number_of_users  = CustomUser.objects.filter(is_superuser = False).count()
    print('user',number_of_users )
    paypal_orders = Payment.objects.filter(payment_method="Paypal",status = 'True').count()
    cash_on_delivery_count = Payment.objects.filter(payment_method="Cash on Delivery",status = 'True').count()
    wallet_payment = Payment.objects.filter(payment_method="Wallet payment",status = 'True').count()

    print('papal' ,cash_on_delivery_count)
    total_payment_count = paypal_orders  + cash_on_delivery_count + wallet_payment
    try:
        total_payment_amount = Payment.objects.filter(status = 'True').annotate(total_amount=Cast('amount_paid', FloatField())).aggregate(Sum('total_amount'))
        
    except:
        total_payment_amount=0
        
    if total_payment_amount['total_amount__sum'] :
      revenue = total_payment_amount['total_amount__sum']
      revenue = format(revenue, '.2f')
    
    else:
      revenue = 0
           
    blocked_user = CustomUser.objects.filter(is_active = False,is_superuser = False).count()
    unblocked_user = CustomUser.objects.filter(is_active = True,is_superuser = False).count()

    today_sale = Order.objects.filter(created_at = today_date,payment__status = 'True', is_ordered=True).count()
    print(today_sale)
    today = today.strftime("%A")
    new_date = datetime.today() - timedelta(days = 1)
    yester_day_sale =   Order.objects.filter(created_at = new_date,payment__status = 'True', is_ordered=True).count()  
    yesterday = new_date.strftime("%A")
    new_date = new_date - timedelta(days = 1)
    day_2 = Order.objects.filter(created_at = new_date,payment__status = 'True', is_ordered=True).count()
    day_2_name = new_date.strftime("%A")
    new_date = new_date - timedelta(days = 1)
    day_3 = Order.objects.filter(created_at = new_date,payment__status = 'True', is_ordered=True).count()
    day_3_name = new_date.strftime("%A")
    new_date = new_date - timedelta(days = 1)
    day_4 = Order.objects.filter(created_at = new_date,payment__status = 'True', is_ordered=True).count()
    day_4_name = new_date.strftime("%A")
    new_date = new_date - timedelta(days = 1)
    day_5 = Order.objects.filter(created_at = new_date,payment__status = 'True', is_ordered=True).count()
    day_5_name = new_date.strftime("%A")
    # #status
    ordered = Order.objects.filter(status = 'Order Confirmed', is_ordered=True).count()
    shipped = Order.objects.filter(status = "Shipped").count()
    out_of_delivery = Order.objects.filter(status ="Out for delivery").count()
    delivered = Order.objects.filter(status = "Delivered").count()
    returned = Order.objects.filter(status = "Returned").count()
    cancelled = Order.objects.filter(status = "Cancelled").count()

    context ={
        'order_count_in_month':order_count_in_month,
        'order_count_in_day':order_count_in_day,
        'order_count_in_week':order_count_in_week,
        'number_of_users':number_of_users,
        'paypal_orders':paypal_orders,
        'wallet_payment':wallet_payment,
        'total_payment_count':total_payment_count,
        'revenue':revenue,
        'ordered':ordered,
        'shipped':shipped,
        'out_of_delivery':out_of_delivery,
        'delivered':delivered,
        'returned':returned,
        'cancelled':cancelled,
        'cash_on_delivery_count':cash_on_delivery_count,
        'blocked_user':blocked_user,
        'unblocked_user':unblocked_user,
        'today_sale':today_sale,
        'yester_day_sale':yester_day_sale,
        'day_2':day_2,
        'day_3':day_3,
        'day_4':day_4,
        'day_5':day_5,
        'today':today,
        'yesterday':yesterday,
        'day_2_name':day_2_name,
        'day_3_name':day_3_name,
        'day_4_name':day_4_name,
        'day_5_name':day_5_name
        
    }
    return render(request, 'adminpanel/dashbord.html', context)






#sales report
def salesReport(request):
    year = datetime.now().year
    today = datetime.today()
    month = today.month
    years = []
    today_date=str(date.today())
    start_date=today_date
    end_date=today_date


    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        val = datetime.strptime(end_date, '%Y-%m-%d')
        end_date = val+timedelta(days=1)
        orders = Order.objects.filter(Q(created_at__lte=end_date),Q(created_at__gte=start_date),payment__status = 'True').values('user_order_page__product__product_name','user_order_page__product__stock',total = Sum('order_total'),).annotate(dcount=Sum('user_order_page__quantity')).order_by('-total')
        paginator = Paginator(orders,1)
        page= request.GET.get('page')
        paged_report = paginator.get_page(page) 
       
    else:
        orders = Order.objects.filter(created_at__year = year,created_at__month=month,payment__status = 'True').values('user_order_page__product__product_name','user_order_page__product__stock',total = Sum('order_total'),).annotate(dcount=Sum('user_order_page__quantity')).order_by('-total')
        paginator = Paginator(orders,7)
        page= request.GET.get('page')
        paged_report = paginator.get_page(page) 
        
    year = today.year
    for i in range (4):
        val = year-i
        years.append(val)

    


    context = {
        'orders':paged_report,
        'today_date':today_date,
        'years':years,
        'start_date':start_date,
        'end_date':end_date,
       
    }
    
    
    return render(request,'adminpanel/salesReport.html',context)



def salesReportMonth(request,id):
    orders = Order.objects.filter(created_at__month = id,payment__status = 'True').values('user_order_page__product__product_name','user_order_page__product__stock',total = Sum('order_total'),).annotate(dcount=Sum('user_order_page__quantity')).order_by()
    paginator = Paginator(orders,7)
    page= request.GET.get('page')
    paged_report = paginator.get_page(page) 
    today_date=str(date.today())
    context = {
        'orders':paged_report,
        'today_date':today_date
    }
    return render(request,'adminpanel/salesReportTable.html',context)

def salesReportYear(request,id):
    orders = Order.objects.filter(created_at__year = id,payment__status = 'True').values('user_order_page__product__product_name','user_order_page__product__stock',total = Sum('order_total'),).annotate(dcount=Sum('user_order_page__quantity')).order_by()
    paginator = Paginator(orders,7)
    page= request.GET.get('page')
    paged_report = paginator.get_page(page)    
    today_date=str(date.today())
    context = {
        'orders':paged_report,
        'today_date':today_date
    }
    return render(request,'adminpanel/salesReportTable.html',context) 



def pdfReport(request, start_date, end_date):
    year = datetime.now().year
    today = datetime.today()
    month = today.month
    
    if start_date == end_date:
      orders = Order.objects.filter(created_at__year = year,created_at__month=month,payment__status = 'True').values('user_order_page__product__product_name','user_order_page__product__stock',total = Sum('order_total'),).annotate(dcount=Sum('user_order_page__quantity')).order_by('-total')
    else:
      orders = Order .objects.filter(Q(created_at__lte=end_date),Q(created_at__gte=start_date),payment__status = 'True').values('user_order_page__product__product_name','user_order_page__product__stock',total = Sum('order_total'),).annotate(dcount=Sum('user_order_page__quantity')).order_by('-total')
    
    template_path = 'adminpanel/salesReportPdf.html'
    context = {'orders': orders,}
    
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=sales_report' + str(datetime.now()) +'.pdf'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
  
  
def excelReport(request, start_date, end_date):
    year = datetime.now().year
    today = datetime.today()
    month = today.month
    
    if start_date == end_date:
      orders = Order.objects.filter(created_at__year = year,created_at__month=month,payment__status = 'True').values_list('user_order_page__product__product_name', Sum('user_order_page__quantity'),'user_order_page__product__stock', Sum('order_total'))
    else:
      orders = Order.objects.filter(Q(created_at__lte=end_date),Q(created_at__gte=start_date),payment__status = 'True').values_list('user_order_page__product__product_name', Sum('user_order_page__quantity'),'user_order_page__product__stock', Sum('order_total'))
      
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=sales_report' + str(datetime.now()) +'.xls'
    
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Sales_report')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    
    columns = ['Item Name', 'Item sold', 'In stock', 'Amount Received']
    
    for col_num in range(len(columns)):
      ws.write(row_num, col_num, columns[col_num], font_style)
      
    font_style = xlwt.XFStyle()
    
    rows = orders
    
    for row in rows:
      row_num += 1

      for col_num in range(len(row)):
        ws.write(row_num, col_num, str(row[col_num]), font_style)
        
    wb.save(response)

    return response
    
    

  

