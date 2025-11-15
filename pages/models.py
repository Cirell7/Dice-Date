from django.db import models
from django.contrib.auth.models import User

class Posts(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    address = models.CharField(max_length=200, blank=True)
    max_participants = models.IntegerField(default=10)

# Create your models here.

class Profile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский'),
        ('O', 'Другой'),
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

class Comment(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)