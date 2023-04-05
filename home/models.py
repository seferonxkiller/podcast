from django.contrib.auth.models import User
from django.db import models
from episodes.models import Episode


class Like(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE)
