"""Distinct view styles from RESTFrameworkTutorial using shared models."""
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from watchlist_app.models import Movie, WatchList, StreamPlatform
from watchlist_app.api.v1.permissions import IsAdminOrReadOnly
from watchlist_app.api.v1.serializers.foundations import FoundationMovieSerializer, ManualMovieSerializer
from watchlist_app.api.v1.serializers.movie import MovieSerializer, NestedStreamSerializer


def django_movie_list(request):
    """Plain Django JSON, before introducing DRF responses."""
    return JsonResponse({'movies': list(Movie.objects.values('id', 'name', 'description', 'active'))})


def django_movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    return JsonResponse({'id': movie.pk, 'name': movie.name, 'description': movie.description, 'active': movie.active})


@api_view(['GET', 'POST'])
@permission_classes([IsAdminOrReadOnly])
def movie_list(request):
    if request.method == 'GET':
        return Response(FoundationMovieSerializer(Movie.objects.all(), many=True).data)
    serializer = FoundationMovieSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAdminOrReadOnly])
def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == 'GET':
        return Response(FoundationMovieSerializer(movie).data)
    if request.method == 'DELETE':
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    serializer = FoundationMovieSerializer(movie, data=request.data, partial=request.method == 'PATCH')
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


class ManualMovieList(generics.ListCreateAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Movie.objects.all()
    serializer_class = ManualMovieSerializer


class ManualMovieDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Movie.objects.all()
    serializer_class = ManualMovieSerializer


class WatchlistCRUDView(mixins.ListModelMixin, mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin, generics.GenericAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = WatchList.objects.select_related('platform')
    serializer_class = MovieSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs) if 'pk' in kwargs else self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class WatchlistView(generics.ListAPIView):
    queryset = WatchList.objects.select_related('platform')
    serializer_class = MovieSerializer


class WatchListDetailView(generics.RetrieveAPIView):
    queryset = WatchList.objects.select_related('platform')
    serializer_class = MovieSerializer


class WatchListUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = WatchList.objects.all()
    serializer_class = MovieSerializer


class WatchListRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = WatchList.objects.select_related('platform')
    serializer_class = MovieSerializer


class NetflixWatchListView(WatchlistView):
    def get_queryset(self):
        return super().get_queryset().filter(platform__name='Netflix')


class WatchlistViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = WatchList.objects.select_related('platform')
    serializer_class = MovieSerializer


class StreamPlatformViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = StreamPlatform.objects.prefetch_related('movies')
    serializer_class = NestedStreamSerializer
