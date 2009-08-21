from django.db import models

# Create your models here.
class Person(models.Model):
  name = models.CharField(max_length=30)
  address = models.CharField(max_length=50)
  city = models.CharField(max_length=60)
  country = models.CharField(max_length=50)
  email = models.EmailField()
  identity = models.CharField(max_length=14, unique=True)
  cpf = models.CharField(max_length=14, unique=True)
  phone = models.CharField(max_length=14)

  def __unicode__(self):
    return self.cpf + ' - ' + self.name


class Car(models.Model):
  company = models.CharField(max_length=30)
  model = models.CharField(max_length=30)
  date = models.DateField('Date of purchase')
  chaci = models.CharField(max_length=50)
  color = models.CharField(max_length=10)
  plate = models.CharField(max_length=10)
  owner = models.ForeignKey('Person')

