from django import forms
from .models import CustomUser
from home.models import UserProfile

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name','last_name','phone','email')

    def __init__(self,*args,**kwargs):
        super(CustomUserForm,self).__init__(*args,**kwargs)   

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False,error_messages={'invalid':("image files only")},widget=forms.FileInput) 
    class Meta:
        model = UserProfile
        fields = ('address_line_1','address_line_2','city','state','country','profile_picture')

    def __init__(self,*args,**kwargs):
        super(UserProfileForm,self).__init__(*args,**kwargs)   

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'