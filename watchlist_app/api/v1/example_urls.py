from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import examples

router = DefaultRouter()
router.register('watchlist', examples.WatchlistViewSet, basename='example-watchlist')
router.register('stream_platform', examples.StreamPlatformViewSet, basename='example-platform')

urlpatterns = [
    path('django/movies/', examples.django_movie_list),
    path('django/movies/<int:pk>/', examples.django_movie_detail),
    path('functions/movies/', examples.movie_list),
    path('functions/movies/<int:pk>/', examples.movie_detail),
    path('manual/movies/', examples.ManualMovieList.as_view()),
    path('manual/movies/<int:pk>/', examples.ManualMovieDetail.as_view()),
    path('mixins/watchlist/', examples.WatchlistCRUDView.as_view(http_method_names=['get', 'post', 'head', 'options']), name='example-mixin-list'),
    path('mixins/watchlist/<int:pk>/', examples.WatchlistCRUDView.as_view(http_method_names=['get', 'put', 'patch', 'delete', 'head', 'options']), name='example-mixin-detail'),
    path('generic/watchlist/', examples.WatchlistView.as_view()),
    path('generic/watchlist/<int:pk>/', examples.WatchListDetailView.as_view()),
    path('generic/update/<int:pk>/', examples.WatchListUpdateView.as_view()),
    path('generic/crud/<int:pk>/', examples.WatchListRetrieveUpdateDeleteView.as_view()),
    path('generic/netflix/', examples.NetflixWatchListView.as_view()),
    path('router/', include(router.urls)),
]
