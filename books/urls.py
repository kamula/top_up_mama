from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('books', views.get_name_authors_comments,
         name='get_name_authors_comments')
]
