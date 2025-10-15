from django.db import models

# Create your models here.
class Form(models.Model):
    operation: models.CharField=models.CharField(max_length=100)

class Form_error(models.Model):
    error: models.CharField=models.CharField(max_length=100)
    email: models.CharField=models.CharField(max_length=100)
