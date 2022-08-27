from django.db import models
from semantic_version.django_fields import SemVerField
from core.models import User


class Language(models.Model):
    name: models.CharField(max_length=200)
    hljs_name: models.CharField(max_length=200)


class SnippetPermissionSet(models.Model):
    delete: models.BooleanField()
    edit: models.BooleanField()
    edit_perms: models.BooleanField()
    fork: models.BooleanField()
    rename: models.BooleanField()
    view: models.BooleanField()


class Snippet(models.Model):
    title: models.CharField(max_length=100)
    author: models.ForeignKey(User, on_delete=models.CASCADE, related_name='snippets')
    description: models.TextField(max_length=2000)
    anyone_can: SnippetPermissionSet()
    language: models.ForeignKey(Language, on_delete=models.SET_NULL, related_name='snippets', blank=True, null=True)
    language_version: SemVerField()
    code: models.TextField()


class SnippetPermissions(models.Model):
    user: models.ForeignKey(User, on_delete=models.CASCADE, related_name='snippetperms')
    snippet: models.ForeignKey(Snippet, on_delete=models.CASCADE, related_name='snippetperms')
    can: SnippetPermissionSet()
