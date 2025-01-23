from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from watchlist_app.api.v1.serializers.movie import MovieSerializer
from watchlist_app.models import Movie


# Create your views here.
# def movie_list(request):
#     movies = Movie.objects.all()
#     # print(list(movies.values()))
#     data = {
#         'movies': list(movies.values())
#     }
#     return JsonResponse(data)

@api_view(['GET', 'POST'])
def movie_list(request):
    if request.method == 'GET':
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True})
        else:
            return Response(serializer.errors)
        # name = request.data['name']
        # description = request.data['description']
        # active = request.data['active']


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

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def movie_details(request, pk):
    if request.method == 'GET':
        try:
            movie = Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            return Response({
                'error': 'No such movie!'
            })
        serializer = MovieSerializer(movie)
        return Response(serializer.data)

    if request.method == 'PATCH':
        movie = Movie.objects.get(pk=pk)
        serializer = MovieSerializer(instance=movie, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True})
        else:
            return Response(serializer.errors)

    if request.method == 'PUT':
        pass

    if request.method == 'DELETE':
        movie = Movie.objects.get(pk=pk)
        movie.delete()
        return Response({'success': True})
