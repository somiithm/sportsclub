from django.db import models
from base.models import BaseModel


class Club(BaseModel):
    name = models.CharField(max_length=255)

