# Generated by Django 4.1 on 2022-08-27 19:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api_snippets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='snippetuserpermission',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='snippetperms', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='snippet',
            name='anyone_can',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api_snippets.snippetpermissionset'),
        ),
        migrations.AddField(
            model_name='snippet',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='snippets', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='snippet',
            name='language',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='snippets', to='api_snippets.language'),
        ),
    ]
