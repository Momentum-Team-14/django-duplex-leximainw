from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http.response import HttpResponseBadRequest
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from api_snippets.models import Snippet
from .forms import SnippetForm
from .models import User
from .shortcuts import (
    newest_viewable_snippets,
    recent_snippets,
    search_snippets,
    viewable_snippets,
)


def homepage(request):
    return render(request, 'core/homepage.html', {'snippets': recent_snippets(request.user)})


def user_profile(request, pk=None):
    if pk is None:
        user = request.user
        if not user.is_authenticated:
            return redirect('/accounts/login')
        else:
            return redirect('User profile', pk=user.pk)
    else:
        user = get_object_or_404(User, pk=pk)
        if user.pk == request.user.pk:
            name = "Your"
        else:
            name = f"{user.username}'s"
        return render(request, 'profile.html', {
            'profile': user,
            'name': name,
            'snippets': viewable_snippets(request.user).filter(author=user),
            'favorites': viewable_snippets(request.user).intersection(user.favorite_snippets.all())
        })


def search_profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    query = request.GET.get('query', '')
    if not query:
        raise HttpResponseBadRequest()
    snippets = search_snippets(viewable_snippets(request.user)
        & (Snippet.objects.filter(author=user)
                | user.favorite_snippets.all()), query)[:settings.SEARCH_COUNT]
    return render(request, 'core/snippet_results.html', {
        'subtitle': f'Results for {query}:',
        'snippets': snippets,
    })


def snippets_recent(request):
    query = request.GET.get('query', '')
    if not query:
        return render(request, 'core/recent_snippets_page.html', {'snippets': recent_snippets(request.user)})
    snippets = search_snippets(newest_viewable_snippets(request.user), query)[:settings.SEARCH_COUNT]
    return render(request, 'core/snippet_results.html', {
        'subtitle': f'Results for {query}:',
        'snippets': snippets,
    })


def snippets_details(request, pk):
    snippet = get_object_or_404(Snippet, pk=pk)
    if not (snippet.allow_view or request.user in snippet.editors.all() or request.user == snippet.author):
        raise PermissionDenied()
    return render(request, 'core/snippet_details.html', {
        'snippet': snippet,
        'detailed': True
    })


def snippets_edit(request, pk=None):
    if not request.user.is_authenticated:
        raise PermissionDenied()
    if pk is not None:
        snippet = get_object_or_404(Snippet, pk=pk)
        if request.user not in snippet.editors.all():
            raise PermissionDenied()
    else:
        snippet = None
    if request.method == 'POST':
        form = SnippetForm(request.POST, instance=snippet)
        if form.is_valid():
            if pk is None:
                snippet = form.save(commit=False)
                snippet.author = request.user
                snippet.save()
                snippet.editors.add(request.user)
            else:
                snippet = form.save()
            return redirect('Snippet details', pk=snippet.pk)
        else:
            return redirect('/')
    else:
        form = SnippetForm(instance=snippet)
        return render(request, 'core/snippet_edit.html', {
            'form': form,
            'button_text': 'Create' if pk is None else 'Save Changes',
        })


def snippets_delete(request, pk):
    if not request.user.is_authenticated:
        raise PermissionDenied()
    snippet = get_object_or_404(Snippet, pk=pk)
    if request.user != snippet.author:
        raise PermissionDenied()
    if request.method == 'POST':
        if request.POST['confirm'] == snippet.title:
            snippet.delete()
            return redirect('Recent snippets')
        else:
            return redirect('Snippet details', pk=snippet.pk)
    else:
        return render(request, 'core/delete_form.html', {
            'confirm_text': snippet.title,
        })


def snippets_fork(request, pk):
    if not request.user.is_authenticated:
        raise PermissionDenied()
    snippet = get_object_or_404(Snippet, pk=pk)
    if not (snippet.allow_forks or request.user in snippet.editors.all()):
        raise PermissionDenied()
    snippet.parent = Snippet.objects.get(pk=pk)
    snippet.pk = None
    snippet.id = None
    snippet.author = request.user
    snippet.save()
    snippet.editors.add(request.user)
    return redirect('Snippet details', pk=snippet.pk)
