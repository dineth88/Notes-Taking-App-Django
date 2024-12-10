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
    #cascade --> Delete all the notes of a particular user if the user deleted., related_name --> refrence
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")
    
    def __Str__(self):
        return self.title