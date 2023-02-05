from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from .models import Order,Payment,Address
from shop.models import Variation
from carts.models import CartItem
from .forms import OrderForm
import datetime
from .models import Payment,OrderProduct,Order,Coupon,UserCoupon
import json

# Create your views here.
def payments(request):
   body = json.loads(request.body)
   order = Order.objects.get(user=request.user,is_ordered=False,order_number=body['orderID'])
   payment = Payment(
      user = request.user,
      payment_id = body['transID'],
      order_id = order.order_number,
      payment_method = body['payment_method'],
      amount_paid = order.order_total,
      status = body['status'],
   )
   payment.save()
   order.payment = payment
   order.is_ordered = True
   order.save()
   # move the cart item in to oredr product table
   cart_items = CartItem.objects.filter(user=request.user)
   for item in cart_items:
      order_product = OrderProduct()
      order_product.order_id = order.id
      order_product.payment = payment
      order_product.user_id = request.user.id
      order_product.product_id = item.product_id
      order_product.quantity = item.quantity
      order_product.product_price = item.product.price
      order_product.ordered = True
      order_product.save()

      cart_item = CartItem.objects.get(id=item.id)
      product_variation = cart_item.variations.all()
      order_product = OrderProduct.objects.get(id=order_product.id)
      order_product.variations.set(product_variation)
      order_product.save()

      # reduce the Quantity
      variation = Variation.objects.filter(id__in= cart_item.variations.all())
         
      for var in variation:
         var.stock -= cart_item.quantity
         var.save()
         print('ann')

   # clear cart
   CartItem.objects.filter(user=request.user).delete()
   
   # send order number transaction id back to send data method via jsonResponce
   data = {
      'order_number':order.order_number,
      'transID':payment.payment_id
   }
   print('boss')
   return JsonResponse(data)

def payments_completed(request):
   order_number = request.GET.get('order_number')
   transID = request.GET.get('payment_id')
   print(transID, "testing transid")
   try:
      print('jis')
      order = Order.objects.get(order_number=order_number)
      print('lofi')
      ordered_products = OrderProduct.objects.filter(order_id=order.id)
      print('break')
      # payment = Payment.objects.get(payment_id=transID)
      print('mallayya')
      total = 0
      for i in ordered_products:
           total += i.product_price * i.quantity
      tax = (2*total)/100
      
      print('check')
      grand_total = total + tax 
      payment = Payment.objects.get(payment_id=transID)
      context={
         'order':order,
         'ordered_products':ordered_products,
         'order_number':order.order_number,
         'transID':payment.payment_id,
         'payment':payment,
         'total':total,
         'tax':tax,
         'grand_total':grand_total,
      }
      return render(request,'payment_success.html',context)
   except Exception as e:
      print(e)
      print('kashtam')
      return redirect('home')
   
# def place_order(request,total=0,quantity=0):
#     current_user = request.user

#     # if the cart count is less than or equal to 0,then redirect back to shop
#     cart_items = CartItem.objects.filter(user=current_user)
#     cart_count = cart_items.count()
#     if cart_count <= 0:
#       return redirect('shop')
    
#     grand_total = 0
#     tax = 0
#     for cart_item in cart_items:
#        total += (cart_item.product.price * cart_item.quantity)
#        quantity += cart_item.quantity
#     tax =(2 * total)/100
#     grand_total = total + tax     
    
#     if request.method == 'POST':
#        form = OrderForm(request.POST)
#        if form.is_valid():
#           # store all the billing information inside order table
#           data = Order()
#           data.user = current_user
#           data.first_name = form.cleaned_data['first_name']
#           data.last_name = form.cleaned_data['last_name']
#           data.phone = form.cleaned_data['phone']
#           data.email = form.cleaned_data['email']
#           data.address_line_1 = form.cleaned_data['address_line_1']
#           data.address_line_2 = form.cleaned_data['address_line_2']
#           data.country = form.cleaned_data['country']
#           data.state = form.cleaned_data['state']
#           data.city = form.cleaned_data['city']
#           data.order_note = form.cleaned_data['order_note']
#           data.order_total = grand_total
#           data.tax = tax 
#           data.ip = request.META.get('REMOTE_ADDR')
#           data.save()

#           # generate order number
#           yr = int(datetime.date.today().strftime('%Y'))
#           dt = int(datetime.date.today().strftime('%d'))
#           mt = int(datetime.date.today().strftime('%m'))
#           d = datetime.date(yr,mt,dt)
#           current_date = d.strftime("%Y%m%d")
#           order_number = current_date + str(data.id)
#           data.order_number = order_number
#           data.save()

#           order = Order.objects.get(user=current_user,is_ordered=False,order_number=order_number)
#           context={
#              'order':order,
#              'cart_items':cart_items,
#              'total':total,
#              'tax':tax,
#              'grand_total':grand_total,
#              'order_number':order_number

#           }
#           return render(request,'payments.html',context)
#        else:
#           print('form not valid')
#           return redirect('checkout')
       
def place_order(request,total=0,quantity=0):
    current_user = request.user

    # if the cart count is less than or equal to 0,then redirect back to shop
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
      return redirect('shop')
    
    grand_total = 0
    tax = 0
    for cart_item in cart_items:
       total += (cart_item.product.price * cart_item.quantity)
       quantity += cart_item.quantity
    tax =(2 * total)/100
    grand_total = total + tax    

    

    
    if request.method == 'POST':
          id = request.POST['flexRadioDefault']
          address  = Address.objects.get(user = request.user,id = id)
          data = Order()
          data.user = current_user
          data.first_name = address.first_name
          data.last_name = address.last_name
          data.phone = address.phone
          data.email = address.email
          data.address_line_1 = address.address_line1
          data.address_line_2 = address.address_line2
          data.state = address.state
          data.city = address.city
          data.country = address.country
          data.order_note = address.order_note
          data.order_total = grand_total
          data.tax = tax 
          data.ip = request.META.get('REMOTE_ADDR')
          data.save()

          # generate order number
          yr = int(datetime.date.today().strftime('%Y'))
          dt = int(datetime.date.today().strftime('%d'))
          mt = int(datetime.date.today().strftime('%m'))
          d = datetime.date(yr,mt,dt)
          current_date = d.strftime("%Y%m%d")
          order_number = current_date + str(data.id)
          data.order_number = order_number
          data.save()

          order = Order.objects.get(user=current_user,is_ordered=False,order_number=order_number)


          context={
             'order':order,
             'cart_items':cart_items,
             'total':total,
             'tax':tax,
             'grand_total':grand_total,
             'order_number':order_number,
             

          }
          return render(request,'payments.html',context)
    else:
          print('form not valid')
          return redirect('checkout')

def cash_on_delivery(request,id):
   # Move cart item to ordered product table
   try:
      
      order = Order.objects.get(user=request.user,is_ordered=False,order_number=id)
      cart_items = CartItem.objects.filter(user=request.user)
      order.is_ordered = True
      payment = Payment(
         user = request.user,
         payment_id = order.order_number,
         order_id = order.order_number,
         payment_method = 'Cash on Delivery',
         amount_paid = order.order_total,
         status = False
      )
      payment.save()
      order.payment = payment
      order.is_ordered = True
      order.save()
      print('dill')
      
      for cart_item in cart_items:
         order_product = OrderProduct()
         order_product.order_id = order.id
         order_product.payment = payment
         order_product.user_id = request.user.id
         order_product.product_id = cart_item.product_id
         order_product.quantity = cart_item.quantity
         order_product.product_price = cart_item.product.price
         order_product.ordered = True
         print('les')
         print(order_product.order_id)
         order_product.save()

         cart_item = CartItem.objects.get(id=cart_item.id)
         product_variation = cart_item.variations.all()
         print
         order_product = OrderProduct.objects.get(id=order_product.id)
         print(order_product.variations)
         print('juuum')
         order_product.variations.set(product_variation)
         print('heeeeeeeeeeeeeeeee')
         order_product.save()

         # # Reduce quantity of product
         print('mooooo')
         print(cart_item.id)
         print(type(cart_item.variations))
         print(cart_item.variations.all())
         test = cart_item.variations.all()[0]
         print(test)
         variation = Variation.objects.filter(id__in= cart_item.variations.all())
         for var in variation:
          var.stock -= cart_item.quantity
          var.save()
          print('ann')

         #clear cart
         print('lala')
      CartItem.objects.filter(user= request.user).delete()

      ordered_products = OrderProduct.objects.filter(order_id = order.id)

      total = 0
      for i in ordered_products:
           total += i.product_price * i.quantity
      tax = (2*total)/100
      shipping = (2*total)/100
      grand_total = total + tax + shipping

      context ={
            'order':order,
            'ordered_products':ordered_products,
            'payment':payment,
            'total':total,
            'tax':tax,
            'shipping':shipping,
            'grand_total':grand_total
         }  
      return render(request,'cod_success.html',context) 
   except Exception as e:
      print(e)
      return redirect('home')
      


def cancel_order(request,id):
    if request.user.is_superuser:
      order = Order.objects.get(order_number = id)
    else:
      order = Order.objects.get(order_number = id,user = request.user)
    order.status = "Cancelled"
    order.save()
    payment = Payment.objects.get(order_id = order.order_number)
    payment.delete()
    order_product = OrderProduct.objects.get(user=request.user,order=order)
    print(order_product.variations)
    variation = Variation.objects.filter(id__in= order_product.variations.all())
    print(variation)
    for var in variation:
         var.stock += order_product.quantity
         var.save()
         print('ann')
    if request.user.is_superuser:
      return redirect('orders')
    else:
      return redirect('my_orders')
    

def return_order(request, id):
  print("loooooo")
  if request.method == 'POST':
    print('helloooooooooooooooo')
    return_reason = request.POST['return_reason']
  print(return_reason)
  order = Order.objects.get(order_number = id,user = request.user)
  order.status = "Returned"
  order.is_returned = True
  order.return_reason = return_reason
  order.save()
  payment = Payment.objects.get(order_id = order.order_number)
  print("order get")
  payment.delete()
  order_product = OrderProduct.objects.get(user=request.user,order=order)
  print(order_product.variations)
  variation = Variation.objects.filter(id__in= order_product.variations.all())
  print(variation)
  for var in variation:
         var.stock += order_product.quantity
         var.save()
         print('ann')

         

  return redirect('my_orders')





# def coupon(request):
#   if request.method == 'POST':
#     coupon_code = request.POST['coupon']
#     grand_total = request.POST['grand_total']
#     coupon_discount = 0
#     try:
#       instance = UserCoupon.objects.get(user = request.user ,coupon__code = coupon_code)

#       if float(grand_total) >= float(instance.coupon.min_value):
#         coupon_discount = ((float(grand_total) * float(instance.coupon.discount))/100)
#         grand_total = float(grand_total) - coupon_discount
#         grand_total = format(grand_total, '.2f')
#         coupon_discount = format(coupon_discount, '.2f')
#         msg = 'Coupon Applied successfully'
#         instance.used = True
#         instance.save()
#       else:
#           msg='This coupon is only applicable for orders more than ₹'+ str(instance.coupon.min_value)+ '\- only!'
#     except:
#             msg = 'Coupon is not valid'
#     response = {
#                'grand_total': grand_total,
#                'msg':msg,
#                'coupon_discount':coupon_discount,
#                'coupon_code':coupon_code,
#                 }

#   return JsonResponse(response)






def coupons(request):
  if request.method == 'POST':
    coupon_code = request.POST['coupon']
    grand_total = request.POST['grand_total']
    coupon_discount = 0
    try:
      instance = UserCoupon.objects.get(user = request.user ,coupon__code = coupon_code)

      if float(grand_total) >= float(instance.coupon.min_value):
        coupon_discount = ((float(grand_total) * float(instance.coupon.discount))/100)
        grand_total = float(grand_total) - coupon_discount
        grand_total = format(grand_total, '.2f')
        coupon_discount = format(coupon_discount, '.2f')
        msg = 'Coupon Applied successfully'
        instance.used = True
        instance.save()
      else:
          msg='This coupon is only applicable for orders more than ₹'+ str(instance.coupon.min_value)+ '\- only!'
    except:
            msg = 'Coupon is not valid'
    response = {
               'grand_total': grand_total,
               'msg':msg,
               'coupon_discount':coupon_discount,
               'coupon_code':coupon_code,
                }

  return JsonResponse(response)


