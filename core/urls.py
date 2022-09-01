from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='Homepage'),
    path('accounts/profile/', views.user_profile, name='Account profile'),
    path('accounts/<int:pk>/profile/', views.user_profile, name='User profile'),
    path('accounts/<int:pk>/profile/search', views.search_profile, name='Search profile'),
    path('snippets/recent/', views.snippets_recent, name='Recent snippets'),
    path('snippets/recent/search', views.snippets_recent, name='Search recent snippets'),
    path('snippets/new/', views.snippets_edit, name='Create snippet'),
    path('snippets/<int:pk>/', views.snippets_details, name='Snippet details'),
    path('snippets/<int:pk>/edit/', views.snippets_edit, name='Edit snippet'),
    path('snippets/<int:pk>/delete/', views.snippets_delete, name='Delete snippet'),
    path('snippets/<int:pk>/fork/', views.snippets_fork, name='Fork snippet'),
    path('languages/<str:name>/', views.languages_details, name='Language details'),
    path('languages/<str:name>/search', views.languages_search, name='Search by language'),
]
