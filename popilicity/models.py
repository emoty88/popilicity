from django.db import models
from django.contrib.auth.models import User
from django_resized import ResizedImageField

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
    #path        = models.ImageField(upload_to='post/images/',  max_length=254, null=False)
    path        = ResizedImageField(size=[800, 800], crop=['middle', 'center'], quality=75, upload_to='post/images/')
    location    = models.ForeignKey(Location, default=1)
    interest    = models.ForeignKey(Interest, default=1)
    status      = models.IntegerField(choices=STATUS_CHOICES, default=1)
    point       = models.FloatField(default=0)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-create_date',)


class Comment(models.Model):
    owner       = models.ForeignKey(User)
    post        = models.ForeignKey(Post)
    text        = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)


class Reaction(models.Model):
    type        = models.IntegerField(choices=REACTION_CHOICES, blank=True, null=True)
    user        = models.ForeignKey(User)
    post        = models.ForeignKey(Post)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)


class Profile(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE)
    bio         = models.TextField(max_length=500, blank=True)
    #image       = models.ImageField(upload_to='user/images/', max_length=254)
    image       = ResizedImageField(size=[500, 500], crop=['middle', 'center'], quality=75, upload_to='post/images/')
    location    = models.ForeignKey(Location, default=1)
    interest    = models.ForeignKey(Interest, default=1)
    birth_date  = models.DateField(null=True, blank=True)
    post_count  = models.IntegerField(default=0)
    like_count  = models.IntegerField(default=0)
    dislike_count  = models.IntegerField(default=0)
    point       = models.FloatField(default=0)


class Notification(models.Model):
    owner       = models.ForeignKey(User, related_name='owner')
    target_usr  = models.ForeignKey(User, related_name='target_usr')
    target_post = models.ForeignKey(Post)
    action      = models.IntegerField(choices=REACTION_CHOICES, blank=True, null=True)
    is_seen     = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
