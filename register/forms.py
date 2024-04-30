from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser



class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    currency = forms.ChoiceField(choices=CustomUser.currency_choices)

    class Meta:
        model = CustomUser
        fields = ["username", "firstName", "lastName", "email", "currency", "password1", "password2"]


# class EmailAuthenticationForm(AuthenticationForm):
class EmailAuthenticationForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=254)
    password = forms.CharField(label='Password',widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ["email", "password"]
