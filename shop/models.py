from django.db import models
from category.models import Sub_Category,Category
from django.urls import reverse

# Create your models here.
class Products(models.Model):
    product_name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100)
    description = models.CharField(max_length=255)
    price = models.IntegerField()
    image1 = models.ImageField(upload_to='potos/product')
    image2 = models.ImageField(upload_to='potos/product')
    image3 = models.ImageField(upload_to='potos/product')
    stock = models.IntegerField()
    is_available = models.BooleanField()
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    sub_category = models.ForeignKey(Sub_Category,on_delete=models.CASCADE)
    created_at = models.DateField(auto_now=True)
    modified_at = models.DateField(auto_now=True)
    def get_url(self):
         return reverse('product_details',args=[self.sub_category.slug,self.slug])
    def __str__(self):
         return self.product_name

class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager,self).filter(variation_category='color',is_active=True)
    def sizes(self):
        return super(VariationManager,self).filter(variation_category='size',is_active=True)

variation_category_choices = (
     ('color','color'),
      ('size','size'),
)    
class  Variation(models.Model):
     product = models.ForeignKey(Products,on_delete=models.CASCADE)
     variation_category = models.CharField(max_length=100,choices=variation_category_choices)
     variation_value = models.CharField(max_length=100)
     is_active = models.BooleanField(default=True)
     created_at =  models.DateField(auto_now=True)

     objects = VariationManager()

     def __str__(self):
        return self.variation_value   
    



