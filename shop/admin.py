from django.contrib import admin
from .models import Products
# Register your models here.
class ProductsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('product_name',)}
    list_display = ('product_name','slug','is_available','price','sub_category','category','created_at','modified_at')
admin.site.register(Products,ProductsAdmin)