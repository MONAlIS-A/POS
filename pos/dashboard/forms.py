from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from . models import Profile


# Registation
class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields= ['username', 'email']
        labels = {
            'email':'Email'
        }

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields =['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields =['address', 'phone', 'image']