from django.db import models

# Create your models here.
class Person(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    country = models.CharField(max_length=50)
    email = models.EmailField()
    identity = models.CharField(max_length=14)
    cpf = models.CharField(max_length=14)
    phone = models.CharField(max_length=14)
