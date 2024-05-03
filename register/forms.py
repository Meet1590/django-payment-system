from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import CustomUser


# RegisterForm inheriting UserCreationForm to mimic its functionalities with own developed version.
class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    currency = forms.ChoiceField(choices=CustomUser.currency_choices)

    class Meta:
        model = CustomUser
        fields = ["username", "firstName", "lastName", "email", "currency", "password1", "password2"]  # Form fields

    # Ensure that email is not already in use
    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        return email

    # Ensure that both password matches
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 != password2:
            raise ValidationError("Passwords do not match.")
        return cleaned_data


# CustomAuth form to feed custom backend.
class EmailAuthenticationForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=254)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ["email", "password"]
