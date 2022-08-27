from django.shortcuts import get_object_or_404, render
from api_snippets.models import Snippet


def homepage(request):
    return render(request, 'core/homepage.html', {})


def snippets_recent(request):
    snippets = Snippet.objects.order_by('created_at').reverse()[:20]
    return render(request, 'core/recent_snippets_page.html', {'snippets': snippets})


def snippets_details(request, pk=None):
    snippet = get_object_or_404(Snippet, pk=pk)
    return render(request, 'core/snippet_details.html', {'snippet': snippet, 'detailed': True})
