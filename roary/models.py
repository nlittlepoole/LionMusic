from django.db import models

# Create your models here.

class User(models.Model):
    uni = models.CharField(max_length=10,primary_key=True)
    department = models.CharField(max_length=120)
    dorm = models.CharField(max_length=120)
    #google_music_time =

    def __str__(self):
        return self.uni
class Song(models.Model):
    url = models.CharField(max_length=200,primary_key=True)
    name = models.CharField(max_length=200)
    year = models.CharField(max_length=200)
    genre = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    duration = plays = models.IntegerField()
    plays = models.IntegerField()
    owner = models.ManyToManyField(User)

    def __str__(self):
        return self.name


