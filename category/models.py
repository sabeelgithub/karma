from django.db import models
from django.urls import reverse


# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=150,unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    created_at = models.DateField(auto_now=True)
    modified_at = models.DateField(auto_now=True)
    class Meta:
         verbose_name = 'category'
         verbose_name_plural = 'categories'
    def __str__(self):
         return self.category_name
    
class Sub_Category(models.Model):
  sub_category_name = models.CharField(max_length=50)
  slug = models.SlugField(max_length=50,unique=True)
  category= models.ForeignKey(Category,on_delete=models.CASCADE)
  created_at = models.DateField(auto_now=True)
  modified_at = models.DateField(auto_now=True)
  
  class Meta:
        verbose_name        = 'sub category'
        verbose_name_plural = 'sub categories'

  def __str__(self):
        return self.sub_category_name
   
   
    