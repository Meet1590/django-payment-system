from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from .models import CustomUser

class CustomAuthBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None):

        try:
            # Your custom authentication logic goes here
            user = CustomUser.objects.get(email=email)
            if user.check_password(password):
                return user
        except CustomUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        CustomUser = get_user_model()
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None
