import os
from .models import Notification

def notifications_count(request):
    if request.user.is_authenticated:
        try:
            count = Notification.objects.filter(
                user=request.user,
                is_read=False
            ).count()
            return {'unread_notifications_count': count}
        except Exception:
            return {'unread_notifications_count': 0}
    return {'unread_notifications_count': 0}

def yandex_maps_api_key():
    return {'YANDEX_MAPS_API_KEY': os.environ.get('YANDEX_MAPS_API_KEY', '')}
