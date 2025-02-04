from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status,mixins,generics,viewsets
from rest_framework.mixins import ListModelMixin, CreateModelMixin,RetrieveModelMixin,UpdateModelMixin, DestroyModelMixin
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated,IsAdminUser,IsAuthenticatedOrReadOnly
from watchlist_app.api.v1.permissions import IsAdminOrReadOnly,IsReviewUserOrReadOnly

from watchlist_app.api.v1.serializers.movie import MovieSerializer, StreamSerializer, ReviewSerializer
# from watchlist_app.models import Movie
from watchlist_app.models import WatchList,StreamPlatform,Review





# Create your views here.
# def movie_list(request):
#     movies = Movie.objects.all()
#     # print(list(movies.values()))
#     data = {
#         'movies': list(movies.values())
#     }
#     return JsonResponse(data)

# @api_view(['GET', 'POST'])
# def movie_list(request):
#     if request.method == 'GET':
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies, many=True)
#         return Response(serializer.data)
#     if request.method == 'POST':
#         serializer = MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'success': True})
#         else:
#             return Response(serializer.errors)
#         # name = request.data['name']
#         # description = request.data['description']
#         # active = request.data['active']




# def movie_details(request, pk):
#     try:
#         movie = Movie.objects.get(pk=pk)
#         data = {
#             'name': movie.name,
#             'description': movie.description,
#             'active': movie.active
#         }
#         return JsonResponse(data)
#     except Movie.DoesNotExist:
#         return JsonResponse({
#             'error': 'No such movie!'
#         })

# @api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
# def movie_details(request, pk):
#     if request.method == 'GET':
#         try:
#             movie = Movie.objects.get(pk=pk)
#         except Movie.DoesNotExist:
#             return Response({
#                 'error': 'No such movie!'
#             })
#         serializer = MovieSerializer(movie)
#         return Response(serializer.data)
#
#     if request.method == 'PATCH':
#         movie = Movie.objects.get(pk=pk)
#         serializer = MovieSerializer(instance=movie, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'success': True})
#         else:
#             return Response(serializer.errors)
#
#     if request.method == 'PUT':
#         pass
#
#     if request.method == 'DELETE':
#         movie = Movie.objects.get(pk=pk)
#         movie.delete()
#         return Response({'success': True})

"""............................................................................"""

class MovieListAv(APIView):
    def get(self,request):
        movies=WatchList.objects.all()
        serializer=MovieSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer=MovieSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MovieDetailAV(APIView):
    def get(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({
                'error': 'No such movie!'
            })
        serializer=MovieSerializer(movie)
        return  Response(serializer.data)

    def patch(self,request,pk):
        movie=WatchList.objects.get(pk=pk)
        serializer = MovieSerializer(instance=movie, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        movie=WatchList.objects.get(pk=pk)
        serializer=MovieSerializer(instance=movie, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        movie=WatchList.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class StreamListAv(APIView):
    def get(self,request):
        streamer=StreamPlatform.objects.all()
        serializer=StreamSerializer(streamer, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer=StreamSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class StreamDetailAV(APIView):
    def get(self, request, pk):
        try:
            streamer = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({
                'error': 'No such stream platform!'
            })
        serializer=StreamSerializer(streamer)
        return  Response(serializer.data)

    def patch(self,request,pk):
        streamer=StreamPlatform.objects.get(pk=pk)
        serializer = StreamSerializer(instance=streamer, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        streamer=StreamPlatform.objects.get(pk=pk)
        serializer=StreamSerializer(instance=streamer, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        streamer=StreamPlatform.objects.get(pk=pk)
        streamer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


"""...................................................................................................."""

"""Generic views and Mixins"""

# class ReviewList(mixins.ListModelMixin,CreateModelMixin, generics.GenericAPIView):
#     queryset=Review.objects.all()
#     serializer_class=ReviewSerializer
#
#     def get(self,request, *args, **kwargs):
#         return self.list(request,*args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.post(request, *args, **kwargs)

# class ReviewDetail(mixins.DestroyModelMixin,RetrieveModelMixin,UpdateModelMixin, generics.GenericAPIView):
#     queryset=Review.objects.all()
#     serializer_class=ReviewSerializer
#
#     def get(self,request, *args, **kwargs):
#         return self.retrieve(request,*args, **kwargs)
#
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
#     def patch(self, request, *args, **kwargs):
#         return self.partial_update(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)

"""................................................................................................"""

"""Concrete View Classes"""

class ReviewList(ListCreateAPIView):
    queryset=Review.objects.all()
    serializer_class=ReviewSerializer
    permission_classes = [IsAdminOrReadOnly, ]


class ReviewDetail(RetrieveUpdateDestroyAPIView):
    queryset=Review.objects.all()
    serializer_class=ReviewSerializer
    permission_classes = [IsReviewUserOrReadOnly, ]



""".........................................................................................."""

"""viewsets"""

# class ReviewViewSet(viewsets.ViewSet):
#     """
#     A simple ViewSet for listing or retrieving reviews.
#     """
#     def list(self, request):
#         queryset = Review.objects.all()
#         serializer = ReviewSerializer(queryset, many=True)
#         return Response(serializer.data)
#
#     def retrieve(self, request, pk=None):
#         queryset = Review.objects.all()
#         review = get_object_or_404(queryset, pk=pk)
#         serializer = ReviewSerializer(review)
#         return Response(serializer.data)



"""........................................................................................"""

"""ModelViewSets"""
# class ReviewViewSet(viewsets.ModelViewSet):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer












