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
    #serializer --> Manage JSON data
    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ["id", "username", "password"]
            #Do not return password
            extra_kwargs = {"password":{"write_only":True}}

    #Create new user object

        def create(self, validated_data):
            user = User.objects.create_user(**validated_data)
            return user

            When user entered new user credentials it will store the fields and 
    # create function create the user obj with those credentials.

7. Creating views for

    app/view.py

    from django.shortcuts import render
    from django.contrib.auth.models import User
    from rest_framework import generics
    from .serializers import UserSerializer
    from rest_framework.permissions import isAuthenticated, AllowAny

    # Create your views here.
    class CreateUserView(generics.CreateAPIView):
        #list of all of the User obj
        queryset = User.objects.all()
        serializer_class = UserSerializer
        permission_classes = [AllowAny]

8. Creating URLS

    project/urls

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

9. Add migrations

    #Making migrations
    python3 manage.py makemigrations
    #applying migrations --> Setup the database, when we type this cmd again it will setup a new database
    python3 manage.py migrate
    #run app
    python3 manage.py runserver

10. Creating new user

    http://127.0.0.1:8000/api/user/register --> enter new username and password and then POST.

    Getting access token and refresh token.

    http://127.0.0.1:8000/api/token/ --> enter user creentials and click

    copy the refresh token.

    http://127.0.0.1:8000/api/token/refresh/ --> Paste the refresh token and get the access token

11. Link notes with users.


    Note 1 ---------------> User 1 <---------------Note 3
                              ^
                              |
    Note 2 --------------------

    User inbuilt model making connection with note class by joining with foreign keys.

    app/models
    from django.db import models
    from django.contrib.auth.models import User
    # Create your models here.
    class Note(models.Model):
        title = models.CharField(max_length=100)
        content = models.TextField()
        #Do not pass just automatically populate
        created_at = models.DateTimeField(auto_now_add=True)
        #Specify who made this note
        #One to many.One user has many notes.
        #cascade --> Delete all the notes ofa particular user if the user deleted.
        author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")
        
        def __Str__(self):
            return self.title

13. Create Note serializer

    app/serializer
    
    from django.contrib.auth.models import User
    from rest_framework import serializers
    from .models import Note
    #serializer --> Manage JSON data
    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ["id", "username", "password"]
            #Do not return password
            extra_kwargs = {"password":{"write_only":True}}

        #Create new user object

        def create(self, validated_data):
            user = User.objects.create_user(**validated_data)
            return user
    
    #When user entered new user credentials it will store the fields and 
    # create function create the user obj with those credentials

    #Note serializer class
    class NoteSerializer(serializers.ModelSerializer):
        class Meta:
            model = Note
            fields = ["id", "title", "content", "created_at", "author"]
            extra_kwargs = {"author": {"read_only": True}}

14. Creating views to create and delete the notes.

    ListCreateAPIView --> Handling mutiple operations like create and select

    app/views

    from django.shortcuts import render
    from django.contrib.auth.models import User
    from rest_framework import generics
    from .serializers import UserSerializer, NoteSerializer
    from rest_framework.permissions import IsAuthenticated, AllowAny
    from .models import Note

    # Create your views here.
    class CreateUserView(generics.CreateAPIView):
        #list of all of the User obj
        queryset = User.objects.all()
        #adding serializer class
        serializer_class = UserSerializer
        permission_classes = [AllowAny]
        
    #Created a ListCreateAPIView because it will state all the notes of a particular user or it will create a new note
    class NoteListCreate(generics.ListCreateAPIView):
        serializer_class = NoteSerializer
        #Cannot create a view without authenticating
        permission_classes = [IsAuthenticated]

        def get_queryset(self):
        #get the user that is current interacting with
        user = self.request.user
        #get all the notes
        #return Note.objects.all()
        #get all the notes of the user
        return Note.objects.filter(author=user)
        #get all the notes of the user by filtering attributes
        #return Note.objects.filter(author=user, title=title)

        #custom functionality to override the create method
        def perform_create(self, serializer):
            if serializer.is_valid():
                #author = self.request.user --> As we allowed read only to the author we nead to write the author manually.
                serializer.save(author = self.request.user)
            else:
                print(serializer.errors)

    class NoteDelete(generics.DestroyAPIView):
        serializer_class = NoteSerializer
        permission_classes = [IsAuthenticated]
        
        #specifying what notes will be deleted
        def get_queryset(self):
            user = self.request.user
            return Note.objects.filter(author=user)
    
    --------------------------------------------------------------------------------------------------------------

    self.request.user --> Get the current user

    create --> CreateAPIView, ListCreateAPIView
    delete --> DeleteAPIView, ListDeleteAPIView

15. Create app urls  

    as_view() --> class-based views have an as_view() class method which returns a function that can be 
                  called when a request arrives for a URL matching the associated pattern
    
    app/urls.py

    from django.urls import path
    from . import views

    urlpatterns = [
        path("notes/", views.NoteListCreate.as_view(), name="note-list"),
        path("notes/delete/<int:pk>/", views.NoteDelete.as_view(), name="delete-note")
    ]

16. Join app/urls with project/urls.

    project/urls

    #including app/urls
    path("api/", include("api.urls")),

17. run

    python manage.py makemigrations
    python3 manage.py migrate
    python manage.py runserver



    _________________________________________________________________React___________________________________________________________



     npm create vite@latest frontend -- --template react
     npm install react-axios react-router-dom jwt-decode 

     Mapping with endpoint

    src/consttants.js

     export const ACCESS_TOKEN = "access";
    export const REFRESH_TOKEN = "refresh";

    src.api.js

    import axios from "axios"
    import {ACCESS_TOKEN} from "./constants"

    const api = axios.create({
        baseURL: import.meta.env.VITE_API_URL
    })

    src/.env

    VITE_API_URL = "http://localhost:8080"

    api.js

    import axios from "axios"
    import {ACCESS_TOKEN} from "./constants"

    const api = axios.create({
        baseURL: import.meta.env.VITE_API_URL
    })

    api.interceptors.request.use(
        (config) =>{
            //localStorage is a web storage object that allows
            // JavaScript sites and apps to keep key-value 
            //pairs in a web browser with no expiration date
            const token = localStorage.getItem(ACCESS_TOKEN);
            if (token) {
                config.headers.Authorization = 'Bearer ${token}'
            }
            return config
        },
        (error) => {
            return Promise.reject(error)
        }
    )

    export default api

    localhost --> localStorage is a web storage
     object that allows JavaScript sites and apps to keep key-value 
     pairs in a web browser with no expiration date.

















        

