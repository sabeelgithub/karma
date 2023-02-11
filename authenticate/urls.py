from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login,name='login'),
    path('signup/', views.signup,name='signup'),
    path('mobile/', views.mobile,name='mobile'),
    path('logout/', views.logout,name='logout'),
    path('verify_code/', views.verify_code, name='verify_code'),
    path('mobilelogin/', views.mobilelogin, name='mobilelogin'), 
    path('verify_codelogin/', views.verify_codelogin, name='verify_codelogin'),
   
    
        
]
