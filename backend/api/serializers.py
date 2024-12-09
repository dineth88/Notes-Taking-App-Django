from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        field = ["id", "username", "password"]
        #Do not return password
        extra_kwargs = {"password":{"write_only":True}}

#Create new user object

    def create(self, validated_data):
        user = User.objects.create_ser(**validated_data)
        return user
    
    #When user entered new user credentials it will store the fields and 
    # create function create the user obj with those credentials