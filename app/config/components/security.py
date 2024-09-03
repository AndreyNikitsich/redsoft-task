import os

SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = True
ALLOWED_HOSTS = []
AUTH_USER_MODEL = "mentors.CustomUser"
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
PASSWORD_HASHERS = [
    "mentors.password_encryption.AesPasswordEncryption",
]
PASSWORD_ENCRYPTION_KEY = os.environ.get('PASSWORD_ENCRYPTION_KEY').encode('utf-8')