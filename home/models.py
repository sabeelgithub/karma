from django.db import models
from authenticate.models import CustomUser

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    address_line_1 = models.CharField(blank=True,max_length=100)
    address_line_2 = models.CharField(blank=True,max_length=100)
    profile_picture = models.ImageField(blank=True,upload_to='userprofile')
    city = models.CharField(blank=True,max_length=20)
    state = models.CharField(blank=True,max_length=20)
    country = models.CharField(blank=True,max_length=20)

    def __str__(self):
        return self.user.first_name
    def full_address(self):
        return f'{self.address_line_1}{self.address_line_2}'