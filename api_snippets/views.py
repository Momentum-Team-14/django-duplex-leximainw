from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Snippet

def snippet_favorite(request, pk):
    if not request.user.is_authenticated:
        raise PermissionDenied()
    snippet = get_object_or_404(Snippet, pk=pk)
    if request.user.favorite_snippets.filter(pk=pk).exists():
        request.user.favorite_snippets.remove(snippet)
        data = {'favorited': False}
    else:
        request.user.favorite_snippets.add(snippet)
        data = {'favorited': True}
    return JsonResponse(data)
