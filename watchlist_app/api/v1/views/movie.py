"""The consolidated watchlist API, preserving the existing /movie/ routes."""
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from watchlist_app.models import WatchList, StreamPlatform, Review
from watchlist_app.api.v1.serializers.movie import MovieSerializer, StreamSerializer, ReviewSerializer
from watchlist_app.api.v1.permissions import IsAdminOrReadOnly, IsReviewUserOrReadOnly
from watchlist_app.api.v1.pagination import CustomCursorPagination
from watchlist_app.api.v1.throttles import ReviewRateThrottle


class MovieListAv(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        return Response(MovieSerializer(WatchList.objects.select_related('platform'), many=True).data)

    def post(self, request):
        serializer = MovieSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MovieDetailAV(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = WatchList.objects.select_related('platform')
    serializer_class = MovieSerializer


class StreamListAv(generics.ListCreateAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = StreamPlatform.objects.prefetch_related('movies')
    serializer_class = StreamSerializer


class StreamDetailAV(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = StreamPlatform.objects.prefetch_related('movies')
    serializer_class = StreamSerializer


class ReviewList(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['rating', 'active']
    search_fields = ['review_user__username', 'description']
    ordering_fields = ['rating', 'created', 'id']
    pagination_class = CustomCursorPagination
    throttle_classes = [ReviewRateThrottle]

    def get_queryset(self):
        queryset = Review.objects.select_related('review_user', 'watchlist')
        username = self.kwargs.get('username') or self.request.query_params.get('username')
        return queryset.filter(review_user__username=username) if username else queryset

    def perform_create(self, serializer):
        serializer.save(review_user=self.request.user)


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.select_related('review_user', 'watchlist')
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsReviewUserOrReadOnly]
