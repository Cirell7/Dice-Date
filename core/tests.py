from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from core.models import Profile, Form_error
from core.forms import RegisterForm

class CoreModelsTest(TestCase):
    """Тестирование core"""
    def setUp(self):
        """Создание тестовых данных перед каждым тестом."""
        self.user = User.objects.create_user(
            username='vasua',
            email='example@example.com',
            password='12345'
        )
    def test_profile_creation(self):
        """Проверка, что профиль создаётся вместе с пользователем."""
        profile = Profile.objects.create(
            user=self.user,
            gender='M',
            description='Текст'
        )
        self.assertEqual(profile.user.username, 'vasua')
        self.assertEqual(profile.gender, 'M')
        self.assertEqual(profile.likes_count, 0)

    def test_form_error_creation(self):
        """Проверка создания Form_error"""
        error = Form_error.objects.create(
            error='Текст',
            email='example@example.com'
        )
        self.assertEqual(error.error, 'Текст')
        self.assertEqual(error.email, 'example@example.com')

class RegisterFormTest(TestCase):
    """Тестирование формы регистрации"""
    def setUp(self):
        """Базовые валидные данные для формы"""
        self.valid_form_data = {
            'username': 'vasua',
            'email': 'example@example.com',
            'password': '12345'
        }

    def test_valid_form(self):
        """Проверка формы регистрации"""
        form = RegisterForm(data=self.valid_form_data)
        self.assertTrue(form.is_valid())

    def test_username_too_short(self):
        """Проверка имени пользователя"""
        test_data = self.valid_form_data.copy()
        test_data['username'] = 'ab'
        form = RegisterForm(data=test_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

    def test_invalid_email(self):
        """Проверка email"""
        test_data = self.valid_form_data.copy()
        test_data['email'] = 'invalid-email'
        form = RegisterForm(data=test_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_form_save(self):
        """Проверка создания пользователя через форму save()"""
        save_data = {
            'username': 'formuser',
            'email': 'form@example.com',
            'password': 'formpass123'
        }
        form = RegisterForm(data=save_data)
        self.assertTrue(form.is_valid())

        user = form.save()
        self.assertEqual(user.username, 'formuser')
        self.assertEqual(user.email, 'form@example.com')
        self.assertTrue(user.check_password('formpass123'))

class ProfileImageTest(TestCase):
    """Тестирование загрузки изображений в профиль"""
    def test_profile_with_image(self):
        """Проверка, что профиль может иметь изображение."""
        user = User.objects.create_user(username='imageuser')

        test_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'image',
            content_type='image/jpeg'
        )

        profile = Profile.objects.create(
            user=user,
            photo=test_image
        )

        self.assertIsNotNone(profile.photo)
        self.assertTrue('profile_photos' in profile.photo.name)
