from django.db import models
from base.models import BaseModel
from users.models import User


class Tournament(BaseModel):
    name = models.CharField(max_length=255)
    created_by = models.OneToOneField(to=User, on_delete=models.CASCADE)
