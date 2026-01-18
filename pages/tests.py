from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone

from core.models import ParticipantRating
from pages.models import Posts

class ParticipantRatingTest(TestCase):
    """Тестирование системы оценок участников."""
    def setUp(self):
        self.user1 = User.objects.create_user(username='rater')
        self.user2 = User.objects.create_user(username='participant')
        self.post = Posts.objects.create(
            name='Тестовое мероприятие',
            user=self.user1,
            expiration_date=timezone.now()
        )
    def test_participant_rating_creation(self):
        """Проверка создания оценки для участника мероприятия"""
        rating = ParticipantRating.objects.create(
            rater=self.user1,
            participant=self.user2,
            post=self.post,
            was_late=False,
            would_repeat=True
        )

        self.assertEqual(rating.rater.username, 'rater')
        self.assertEqual(rating.participant.username, 'participant')
        self.assertFalse(rating.was_late)
        self.assertTrue(rating.would_repeat)
