from django.conf import settings
from django.db.models import Q
from api_snippets.models import Snippet


def viewable_snippets(user=None):
    if user is None or not user.is_authenticated:
        return Snippet.objects.filter(allow_view=True)
    else:
        return Snippet.objects.filter(Q(allow_view=True)
            | Q(author=user) | Q(editors=user))


def newest_viewable_snippets(user=None):
    return viewable_snippets(user).order_by('created_at').reverse()


def recent_snippets(user=None, count=settings.SEARCH_COUNT):
    return newest_viewable_snippets(user)[:count]


def search_snippets(queryset, search_text):
    search_terms = []
    curr_term = ""
    in_string = False
    escaped = False
    for char in search_text:
        if in_string:
            if escaped:
                curr_term += char
            elif char == '\\':
                escaped == True
            elif char == '"':
                in_string = False
                if len(curr_term):
                    search_terms.append(curr_term)
                curr_term = ""
            else:
                curr_term += char
            pass
        elif escaped:
            curr_term += char
            escaped = False
        elif char.isspace():
            if len(curr_term):
                search_terms.append(curr_term)
            curr_term = ""
        elif char == '"':
            if len(curr_term):
                search_terms.append(curr_term)
            curr_term = ""
            in_string = True
        elif char == '\\':
            escaped = True
        else:
            curr_term += char
    if len(curr_term):
        search_terms.append(curr_term)
    if len(search_terms) > 8:
        search_terms = search_terms[0:8]
    print(len(search_terms))
    for term in search_terms:
        print(term)
        queryset = queryset.filter(Q(title__icontains=term)
            | Q(language__name__icontains=term)
            | Q(description__icontains=term)
            | Q(code__icontains=term))
    return queryset
