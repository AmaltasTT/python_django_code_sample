#crate forms here
from django import forms
from .models import RegisterVIP
from django.contrib.auth.forms import UserCreationForm

class RegisterVIPForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = RegisterVIP
        fields = ('name', 'mobile_number')
