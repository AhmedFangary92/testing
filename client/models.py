from django.db import models
from django.contrib.auth.models import User


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=('اسم المستخدم'))
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name=('رقم الجوال'))
    
    class Meta:
        verbose_name_plural ='المستخدمين'

    def __str__(self) :
        return self.user.username
