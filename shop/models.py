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
    



