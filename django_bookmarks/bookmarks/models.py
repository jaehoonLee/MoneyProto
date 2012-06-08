from django.db import models
from django.contrib.auth.models import User

class Link(models.Model):
    url = models.URLField(unique=True)

class Bookmark(models.Model):
    title = models.CharField(max_length=200)
    user = models.ForeignKey(User)
    link = models.ForeignKey(Link)

#Real DB For Money

class Person(models.Model):
    accountID = models.CharField(max_length=20)
    age = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    pno = models.CharField(max_length=20)
    sex = models.CharField(max_length=20)
    uid = models.CharField(max_length=20)

class Card(models.Model):
    cardID = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    pno = models.CharField(max_length=20)
    uid = models.CharField(max_length=20)

