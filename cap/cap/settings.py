import sys
from pathlib import Path
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# print('************************************')
# print( BASE_DIR )
# if 'zaws' in str( BASE_DIR ):
#     sys.path.append("C:/zaws/Link/0322/sam")
# else:
#     sys.path.append("/home/ubuntu/sam")
# print('************************************')
# from settings2 import SECRET_KEY    #   Works
# print ( settings2.SECRET_KEY )        #   import settings2
# print( SECRET_KEY )
# print('____________________________________')

# from settings2 import SECRET_KEY, DEBUG, ALLOWED_HOSTS
# print('____________________________________')
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'k%49@hrebkp*!h-i0q6v6azj1@&1xch)1h0ivku^b*=znp1!79'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0', '10.0.0.228', '54.241.108.184', 'ec2-54-241-108-184.us-west-1.compute.amazonaws.com' ]
ALLOWED_HOSTS = ['*']
# ALLOWED_HOSTS = ['10.0.0.12', '98.210.94.90']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ie.apps.IeConfig',
    'mail.apps.MailConfig',
    'cc.apps.CcConfig',
    'cclog.apps.CclogConfig',
    'po.apps.PoConfig',
    'ro.apps.RoConfig',
    'link.apps.LinkConfig',
    'vendor.apps.VendorConfig',
    'django_filters'        #   pip install django-filter

    # 'background_task'
    # 'bootstrapform'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cap.urls'

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

WSGI_APPLICATION = 'cap.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL          = '/home/x/CAP/static/'
# STATIC_URL          = '/home/ec2-user/static/'
LOGIN_REDIRECT_URL  = 'home'
LOGOUT_REDIRECT_URL = 'login'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
