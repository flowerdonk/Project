# movies/views.py

from django.shortcuts import render
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import ActorSerializer, MovieSerializer, ReviewSerializer
from .models import Movie, Actor, Review

@api_view(['GET'])
def actor_list(request):
    if request.method == 'GET':
        actors = get_list_or_404(Actor)
        serializer = ActorSerializer(actors, many=True)
        data = serializer.data
        [item.pop('movies') for item in data]
        return Response(data)

@api_view(['GET'])
def actor_detail(request, actor_pk):
    if request.method == 'GET':
        actor = get_object_or_404(Actor, pk=actor_pk)
        serializer = ActorSerializer(actor)
        return Response(serializer.data)

@api_view(['GET'])
def movie_list(request):
    if request.method == 'GET':
        movies = get_list_or_404(Movie)
        serializer = MovieSerializer(movies, many=True)
        data = serializer.data
        [item.pop('id') for item in data]
        [item.pop('release_date') for item in data]
        [item.pop('poster_path') for item in data]
        [item.pop('actors') for item in data]
        return Response(data)

@api_view(['GET'])
def movie_detail(request, movie_pk):
    if request.method == 'GET':
        movie = get_object_or_404(Movie, pk=movie_pk)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)

@api_view(['GET'])
def review_list(request):
    if request.method == 'GET':
        reviews = get_list_or_404(Review)
        serializer = ReviewSerializer(reviews, many=True)
        data = serializer.data
        [item.pop('id') for item in data]
        [item.pop('movie') for item in data]
        return Response(data)

@api_view(['GET','PUT','DELETE'])
def review_detail(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.method == 'GET':
        serializer = ReviewSerializer(review)
    elif request.method == 'PUT':
        serializer = ReviewSerializer(review, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    data = serializer.data
    movie_pk = data["movie"]
    movie_title = Movie.objects.get(pk=movie_pk).title
    data["movie"] = {"title" : movie_title}
    return Response(data)

@api_view(['POST'])
def create_review(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.method == 'POST':
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(movie=movie)
            return Response(serializer.data, status=status.HTTP_201_CREATED)