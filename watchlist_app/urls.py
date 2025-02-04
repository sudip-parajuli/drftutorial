from django.contrib import admin
from django.urls import path
from .api.v1.views.movie import MovieListAv, MovieDetailAV, StreamListAv, StreamDetailAV, ReviewList, ReviewDetail
from rest_framework.routers import DefaultRouter


# router = DefaultRouter()
# router.register(r'review', ReviewViewSet, basename='review')



urlpatterns = [
    # path("list/", movie_list, name='movie-list'),
    # path("<int:pk>/", movie_details, name='movie-details'),

    #movie
    path("list/", MovieListAv.as_view(), name='movie-list'),
    path("<int:pk>/", MovieDetailAV.as_view(), name='movie-details'),

    #stream
    path("stream/", StreamListAv.as_view(), name='stream-list'),
    path("stream/<int:pk>/", StreamDetailAV.as_view(), name='stream-details'),

    #review
    path("review/", ReviewList.as_view(), name='review-list'),
    path("review/<int:pk>/", ReviewDetail.as_view(), name='review-details'),

    # path("review/", ReviewViewSet.as_view({'get':'list'}), name='review-list'),
    # path("review/<int:pk>/", ReviewViewSet.as_view({'get':'retrieve'}), name='review-details'),
]
               # +router.urls)




