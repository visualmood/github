"""
Django settings for vmerp project.
Generated by 'django-admin startproject' using Django 5.1.2.
For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
# settings.py文件是Django在创建项目django-admin startproject命令时自动生成的配置文件，
# 该文件包含了Django项目的配置信息，包括数据库、静态文件、模板、中间件等。
# 该文件可以根据实际情况进行修改，但建议不要直接修改该文件，而是通过Django提供的命令行工具来修改配置文件。
# 具体修改方法如下：
# 1. 进入项目目录，执行命令：python manage.py runserver 0.0.0.0:8000
# 2. 打开浏览器，输入http://localhost:8000，出现欢迎页面说明修改成功。
# 3. 打开命令行，进入项目目录，执行命令：python manage.py startapp app_name
# 4. 在项目目录下找到新的app_name文件夹，进入该文件夹，修改app_name/apps.py文件，修改该文件中的name属性为app_name，
# 5. 在项目目录的settings.py文件中，修改INSTALLED_APPS列表，添加app_name应用，
# 6. 重新启动服务器，访问http://localhost:8000/app_name，如果出现欢迎页面说明修改成功。
# 7. 完成。



from pathlib import Path             # 导入pathlib模块,用于处理路径,pathlib模块是Python3.4+的标准库,下面设置BASE_DIR时会用到
import os                            # 导入os模块,用于获取环境变量


# import pymysql                    # 导入pymysql,用于连接mysql数据库
# pymysql.install_as_MySQLdb()      # 将pymysql设置为django的默认数据库引擎

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-a6ao9xe969t(u(0szc#$&l#&hznxj5kl(9^$iwxouth3gan3wf'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']              # 设置允许访问的域名，这里设置为*表示允许所有域名访问   例如：ALLOWED_HOSTS = ['www.example.com', 'example.com']


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 上面是django自带的应用，下面是自定义应用
    'authentication',   # 认证模块
    'suppliers',        # 供应商模块
    'materials',        # 物料模块
    'stock',            # 库存模块
    'goods',            # 商品模块
    'expenses'          # 费用模块
    'purchases',        # 采购模块
    'orders',           # 订单模块
    'production',       # 生产模块
    'reports',          # 报表模块

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


ROOT_URLCONF = 'vmerp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],                                   # 指定模板文件目录
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


WSGI_APPLICATION = 'vmerp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 配置mysql数据库
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'vmerp',
#         'USER': 'root',
#         'PASSWORD': 'vm888888',
#         'HOST': 'localhost',
#         'PORT': '3306',
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/
LANGUAGE_CODE = 'zh-hans'       # 设置语言为中文
TIME_ZONE = 'Asia/Shanghai'     # 设置时区为上海 
USE_I18N = True                 # 设置多语言支持
USE_L10N = True                 # 设置本地化支持   例如：日期时间格式本地化等
USE_TZ = True                   # 设置时区为True,使用时间区分


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/
STATIC_URL = 'static/'         # 设置静态文件url前缀


# 配置静态文件目录
STATICFILES_DIRS = [BASE_DIR / 'static',]

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

# 配置模型类 models 默认的主键数据类型，默认是AutoField，改成BigAutoField，可以支持更大的整数
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# 配置messages出错默认样式，使用bootstrap4格式，如果不设置，出错信息默认样式为蓝色背景，白色字体
from django.contrib import messages
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}



# 配置QQ邮箱发送功能 每个项目配置完，请不要打逗号，打逗号会导致配置出错
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.qq.com'                    # 邮箱服务器
EMAIL_PORT = 25                               # 端口                     
EMAIL_USE_TLS = True                          # 启用TLS加密             
EMAIL_HOST_USER = '727726364@qq.com'          # 邮箱地址                
EMAIL_HOST_PASSWORD = 'caksjysvnxynbahd'      # 邮箱密码  授权码              
DEFAULT_FROM_EMAIL = '727726364@qq.com'       # 默认发件人
# # 14天后，即元月5日将代码改成以下专门为公司系统配置的邮箱。因为以上是私人邮箱，不方便公开。
# EMAIL_HOST_USER = 'viusalmood@qq.com'          # 邮箱地址                
# EMAIL_HOST_PASSWORD = '****'      # 邮箱密码  授权码              
# DEFAULT_FROM_EMAIL = 'viusalmood@qq.com'       # 默认发件人





# # 14天后，也可以设置下sina邮箱能否使用。
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# # SMTP 端口 465：这个端口默认使用 SSL 加密
# EMAIL_HOST = 'smtp.sina.com'                  # 邮箱服务器
# EMAIL_PORT = 465                              # 使用 SSL 端口
# EMAIL_USE_SSL = True                          # 启用SSL加密
# EMAIL_HOST_USER = 'visualmooderp@sina.com'    # 邮箱地址
# EMAIL_HOST_PASSWORD = '306232d571de19ee'      # 邮箱密码 或 授权码
# DEFAULT_FROM_EMAIL = 'visualmooderp@sina.com' # 默认发件人

# # SMTP 端口 587：这个端口通常用于 TLS 加密（STARTTLS）。
# EMAIL_HOST = 'smtp.sina.com'                  # 邮箱服务器
# EMAIL_PORT = 587                              # 使用 STARTTLS 端口
# EMAIL_USE_TLS = True                          # 启用TLS加密
# EMAIL_HOST_USER = 'visualmooderp@sina.com'    # 邮箱地址
# EMAIL_HOST_PASSWORD = '306232d571de19ee'      # 邮箱密码 或 授权码
# DEFAULT_FROM_EMAIL = 'visualmooderp@sina.com' # 默认发件人



