from celery import shared_task
from django.utils import timezone

from pages.models import Posts, PostParticipant
from .models import Notification

@shared_task
def check_expired_events():
    """Проверяет завершенные мероприятия и отправляет уведомления"""
    now = timezone.now()
    expired_posts = Posts.objects.filter(expiration_date__lt=now, is_active=True)

    for post in expired_posts:
        Notification.objects.create(
            post = post,
            user=post.user,
            title="Мероприятие завершено",
            message=f"Ваше мероприятие '{post.name}' завершено",
            notification_type='event_completed'
        )

        participants = PostParticipant.objects.filter(post=post)
        for participant in participants:
            Notification.objects.create(
                post = post,
                user=participant.user,
                title="Мероприятие завершено",
                message=f"Мероприятие '{post.name}', в котором вы участвовали, завершено",
                notification_type='event_completed'
            )

        post.is_active = False
        post.save()
