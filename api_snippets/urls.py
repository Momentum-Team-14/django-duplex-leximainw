from django.urls import path
from . import views

urlpatterns = [
    path('api/snippets/<int:pk>/favorite/', views.snippet_favorite, name='Favorite snippet'),
]
