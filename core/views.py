from django.shortcuts import get_object_or_404, render
from api_snippets.models import Snippet
from .shortcuts import recent_snippets


def homepage(request):
    return render(request, 'core/homepage.html', {'snippets': recent_snippets(request.user)})


def snippets_recent(request):
    return render(request, 'core/recent_snippets_page.html', {'snippets': recent_snippets(request.user)})


def snippets_create(request):
    pass


def snippets_details(request, pk=None):
    snippet = get_object_or_404(Snippet, pk=pk)
    return render(request, 'core/snippet_details.html', {'snippet': snippet, 'detailed': True})
