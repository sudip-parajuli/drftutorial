from django.contrib import admin
from django.urls import path

from .api.v1.views.movie import movie_list, movie_details

urlpatterns = [
    path("list/", movie_list, name='movie-list'),
    path("<int:pk>/", movie_details, name='movie-details'),
]
