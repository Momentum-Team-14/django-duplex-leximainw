from django.db import models
from django.db.models import Q
from semantic_version.django_fields import SemVerField
from core.models import User


class Language(models.Model):
    name = models.CharField(max_length=200)
    hljs_name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name}"


class Snippet(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='snippets')
    description = models.TextField(max_length=2000, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, related_name='snippets', blank=True, null=True)
    language_version = SemVerField(blank=True, null=True)
    code = models.TextField()

    allow_forks = models.BooleanField()
    allow_view = models.BooleanField()

    def __str__(self):
        return f"{self.title} by {self.author.username}"
