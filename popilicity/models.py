from django.db import models
from django.contrib.auth.models import User

STATUS_CHOICES = (
    (0, 'DEACTIVE'),
    (1, 'ACTIVE'),
)

TYPE_CHOICES = (
    (1, 'IMAGE'),
    (2, 'VIDEO'),
)

REACTION_CHOICES = (
    (-1, 'DISLIKE'),
    (1, 'LIKE'),
)


class Location(models.Model):
    name        = models.CharField(max_length=64, null=False)

    def __str__(self):
        return self.name


class Interest(models.Model):
    name        = models.CharField(max_length=64, null=False)

    def __str__(self):
        return self.name


class Post(models.Model):
    type        = models.IntegerField(choices=TYPE_CHOICES, default=1)
    owner       = models.ForeignKey(User)
    #path        = models.CharField(max_length=64, null=False)
    path        = models.ImageField(upload_to='static/post/images/', max_length=254)
    location    = models.ForeignKey(Location, default=1)
    interest    = models.ForeignKey(Interest, default=1)
    status      = models.IntegerField(choices=STATUS_CHOICES, default=1)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    owner       = models.ForeignKey(User)
    post        = models.ForeignKey(Post)
    text        = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)


class Reaction(models.Model):
    type        = models.IntegerField(choices=REACTION_CHOICES)
    user        = models.ForeignKey(User)
    post        = models.ForeignKey(Post)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
