import json
from pprint import pprint


def movie_info(movies, genres):
    # id,title,poster_path,vote_average,overview,genre_names
    genre_names = dict()
    for item in genres:
        genre_names[item['id']] = item['name']
        
    result = []

    for movie in movies:

        movie_genre = []
        for i in range(len(movie.get('genre_ids'))):
            movie_genre.append(genre_names[movie.get('genre_ids')[i]])
        
        result.append({
        'id' : movie.get('id'), 
        'title' : movie.get('title'),
        'poster_path' : movie.get('poster_path'), 
        'vote_average' : movie.get('vote_average'),
        'overview' : movie.get('overview'),
        'genre_ids' : movie_genre
        })

    return result
        
# 아래의 코드는 수정하지 않습니다.
if __name__ == '__main__':
    movies_json = open('data/movies.json', encoding='utf-8')
    movies_list = json.load(movies_json)

    genres_json = open('data/genres.json', encoding='utf-8')
    genres_list = json.load(genres_json)

    pprint(movie_info(movies_list, genres_list))
