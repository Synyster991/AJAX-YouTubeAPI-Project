from django.db import models

class Library(models.Model):
     title = models.CharField(max_length=255)

     def __str__(self):
          return self.title

class Video(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    youtube_id = models.CharField(max_length=255)
    library = models.ForeignKey(Library, on_delete=models.CASCADE)

