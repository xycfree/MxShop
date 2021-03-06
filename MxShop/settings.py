"""
Django settings for MxShop project.

Generated by 'django-admin startproject' using Django 1.10.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""
import logging
import logging.config
import os
import sys
from datetime import datetime

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
sys.path.insert(0, os.path.join(BASE_DIR, 'extra_apps'))

log_dir = os.path.join(BASE_DIR, 'logs')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)  # 判断路径是否存在，不存在则创建路径
# log_file = 'info-{}.log'.format(datetime.now().strftime('%Y-%m-%d'))  # 文件名
# log_err_file = 'error-{}.log'.format(datetime.now().strftime('%Y-%m-%d'))

log_file = 'info.log'
log_err_file = 'error.log'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ent-qn1&!s-p&aj&e)j4(6(k=$&tr-k(m#8e591pn_k5i%2nt8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
AUTH_USER_MODEL = "users.UserProfile"

# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 'django.contrib.sites',
    'django.contrib.admin',  # 解决doesn't declare an explicit app_label

    'goods.apps.GoodsConfig',
    'users.apps.UsersConfig',
    'trade.apps.TradeConfig',
    'user_operation.apps.UserOperationConfig',

    "DjangoUeditor",
    "xadmin",

    'crispy_forms',
    'django_filters',

    'rest_framework',
    'corsheaders',  # 解决跨域请求的问题 pip install django-cors-headers
    'rest_framework.authtoken',



]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # 解决跨域问题
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True  # 所有的访问都将被允许，白名单不会被使用，默认为false
ROOT_URLCONF = 'MxShop.urls'

# ==============跨域问题======================= #
"""
    1.安装django-cors-headers模块, pip install django-cors-headers
    2.在INSTALLED_APPS中注册'corsheaders'
"""
# 配置白名单
CORS_ORIGIN_WHITELIST = (
    'google.com',
    'hostname.example.com')
CORS_ORIGIN_REGEX_WHITELIST = ('^（https？：//）？（\ w + \。）？google \ .com $')
CORS_ALLOW_CREDENTIALS = True  # 是否允许Cookie包含在跨站点HTTP请求（CORS）中，默认为false

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)

CORS_ALLOW_HEADERS = (
    'XMLHttpRequest',
    'X_FILENAME',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'Pragma',
)
# ============================================= #



TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'MxShop.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "mxshop",
        'USER': 'root',
        'PASSWORD': "root",
        'HOST': "127.0.0.1",
        "PORT": 3306,
        'OPTIONS': {
            'init_command': 'SET storage_engine=INNODB;',
            'charset': 'utf8',
            # 'isolation_level': 'read committed',
            'isolation_level': None,
                    }

    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

#设置时区
LANGUAGE_CODE = 'zh-hans'  # 中文支持，django1.8以后支持；1.8以前是zh-cn
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
USE_TZ = False   # 默认是Ture，时间是utc时间，由于我们要用本地时间，所用手动修改为false！！！！

# 自定义用户验证
AUTHENTICATION_BACKENDS = (
    'users.views.CustomBackend',
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = "/media/"
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

MEDIA_ROOT = os.path.join(BASE_DIR, "media")


import datetime
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7),  # 也可以设置seconds=30
    'JWT_AUTH_HEADER_PREFIX': 'JWT',  # JWT跟前端保持一致，比如“token”这里设置成JWT
}



REST_FRAMEWORK = {
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # 'PAGE_SIZE': 10,
    # 'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',)
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    )
}




LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            'format': '%(asctime)s [%(name)s:%(lineno)d] [%(levelname)s]- %(message)s'
        },
        'standard': {
            'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(levelname)s]- %(message)s'
        },
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "stream": "ext://sys.stdout"
        },
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            "formatter": "standard",
            'filename': os.path.join(log_dir, log_err_file),
            'mode': 'w+',
            'maxBytes': 1024 * 1024 * 50,
            'backupCount': 10,
            "encoding": "utf8",
        },

        "default": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "formatter": "standard",
            "filename": os.path.join(log_dir, log_file),
            'mode': 'w+',
            "maxBytes": 1024 * 1024 * 50,  # 5 MB
            "backupCount": 10,
            "encoding": "utf8"
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
        # 'filter': {
        # },
    },

    "loggers": {
        "": {
            "level": "DEBUG",
            "handlers": ["console"],
            "propagate": False,  # this tells logger to send logging message # to its parent (will send if set to True)
        },
        'django.db': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },

    "root": {
        'handlers': ['default', 'console', 'error'],
        'level': "DEBUG",
        'propagate': False
    }
}

# 手机号码正则表达式
REGEX_MOBILE = "^1[3589]\d{9}$|^147\d{8}$|^176\d{8}$"
