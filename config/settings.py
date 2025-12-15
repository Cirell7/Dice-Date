"""
Django settings for config project.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Загружаем .env ТОЛЬКО локально
if 'RENDER' not in os.environ:
    load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# ========== БЕЗОПАСНЫЕ НАСТРОЙКИ ==========
SECRET_KEY = os.environ['SECRET_KEY']

# Определяем режим работы
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = []

# Автоматическая настройка для Render
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')

print("="*60)
print(f"Начальная конфигурация:")
print(f"RENDER_EXTERNAL_HOSTNAME: {RENDER_EXTERNAL_HOSTNAME}")
print(f"DEBUG: {DEBUG}")
print("="*60)

# ========== БАЗОВЫЙ СПИСОК ПРИЛОЖЕНИЙ ==========
# ОДИН общий список для всех режимов, добавляем только специфичные настройки
BASE_INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Твои приложения
    "core",
    "pages",
    "dashboard",
    "notifications",
    # Celery для периодических задач - ДОБАВЛЕНО!
    'django_celery_beat',
]

# После ALLOWED_HOSTS добавьте:
if RENDER_EXTERNAL_HOSTNAME:
    # ========== НАСТРОЙКИ ДЛЯ RENDER (ПРОДАКШЕН) ==========
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
    ALLOWED_HOSTS.append('dice-date.onrender.com')
    DEBUG = False
    
    print(f"⚡ РЕЖИМ: Render (продакшен) - {RENDER_EXTERNAL_HOSTNAME}")
    
    # Безопасность
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    
    # CSRF trusted origins
    CSRF_TRUSTED_ORIGINS = [
        f'https://{RENDER_EXTERNAL_HOSTNAME}',
        'https://dice-date.onrender.com'
    ]
    
    # ========== НАСТРОЙКИ BUCKET.RU ДЛЯ МЕДИАФАЙЛОВ ==========
    # Создаём FINAL_INSTALLED_APPS на основе BASE_INSTALLED_APPS
    INSTALLED_APPS = BASE_INSTALLED_APPS.copy()
    INSTALLED_APPS.insert(6, 'storages')  # Добавляем storages после статических приложений
    
    # Ключи доступа (будут браться из переменных окружения Render)
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    
    # Данные из вашего бакета
    AWS_STORAGE_BUCKET_NAME = 'dice-date-media'
    AWS_S3_ENDPOINT_URL = 'https://s3.buckets.ru/'
    AWS_S3_CUSTOM_DOMAIN = '4cc1f6c9d8c50c34b1d3549ee76a4709.bckt.ru'
    AWS_S3_REGION_NAME = 'ru-1'
    
    # URL для медиафайлов теперь ведёт в Bucket.ru
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/'
    
    # Дополнительные настройки для корректной работы
    AWS_DEFAULT_ACL = 'public-read'      # Файлы будут публичными
    AWS_QUERYSTRING_AUTH = False         # Не добавлять подпись к URL файлов
    AWS_S3_FILE_OVERWRITE = False        # Не перезаписывать файлы с одинаковыми именами
    AWS_S3_SIGNATURE_VERSION = 's3v4'
    AWS_S3_ADDRESSING_STYLE = 'virtual'  # Важно для совместимости
    
    # ========== ВАЖНО: НОВЫЙ ФОРМАТ ДЛЯ DJANGO 5.x ==========
    # ВМЕСТО DEFAULT_FILE_STORAGE используем STORAGES
    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
            "OPTIONS": {
                "location": "",  # Файлы в корне бакета
                "file_overwrite": False,
                "querystring_auth": False,
                "default_acl": "public-read",
            },
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }
    
    # Статика через Whitenoise
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    
    print(f"✅ S3 настроен для bucket: {AWS_STORAGE_BUCKET_NAME}")
    print(f"🔑 S3 ключ доступен: {'ДА' if AWS_ACCESS_KEY_ID else 'НЕТ'}")
    print(f"🌐 Media URL: {MEDIA_URL}")
    
else:
    # ========== ЛОКАЛЬНАЯ РАЗРАБОТКА ==========
    ALLOWED_HOSTS.extend(['localhost', '127.0.0.1', '0.0.0.0'])
    DEBUG = os.environ.get('DEBUG', 'True') == 'True'
    
    print("💻 РЕЖИМ: Локальная разработка")
    
    # Локальные настройки
    INSTALLED_APPS = BASE_INSTALLED_APPS.copy()  # Используем базовый список
    
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    
    # Локальные хранилища
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }

# ========== БАЗОВЫЕ НАСТРОЙКИ (ОБЩИЕ) ==========
APPEND_SLASH = False

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.notifications_count',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# ========== БАЗА ДАННЫХ ==========
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ========== ВАЛИДАТОРЫ ПАРОЛЕЙ ==========
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# ========== ЯЗЫК И ВРЕМЯ ==========
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

# ========== СТАТИЧЕСКИЕ ФАЙЛЫ ==========
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

# ========== ОСТАЛЬНЫЕ НАСТРОЙКИ ==========
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ========== НАСТРОЙКИ CELERY (ОБНОВЛЕНО ДЛЯ BEAT) ==========
REDIS_URL = os.environ.get('REDIS_URL')
if REDIS_URL:
    CELERY_BROKER_URL = REDIS_URL
    CELERY_RESULT_BACKEND = REDIS_URL
else:
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Europe/Moscow'

# ========== ВАЖНО: НАСТРОЙКА CELERY BEAT ==========
# Указываем планировщик для периодических задач
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
print(f"✅ Celery Beat настроен с планировщиком: {CELERY_BEAT_SCHEDULER}")

# ========== ЛОГИРОВАНИЕ ==========
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}

# ========== ТЕСТИРУЕМ S3 ПОДКЛЮЧЕНИЕ ==========
if RENDER_EXTERNAL_HOSTNAME and AWS_ACCESS_KEY_ID:
    try:
        import boto3
        from botocore.exceptions import ClientError
        
        print("="*60)
        print("🔍 Тестируем подключение к S3...")
        
        # Создаем клиент для проверки
        s3_client = boto3.client(
            's3',
            endpoint_url=AWS_S3_ENDPOINT_URL,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_S3_REGION_NAME,
            config=boto3.session.Config(signature_version='s3v4')
        )
        
        # Пробуем получить информацию о бакете
        try:
            response = s3_client.head_bucket(Bucket=AWS_STORAGE_BUCKET_NAME)
            print(f"✅ Бакет '{AWS_STORAGE_BUCKET_NAME}' доступен!")
            
            # Пробуем получить список файлов
            objects = s3_client.list_objects_v2(Bucket=AWS_STORAGE_BUCKET_NAME, MaxKeys=5)
            print(f"📁 Файлов в бакете: {objects.get('KeyCount', 0)}")
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == '404':
                print(f"❌ Бакет '{AWS_STORAGE_BUCKET_NAME}' не найден!")
                print("   Убедитесь, что бакет существует в вашем аккаунте bucket.ru")
            elif error_code == '403':
                print(f"❌ Нет доступа к бакету '{AWS_STORAGE_BUCKET_NAME}'!")
                print("   Проверьте ключи доступа и права бакета")
            else:
                print(f"❌ Ошибка доступа к бакету: {error_code}")
                print(f"   Детали: {e.response['Error']['Message']}")
                
    except ImportError:
        print("⚠️  Не удалось импортировать boto3")
    except Exception as e:
        print(f"⚠️  Ошибка тестирования S3: {type(e).__name__}: {e}")

print("="*60)
print(f"Итоговая конфигурация:")
print(f"ALLOWED_HOSTS: {ALLOWED_HOSTS}")
print(f"DEBUG: {DEBUG}")
print(f"INSTALLED_APPS содержит django_celery_beat: {'django_celery_beat' in INSTALLED_APPS}")
print(f"MEDIA_URL: {MEDIA_URL}")
print(f"STATIC_URL: {STATIC_URL}")
print("="*60)