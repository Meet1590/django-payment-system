from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.core import validators
from rest_framework.exceptions import ValidationError


# Data validator for username field of CustomUser
def custom_slug_validator(value):
    validators.validate_slug(value)  # Use Django's built-in slug validator
    if len(value) < 0:
        raise ValidationError('Username required!.')


# Create your models here.

# CustomUser Model (User table in terms of dbms)
class CustomUser(AbstractUser):
    username = models.SlugField(max_length=10, unique=True, validators=[custom_slug_validator],
                                error_messages={'unique': "A user with that username already exists."})
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    currency_choices = [
        ('GBP', 'British Pound'),
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
    ]
    currency = models.CharField(max_length=3, choices=currency_choices)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=1000.00)

    # Mapping relations (Cardinalities)
    groups = models.ManyToManyField(Group, related_name='custom_user_set')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set')

    def __str__(self):
        return self.username


# CustomUser group and permission setting to override default policies if required in the future.
class CustomGroup(Group):
    class Meta:
        proxy = True


class CustomPermission(Permission):
    class Meta:
        proxy = True
