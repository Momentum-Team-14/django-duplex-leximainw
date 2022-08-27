from django.shortcuts import render
from api_snippets.models import Snippet


def homepage(request):
    return render(request, 'core/homepage.html', {})


def snippets_recent(request):
    snippets = Snippet.objects.order_by('created_at')[:20]
    return render(request, 'core/recent_snippets_page.html', {'snippets': snippets})
