from django import forms
from category.models import Category,Sub_Category
from shop.models import Products
class Update_categoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name','slug']
        labels ={
            'category_name':'category name',
        }  
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name','slug'] 
        labels ={
            'category_name':'category name',

        }       
class Update_sub_categoryForm(forms.ModelForm):
    class Meta:
        model = Sub_Category
        fields = ['sub_category_name','slug']
        labels ={
            'sub_category_name':'sub category name',
        }  
class Sub_CategoryForm(forms.ModelForm):
    class Meta:
        model = Sub_Category
        fields = ['sub_category_name','slug','category'] 
        labels ={
            'sub_category_name':' sub Category name',

        }    
class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['product_name','slug','description','price','image1','image2','image3','stock','is_available','category','sub_category'] 
        labels ={
            'product_name':'product name',
            'description':'description',
            'price':'price',
            'image1':'image 1',
            'image2':'image 2',
            'image3':'image 3',
            'stock':'stock',
            'is_available':'is available',
            'category':'category',
            'sub_category':'sub category',
            



        }
class Update_ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['product_name','slug','description','price','image1','image2','image3','stock','is_available','category','sub_category'] 
        labels ={
            'product_name':'product name',
            'description':'description',
            'price':'price',
            'image1':'image 1',
            'image2':'image 2',
            'image3':'image 3',
            'stock':'stock',
            'is_available':'is available',
            'category':'category',
            'sub_category':'sub category',
           



        }                                                                    