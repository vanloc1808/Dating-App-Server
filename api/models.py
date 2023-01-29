from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class User(models.Model):
    hash_email = models.CharField(max_length=64, primary_key=True)
    email = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=64)
    phone_number = PhoneNumberField(region='VN')

    def __str__(self) -> str:
        return self.email