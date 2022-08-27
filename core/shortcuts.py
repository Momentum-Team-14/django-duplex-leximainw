import imp
from api_snippets.models import Snippet

def recent_snippets(count=20):
    return Snippet.objects.order_by('created_at').reverse()[:count]
