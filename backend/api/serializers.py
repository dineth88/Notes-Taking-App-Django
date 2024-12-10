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
        #Not allowed to write author
        extra_kwargs = {"author": {"read_only": True}}