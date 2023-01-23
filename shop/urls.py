from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop,name='shop'),
    path('sub_category/<slug:sub_category_slug>/', views.shop,name='product_by_sub_category'),
    path('sub_category/<slug:sub_category_slug>/<slug:product_slug>/', views.product_details,name='product_details'),
    path('dashbord/search/', views.search,name='search'),
    
    
]
