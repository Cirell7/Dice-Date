from django.db import models

# Create your models here.
class Form_error(models.Model):
    error: models.CharField=models.CharField(max_length=100)
    email: models.CharField=models.CharField(max_length=100)

class Profile(models.Model):
    gender: models.CharField=models.CharField(max_length=100)
    age: models.CharField=models.CharField(max_length=100)
