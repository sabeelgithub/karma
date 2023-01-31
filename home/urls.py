from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name='home'),
    path('profile/', views.profile,name='profile'),
    path('userdash/', views.userdash,name='userdash'),
    path('my_orders/', views.my_orders,name='my_orders'),
    path('edit_profile/', views.edit_profile,name='edit_profile'),
    path('change_password/', views.change_password,name='change_password'),
    path('order_details/<int:order_id>/', views.order_details,name='order_details'),
]
