from django.db import models
from django.contrib.auth.models import User

from django.core.files.storage import default_storage

class Form_error(models.Model):
    error: models.CharField=models.CharField(max_length=100)
    email: models.CharField=models.CharField(max_length=100)

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
    photo = models.ImageField(upload_to='profile_photos/',
    blank=True, null=True, storage=default_storage)
    description = models.TextField(blank=True, null=True)
    likes_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('join_request', 'Заявка на участие'),
        ('request_approved', 'Заявка одобрена'),
        ('request_rejected', 'Заявка отклонена'),
        ('new_message', 'Новое сообщение'),
        ('system', 'Системное уведомление'),
        ('event_completed', 'Мероприятие завершено'),
    ]
    post = models.ForeignKey('pages.Posts', on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='system')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.user.username}"

class ParticipantRating(models.Model):
    rater = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_ratings')
    participant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_ratings')
    post = models.ForeignKey('pages.Posts', on_delete=models.CASCADE, null=True, blank=True)
    was_late = models.BooleanField(null=True)
    would_repeat = models.BooleanField(null=True)
    rated_at = models.DateTimeField(auto_now_add=True)
