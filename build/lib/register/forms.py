from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from django.contrib.auth import authenticate


class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    currency = forms.ChoiceField(choices=CustomUser.currency_choices)

    class Meta:
        model = CustomUser
        fields = ["username", "firstName", "lastName", "email", "currency", "password1", "password2"]


class EmailAuthenticationForm(AuthenticationForm):
    email = forms.EmailField(label='Email', max_length=254)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ["email", "password"]
