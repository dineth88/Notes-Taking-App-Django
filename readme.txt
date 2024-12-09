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

    -------------------------------------------------------------------------------------

    JWT Tokens

    1. Access token : Make the request, we can set time to delete
    1. Refresh token : Refresh the access token

    When access token expire likely within 30 min the access 
    token will send the refresh token to the back end and it will send new access token.

6. Serializer --> Establish JSON data handling in django.
    
    Setting up an user.

    Project/serializers

    from django.contrib.auth.models import User
    from rest_framework import serializers

    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            field = ["id", "username", "password"]

            #Do not return password
            extra_kwargs = {"password":{"write_only":True}}

            When user entered new user credentials it will store the fields and 
    # create function create the user obj with those credentials.

7. Creating views for

    project/view.py

    from django.shortcuts import render
    from django.contrib.auth.models import User
    from rest_framework import generics
    from .serializers import UserSerializer
    from rest_framework.permissions import isAuthenticated, AllowAny

    # Create your views here.
    class CreateUserView(generics.CreateAPIView):
        #list of all of the User obj
        queryset = User.objects.all()
        serializer_class = User
        permission_classes = [AllowAny]

8. Creating URLS

    from django.contrib import admin
    from django.urls import path, include
    from api.views import CreateUserView
    from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

    urlpatterns = [
        path('admin/', admin.site.urls),
        #url to create a user 
        path("api/user/register", CreateUserView.as_view(), name="register"),
        #getting token
        path("api/token/", TokenObtainPairView.as_view(), name="get_token"),
        #link to refresh th etoken
        path("api/token/refresh/", TokenRefreshView.as_view(), name="refresh"),
        #importing prebuild rest_framework urls
        path("api-auth/", include("rest_framework.urls")),
    ]




        

