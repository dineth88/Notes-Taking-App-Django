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
        


