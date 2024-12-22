"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 5.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path

from django.conf.global_settings import STATICFILES_DIRS
from environ import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-%w%!c6x7q+#j2pmqibo^lg=h8w4h0h9@h4fii$z6ch^4fy&74r'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    '0.0.0.0',
    "socialandmusicalchambertrust.onrender.com",
    '127.0.0.1',
    '35.160.120.126',
    '44.233.151.27',
    '34.211.200.85',
    # '0.0.0.0/0',
    '0.0.0.0/0']

# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'backend',
    'api',
    'corsheaders'
]
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "DELETE",
    "OPTIONS",
]

CORS_ALLOW_HEADERS = [
    "content-type",
    "authorization",
    "x-csrftoken",
]
MIDDLEWARE = [
    # 'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware'
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
import os
from urllib.parse import urlparse
import environ

# Initialize the environment variable reading
env = environ.Env()
environ.Env.read_env()

# Parse the database URL from environment variable
DATABASE_URL = "postgresql://socialandmusicalchamber_user:DjdEZeAQfgBaKbOPKipww19SySo0rEnN@dpg-ctjsr9popnds73fr1j0g-a.oregon-postgres.render.com/socialandmusicalchamber"  # Use environ to fetch the DATABASE_URL

if DATABASE_URL:
    # Parse the database URL
    url = urlparse(DATABASE_URL)

    # Configure the DATABASES setting
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',  # Specify the database engine
            'NAME': url.path[1:],  # Remove leading '/' from the path to get the DB name
            'USER': url.username,  # Get the username from the URL
            'PASSWORD': url.password,  # Get the password from the URL
            'HOST': url.hostname,  # Get the hostname from the URL
            'PORT': url.port,  # Get the port from the URL (default is 5432)
        }
    }
else:
    # Fallback to SQLite if no DATABASE_URL is set
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / "static"
]
# STATICFILES_
# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'backend.CustomUser'

JAZZMIN_SETTINGS = {
    "custom_js": "./admin.js"
}

# CSRF_COOKIE_DOMAIN = 'https://socialandmusicalchambertrust.onrender.com'  # Include the dot for subdomains

CSRF_TRUSTED_ORIGINS = [
    'https://socialandmusicalchambertrust.onrender.com',
    'https://socailandmusicalchamber.netlify.app'
]
# SESSION_COOKIE_DOMAIN = 'https://socialandmusicalchambertrust.onrender.com'  # For session cookies to work across subdomains
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:5173",
# ]
# CORS_ALLOW_ALL_ORIGINS = True

# CORS_ALLOW_HEADERS = ['*']
# CORS_ALLOW_METHODS = ['DELETE', 'GET', 'OPTIONS', 'PATCH', 'POST', 'PUT']

# CORS_ALLOW_CREDENTIALS = True  # Allow credentials (cookies, etc.)
# SECURE_SSL_REDIRECT = False
# CSRF_COOKIE_PATH = '/'  # Set path if needed
#
# CSRF_COOKIE_NAME = "csrftoken"  # This is the default name for the CSRF cookie
# # CSRF_COOKIE_SAMESITE = "None"  # Set to 'None' for cross-site, but 'Lax' is generally good for most cases
# CSRF_COOKIE_HTTPONLY = False  # Allow JavaScript to access the cookie
# CSRF_COOKIE_SECURE = False  # Set this to True if you're using HTTPS in production

# CSRF_COOKIE_DOMAIN = '.yourdomain.com'  # For cross-subdomain access
# CSRF_COOKIE_SECURE = True  # For secure cookie transmission over HTTPS