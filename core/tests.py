from django.test import TestCase


class QuickTest(TestCase):
    def test_1(self):
        r = self.client.get('/register/')
        self.assertEqual(r.status_code, 200)

    def test_2(self):
        r = self.client.post('/register/', {
            'username': 'user1',
            'password1': 'pass1',
            'password2': 'pass1',
        })
        self.assertEqual(r.status_code, 302)
