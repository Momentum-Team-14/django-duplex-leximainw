from django.core.exceptions import PermissionDenied
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from django.http import Http404
from api_snippets.models import Snippet
from .forms import SnippetForm
from .models import User
from .shortcuts import recent_snippets, viewable_snippets


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
        print(user.pk)
        print(request.user)
        if user.pk == request.user.pk:
            name = "Your"
        else:
            name = f"{user.username}'s"
        return render(request, 'profile.html', {
            'profile': user,
            'name': name,
            'snippets': viewable_snippets(request.user).filter(author=user),
        })


def snippets_recent(request):
    return render(request, 'core/recent_snippets_page.html', {'snippets': recent_snippets(request.user)})


def snippets_details(request, pk=None):
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
        if not request.user in snippet.editors.all():
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
                snippet.save()
            return redirect('Snippet details', pk=form.save().pk)
        else:
            return redirect('/')
    else:
        form = SnippetForm(instance=snippet)
        return render(request, 'core/snippet_edit.html', {
            'form': form,
            'button_text': 'Create' if pk is None else 'Save Changes',
        })


def snippets_delete(request, pk=None):
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


def snippets_fork(request, pk=None):
    if not request.user.is_authenticated:
        raise PermissionDenied()
    snippet = get_object_or_404(Snippet, pk=pk)
    if not (snippet.allow_forks or request.user in snippet.editors.all()):
        raise PermissionDenied()
    snippet.parent = Snippet.objects.get(pk=pk)
    snippet.pk = None
    snippet.id = None
    snippet.save()
    snippet.author = request.user
    snippet.editors.add(request.user)
    snippet.save()
    return redirect('Snippet details', pk=snippet.pk)
