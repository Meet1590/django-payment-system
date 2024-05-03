from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from .models import CustomUser


# Customized authentication backend with email as per requirements instead of username as in general.
class CustomAuthBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        """

        :param request: https request
        :param email: user's email that he/she entered in form
        :param password: password entered in form
        :return: authenticated user or None
        """
        try:
            # Your custom authentication logic goes here
            user = CustomUser.objects.get(email=email)
            if user.check_password(password):
                return user
        except CustomUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        """

        :param user_id: user identifier
        :return: user with given identifier
        """
        CustomUser = get_user_model()

        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None
