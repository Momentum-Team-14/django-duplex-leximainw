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


def snippets_edit(request, pk=None):
    if not request.user.is_authenticated:
        raise PermissionDenied()
    if request.method == 'POST':
        form = SnippetForm(request.POST, instance=get_object_or_404(Snippet, pk=pk))
        if form.is_valid():
            if pk is None:
                snippet = form.save(commit=False)
                snippet.author = request.user
            return redirect('Snippet details', pk=form.save().pk)
        else:
            return redirect('/')
    else:
        if pk is None:
            form = SnippetForm()
        else:
            form = SnippetForm(instance=get_object_or_404(Snippet, pk=pk))
        return render(request, 'core/snippet_edit.html', {
            'form': form,
            'button_text': 'Create' if pk is None else 'Save Changes',
        })


def snippets_details(request, pk=None):
    snippet = get_object_or_404(Snippet, pk=pk)
    return render(request, 'core/snippet_details.html', {
        'snippet': snippet,
        'detailed': True
    })
