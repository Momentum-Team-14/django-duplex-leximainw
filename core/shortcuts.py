from django.db.models import Q
from api_snippets.models import Snippet


def viewable_snippets(user=None):
    if user is None or not user.is_authenticated:
        return Snippet.objects.filter(allow_view=True)
    else:
        return Snippet.objects.filter(Q(allow_view=True)
            | Q(author=user) | Q(editors=user))


def recent_snippets(user=None, count=20):
    return viewable_snippets(user).order_by('created_at').reverse()[:count]
