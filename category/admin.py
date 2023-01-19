from django.contrib import admin
from .models import Category,Sub_Category
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('category_name',)}
    list_display = ('category_name','slug','created_at','modified_at')
admin.site.register(Category,CategoryAdmin)
class Sub_CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('sub_category_name',)}
    list_display = ('sub_category_name','slug','category','created_at','modified_at')
admin.site.register(Sub_Category,Sub_CategoryAdmin)    