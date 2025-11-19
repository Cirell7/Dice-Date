from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский'),
        ('prefer-not-to-say', 'Предпочитаю не говорить'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(
        max_length=20, 
        choices=GENDER_CHOICES,  
        blank=True, 
        null=True
    )
    birth_date = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    likes_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

class Form_error(models.Model):
    error: models.CharField=models.CharField(max_length=100)
    email: models.CharField=models.CharField(max_length=100)