from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericRelation
from comment.models import Comment


class Article(models.Model):
    title = models.CharField(max_length=20)
    desc = models.TextField()
    comments = GenericRelation(Comment)

    def __str__(self):
        return self.title

