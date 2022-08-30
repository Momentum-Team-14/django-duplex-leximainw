from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='Homepage'),
    path('snippets/recent/', views.snippets_recent, name='Recent snippets'),
    path('snippets/new/', views.snippets_edit, name='Create snippet'),
    path('snippets/<int:pk>/', views.snippets_details, name='Snippet details'),
    path('snippets/<int:pk>/edit/', views.snippets_edit, name='Edit snippet'),
    path('snippets/<int:pk>/delete/', views.snippets_delete, name='Delete snippet'),
    path('snippets/<int:pk>/fork/', views.snippets_fork, name='Fork snippet'),
]
