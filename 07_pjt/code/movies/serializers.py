from rest_framework import serializers
from .models import Movie, Review, Actor


class MovieSerializer(serializers.ModelSerializer):
    actors = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = '__all__'

    def get_actors(self, movie):
        actors = movie.actors.all()
        return [{'name': actor.name} for actor in actors]

    def get_reviews(self, movie):
        reviews = movie.review_set.all()
        return [{'title': review.title, 'content':review.content} for review in reviews]


class ActorSerializer(serializers.ModelSerializer):
    movies = serializers.SerializerMethodField()

    class Meta:
        model = Actor
        fields = '__all__'
    
    def get_movies(self, actor):
        movies = actor.movie_set.all()
        return [{'title': movie.title} for movie in movies]

class ReviewSerializer(serializers.ModelSerializer):
    # movie_title = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('movie', )
    
    # def get_movies(self, review, movie):
    #     movie_title = review.movie.get(pk=movie)
    #     return {}