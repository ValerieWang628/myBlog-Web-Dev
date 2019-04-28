from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegisForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        # whenever the form validates, it is going to create a new user object
        fields = ['username', 'email', 'password1', 'password2']
        # these are what to be shown in the regisForm