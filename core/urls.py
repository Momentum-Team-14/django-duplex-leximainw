from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='Homepage'),
    path('snippets/recent/', views.snippets_recent, name='Recent Snippets'),
]
