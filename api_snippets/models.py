from django.db import models
from django.db.models.signals import post_migrate
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
    parent = models.ForeignKey('Snippet', on_delete=models.SET_NULL, related_name='forks', blank=True, null=True)
    code = models.TextField()

    editors = models.ManyToManyField(User, related_name='shared_snippets', blank=True)
    favorited_by = models.ManyToManyField(User, related_name='favorite_snippets', blank=True)
    allow_forks = models.BooleanField('Anyone can fork', default=True)
    allow_view = models.BooleanField('Anyone can view', default=True)

    def __str__(self):
        return f"{self.title} by {self.author.username}"


defaultLanguages = [
    {
        'name': 'C',
        'hljs_name': 'c',
    },
    {
        'name': 'C++',
        'hljs_name': 'cpp',
    },
    {
        'name': 'C#',
        'hljs_name': 'csharp',
    },
    {
        'name': 'CSS',
        'hljs_name': 'css',
    },
    {
        'name': 'HTML',
        'hljs_name': 'html',
    },
    {
        'name': 'Java',
        'hljs_name': 'java',
    },
    {
        'name': 'JavaScript',
        'hljs_name': 'js',
    },
    {
        'name': 'Lua',
        'hljs_name': 'lua',
    },
    {
        'name': 'Python',
        'hljs_name': 'python',
    },
    {
        'name': 'Rust',
        'hljs_name': 'rust',
    },
    {
        'name': 'XML',
        'hljs_name': 'xml',
    },
]

def create_default_languages(**kwargs):
    for default in defaultLanguages:
        if Language.objects.filter(name=default['name']).count() == 0:
            Language(**default).save()

post_migrate.connect(create_default_languages)
