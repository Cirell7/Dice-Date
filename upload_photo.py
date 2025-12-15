import os
import django

from django.core.files import File
from core.models import Profile 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

test_path = 'test_photo.jpg'
with open(test_path, 'wb') as f:
    f.write(b'test_image_content')

profile = Profile.objects.first()

with open(test_path, 'rb') as f:
    profile.photo.save('test_from_shell.jpg', File(f), save=True)

os.remove(test_path)

