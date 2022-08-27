from django.shortcuts import render


def homepage(request):
    return render(request, 'core/homepage.html', {})


def snippets_recent(request):
    return render(request, 'base.html', {})
