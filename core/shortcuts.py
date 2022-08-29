from django.db.models import Q
from api_snippets.models import Snippet


def viewable_snippets(user=None):
    if not user.is_authenticated:
        user = None
    return Snippet.objects.filter(Q(allow_view=True)
        | Q(author=user) | Q(editors=user))


def recent_snippets(user=None, count=20):
    return viewable_snippets(user).order_by('created_at').reverse()[:count]
