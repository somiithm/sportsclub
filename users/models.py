from django.db import models
from base.models import BaseModel
from clubs.models import Club


class User(BaseModel):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    handle = models.CharField(max_length=255, unique=True, null=True)

    profile_photo = models.FileField(null=True, blank=True)
    cover_photo = models.FileField(null=True, blank=True)

    email_id = models.EmailField(unique=True)
    email_verified = models.NullBooleanField(blank=True, null=True)

    interests = models.ManyToManyField(to=Sports)
    following_clubs = models.ManyToManyField(to=Club)


class Sports(BaseModel):
    name = models.CharField(max_length=255)


class Friendship(BaseModel):
    requester = models.ForeignKey(User, related_name='requester', on_delete=models.CASCADE)
    acceptor = models.ForeignKey(User, related_name='accepter', on_delete=models.CASCADE)



