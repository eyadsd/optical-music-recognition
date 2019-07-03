from django.db import models
from django.urls import reverse

# Create your models here.
from music.corefiles.detect_objects import get_midi
import os
from website.settings import BASE_DIR


class Album(models.Model):
    artist = models.CharField(max_length=250)
    album_title = models.CharField(max_length=500)
    gener = models.CharField(max_length=100)
    album_logo = models.FileField()
    album_song = models.FileField(null=True)

    def get_absolute_url(self):

        image_name = self.album_title
        image_path = os.path.join(os.path.join(BASE_DIR, 'media'), self.album_logo.name)

        print(image_name)
        print(image_path)

        get_midi(image_path, image_name)
        return reverse('music:index')

        #To Send Back To Home
        #return reverse('music:detail')



    def __str__(self):
        return self.album_title + ' - ' + self.artist

class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    file_type = models.CharField(max_length=10)
    song_title = models.CharField(max_length=250)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.song_title



