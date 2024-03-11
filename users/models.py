from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager,CustomTokenManager,PostManager
from django.conf import settings
from django.utils import timezone
class CustomUser(AbstractUser):
    username=None
    email=models.EmailField(_("Email Address"),unique=True)
    USERNAME_FIELD="email"
    updated_at=models.DateField(auto_now_add=True)
    REQUIRED_FIELDS=[]
    objects=CustomUserManager()

    # def __str__(self) -> str:
    #     return self.email
class Post(models.Model):
    title=models.CharField(_("post title"),max_length=20)
    content=models.CharField(_("post content"),max_length=200)
    userid=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now=True)
    objects=models.Manager()
    postManager=PostManager()
class CustomToken(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    objects=models.Manager()
    # c_token=CustomTokenManager()
    def __str__(self) -> str:
        return str(self.access_token)

# Create your models here.
