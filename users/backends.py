from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.base_user import AbstractBaseUser
from .models import CustomUser
# from django.contrib.auth.models import User
class CustomAuthBackend(BaseBackend):
    def get_user(self, email: int) -> AbstractBaseUser | None:
        return super().get_user(email)
    def authenticate(self, request,password=None,email=None):
        user = CustomUser.objects.get(email=email)
        # hp=user.set_password(user.password)
        # print(hp)
        print(user.email)
        print(user.password)
        print("in CustomAuthBackend")
        if user.check_password(password):
            return user