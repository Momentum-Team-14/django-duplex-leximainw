from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='Homepage'),
    path('snippets/recent/', views.snippets_recent, name='Recent Snippets'),
    path('snippets/new/', views.snippets_edit, name='Create Snippet'),
    path('snippets/<int:pk>/edit/', views.snippets_edit, name='Edit snippet'),
    path('snippets/<int:pk>/', views.snippets_details, name='Snippet details'),
]
