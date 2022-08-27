import imp
from api_snippets.models import Snippet

def recent_snippets(user=None, count=20):
    if not user.is_authenticated:
        user = None
    recent = Snippet.objects.order_by('created_at').reverse()[:count]
    result = []
    for snippet in recent:
        if snippet.can_view(user):
            result.append(snippet)
    return result
