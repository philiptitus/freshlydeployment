from django import forms
from .models import Product, Service, Blog, Garden
from django.utils.text import slugify
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm,PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
import bleach


class SignUpForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class GardenForm(forms.ModelForm):
    class Meta:
        model = Garden
        fields = [ 'name', 'location', 'size','features', 'description']
        
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'desc', 'price', 'image']

class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['type', 'description', 'price']




class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'slug', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['slug'].required = False  # Make slug field optional
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['content'].widget.attrs.update({'class': 'form-control'})
        self.fields['slug'].widget.attrs.update({'class': 'form-control'})
        self.fields['image'].widget.attrs.update({'class': 'form-control'})

    def clean_title(self):
        title = self.cleaned_data.get('title')
        sanitized_title = bleach.clean(title, strip=True)
        return sanitized_title 
    
    def clean_content(self):
        content = self.cleaned_data.get('content')
        sanitized_content = bleach.clean(content, tags=['p', 'b', 'i', 'u', 'a'], attributes={'a': ['href']})
        return sanitized_content
    def save(self, *args, **kwargs):
        instance = super().save(commit=False)
        if not instance.slug:
            instance.slug = slugify(instance.title)
        instance.save()
        return instance

# authentication forms
class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Old Password', widget=forms.PasswordInput(attrs={'autofocus' : 'true', 'autocomplete': 'current-password', 'class':'form-control'}))
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={'autofocus' : 'true', 'autocomplete': 'current-password', 'class':'form-control'}))
    new_password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'autofocus' : 'true', 'autocomplete': 'current-password', 'class':'form-control'}))

class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))


class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={'autofocus' : 'true', 'autocomplete': 'current-password', 'class':'form-control'}))
    new_password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'autofocus' : 'true', 'autocomplete': 'current-password', 'class':'form-control'}))
