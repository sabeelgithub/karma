from django.urls import path
from . import views

urlpatterns = [
    path('', views.adminlogin,name='adminlogin'),
    path('dashbord/', views.dashbord,name='dashbord'),
    path('adminlogout/', views.adminlogout,name='adminlogout'),
    path('users/', views.users,name='users'),
    path('<int:id>/blockuser/', views.blockuser, name='blockuser'),
    path('admincategory/', views.admincategory,name='admincategory'),
    path('<int:id>/delete_category/', views.delete_category,name='delete_category'),
    path('<int:id>/update_category/', views.update_category,name='update_category'),
    path('add_category/', views.add_category,name='add_category'),
    path('adminsub_category/', views.adminsub_category,name='adminsub_category'),
    path('<int:id>/delete_sub_category/', views.delete_sub_category,name='delete_sub_category'),
    path('<int:id>/update_sub_category/', views.update_sub_category,name='update_sub_category'),
    path('add_sub_category/', views.add_sub_category,name='add_sub_category'),
    path('adminproduct/', views.adminproduct,name='adminproduct'),
    path('add_product/', views.add_product,name='add_product'),
    path('<int:id>/delete_product/', views.delete_product,name='delete_product'),
    path('<int:id>/update_product/', views.update_product,name='update_product'),
    path('admin_search/', views.admin_search,name='admin_search'),     

       
]
