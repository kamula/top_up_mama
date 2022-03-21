from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_name_authors_comments,
         name='get_name_authors_comments'),
    path('characters/<str:id>/', views.get_character_list, name='get_character_list')
]
