1. django-cors-headers : To fix cross origin request issue

2.  cd env
 Scripts/activate
 cd ..
 pip install -r requirements.txt
 django-admin startproject backend
 cd backend
 python manage.py startapp api

3. Add credentials like Db password, .. to the env file 

 project/settings

    from datetime import timedelta
    from dotenv import load_dotenv
    import os

    load_dotenv() 

Allow any host to host our django application

    ALLOWED_HOSTS = ["*"]

4. Adding JWT authentication.

    REST_FRAMEWORK = {
        "DEFAULT_AUTHENTICATION_CLASSES":(
            "rest_framework_simplejwt.authentication.JWTAuthentication",
        ),
        "DEFAULT_PERMISSION_CLASSES":[
            "rest_framework.permissions.isAuthenticated",
        ],
    }

    SIMPLE_JWT = {
        "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
        "REFRESH_TOKEN_LIFETIME":timedelta(days=1),
    }

5. Adding installed-apps.

    # Application definition

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        "api",
        "rest_framework",
        "corsheaders"
    ]

    Adding Cors middleware for

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        "corsheaders.middleware.CorsMiddleware",
    ]

    CORS_ALLOW_ALL_ORIGINS = True
    CORS_ALLOWS_CREDENTIALS = True