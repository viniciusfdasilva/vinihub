from django.db import models

class LastInstaWebPath(models.Model):
    last_path = models.TextField(default=None)

class Repository(models.Model):
    nome = models.TextField()
    #size = models.IntegerField()
    #branches = models.IntegerField()
    #tags = models.IntegerField()
    #commits = models.IntegerField()
# Create your models here.
