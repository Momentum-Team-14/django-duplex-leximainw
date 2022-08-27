from django.db import models
from semantic_version.django_fields import SemVerField
from core.models import User


class Language(models.Model):
    name = models.CharField(max_length=200)
    hljs_name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name}"


class SnippetPermissionSet(models.Model):
    destroy = models.BooleanField()
    edit = models.BooleanField()
    edit_perms = models.BooleanField()
    fork = models.BooleanField()
    rename = models.BooleanField()
    view = models.BooleanField()

    def __str__(self):
        perms = [
            ("delete", self.destroy),
            ("edit", self.edit),
            ("edit permissions", self.edit_perms),
            ("fork", self.fork),
            ("rename", self.rename),
            ("view", self.view),
        ]
        return f"({', '.join([x[0] for x in perms if x[1]])})"


class Snippet(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='snippets')
    description = models.TextField(max_length=2000, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    anyone_can = SnippetPermissionSet()
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, related_name='snippets', blank=True, null=True)
    language_version = SemVerField(blank=True, null=True)
    code = models.TextField()

    def __str__(self):
        return f"{self.title} by {self.author.username}"


class SnippetUserPermission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='snippetperms')
    snippet = models.ForeignKey(Snippet, on_delete=models.CASCADE, related_name='snippetperms')
    can = SnippetPermissionSet()

    def __str__(self):
        return f"{self.user.username} can {self.can} {self.snippet.title}"
