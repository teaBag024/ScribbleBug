from django.conf import settings
from django.db import models

# Create your models here.

# This is a Project
class Scribble(models.Model):
    name = models.CharField(max_length=100)
    spider = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="spider_scribble"
    )
    chat_history = models.JSONField(default=list, blank=True)
    code = models.CharField(max_length=30000)

# This is scores
class Score(models.Model):
    spider = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="spider_score"
    )
    scribble = models.ForeignKey(Scribble, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)