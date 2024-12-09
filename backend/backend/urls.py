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
