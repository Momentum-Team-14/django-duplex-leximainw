from django import forms
from api_snippets.models import Snippet


class SnippetForm(forms.ModelForm):
    class Meta:
        model = Snippet
        fields = (
            'title',
            'allow_view',
            'allow_forks',
            'editors',
            'description',
            'language',
            'language_version',
            'code',
        )
