from django.urls import path
from .api.v1.views.movie import MovieListAv, MovieDetailAV, StreamListAv, StreamDetailAV, ReviewList, ReviewDetail

urlpatterns = [
    path('list/', MovieListAv.as_view(), name='movie-list'),
    path('<int:pk>/', MovieDetailAV.as_view(), name='movie-details'),
    path('stream/', StreamListAv.as_view(), name='stream-list'),
    path('stream/<int:pk>/', StreamDetailAV.as_view(), name='stream-details'),
    path('review/', ReviewList.as_view(), name='review-list'),
    path('review/<int:pk>/', ReviewDetail.as_view(), name='review-details'),
    path('review/<str:username>/', ReviewList.as_view(), name='review-by-user'),
]
