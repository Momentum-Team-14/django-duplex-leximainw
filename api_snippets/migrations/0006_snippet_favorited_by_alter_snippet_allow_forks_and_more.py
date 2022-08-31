# Generated by Django 4.1 on 2022-08-31 14:53

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api_snippets', '0005_snippet_parent_alter_snippet_allow_forks_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='snippet',
            name='favorited_by',
            field=models.ManyToManyField(blank=True, related_name='favorite_snippets', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='snippet',
            name='allow_forks',
            field=models.BooleanField(default=True, verbose_name='Anyone can fork'),
        ),
        migrations.AlterField(
            model_name='snippet',
            name='allow_view',
            field=models.BooleanField(default=True, verbose_name='Anyone can view'),
        ),
    ]
