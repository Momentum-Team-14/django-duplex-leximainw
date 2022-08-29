from django.core.exceptions import PermissionDenied
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from api_snippets.models import Snippet
from .forms import SnippetForm
from .shortcuts import recent_snippets


def homepage(request):
    return render(request, 'core/homepage.html', {'snippets': recent_snippets(request.user)})


def snippets_recent(request):
    return render(request, 'core/recent_snippets_page.html', {'snippets': recent_snippets(request.user)})


def snippets_create(request):
    if not request.user.is_authenticated:
        raise PermissionDenied()
    if request.method == 'POST':
        form = SnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save(commit=False)
            snippet.author = request.user
            return redirect('Snippet details', pk=form.save().pk)
        else:
            return redirect('/')
    else:
        form = SnippetForm()
        return render(request, 'core/snippet_create.html', {
            'form': form,
        })


def snippets_details(request, pk=None):
    snippet = get_object_or_404(Snippet, pk=pk)
    return render(request, 'core/snippet_details.html', {'snippet': snippet, 'detailed': True})
