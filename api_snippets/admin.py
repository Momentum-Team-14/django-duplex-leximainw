from django.contrib import admin
from . import models

admin.site.register(models.Language)
admin.site.register(models.Snippet)
admin.site.register(models.SnippetPermissionSet)
admin.site.register(models.SnippetUserPermission)
