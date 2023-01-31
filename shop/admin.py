from django.contrib import admin
from .models import Products,Variation
# Register your models here.
class ProductsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('product_name',)}
    list_display = ('product_name','slug','is_available','price','sub_category','category','created_at','modified_at')
admin.site.register(Products,ProductsAdmin)
class VariationAdmin(admin.ModelAdmin):
    list_display = ('product','variation_category','variation_value','stock','is_active','created_at')
    list_editable = ('is_active',)
    list_filter = ('product','variation_category','variation_value')
admin.site.register(Variation,VariationAdmin)
