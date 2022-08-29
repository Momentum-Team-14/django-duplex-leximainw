from django import forms
from api_snippets.models import Snippet


class SnippetForm(forms.ModelForm):
    class Meta:
        model = Snippet
        fields = (
            'title',
            'allow_forks',
            'allow_view',
            'description',
            'language',
            'language_version',
            'code',
        )
