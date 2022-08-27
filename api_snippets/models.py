from django.db import models
from django.db.models import Q
from django.db.models.signals import post_delete
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
    anyone_can = models.OneToOneField(SnippetPermissionSet, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, related_name='snippets', blank=True, null=True)
    language_version = SemVerField(blank=True, null=True)
    code = models.TextField()

    def __str__(self):
        return f"{self.title} by {self.author.username}"

    def can(self, perm, user=None):
        if getattr(self.anyone_can, perm):
            return True
        if not user:
            return False
        perms = SnippetUserPermission.objects.filter(Q(user=user) & Q(snippet=self)).first()
        print(perms)
        return bool(perms and getattr(perms.can, perm))

    def can_delete(self, user=None):
        return self.can('destroy', user)

    def can_edit(self, user=None):
        return self.can('edit', user)

    def can_edit_perms(self, user=None):
        return self.can('edit_perms', user)

    def can_fork(self, user=None):
        return self.can('fork', user)

    def can_rename(self, user=None):
        return self.can('rename', user)

    def can_view(self, user=None):
        return self.can('view', user)


class SnippetUserPermission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='snippetperms')
    snippet = models.ForeignKey(Snippet, on_delete=models.CASCADE, related_name='snippetperms')
    can = models.OneToOneField(SnippetPermissionSet, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} can {self.can} {self.snippet.title}"


def on_delete_snippet(sender, instance, using, **kwargs):
    instance.anyone_can.delete()
    SnippetUserPermission.objects.filter(snippet=instance).delete()


def on_delete_snippetperms(sender, instance, using, **kwargs):
    instance.can.delete()


post_delete.connect(on_delete_snippet, Snippet)
post_delete.connect(on_delete_snippetperms, SnippetUserPermission)
