import json
from pprint import pprint


def movie_info(movie, genres):
    # id,title,poster_path,vote_average,overview,genre_ids
    
    genre_names = dict()
    for item in genres:
        genre_names[item['id']] = item['name']

    movie_genre = [
        genre_names[movie.get('genre_ids')[0]], 
        genre_names[movie.get('genre_ids')[1]]
        ]
        
    result = {
        'id' : movie.get('id'), 
        'title' : movie.get('title'),
        'poster_path' : movie.get('poster_path'), 
        'vote_average' : movie.get('vote_average'),
        'overview' : movie.get('overview'),
        'genre_names' : movie_genre
      }

    return result
        

# 아래의 코드는 수정하지 않습니다.
if __name__ == '__main__':
    movie_json = open('data/movie.json', encoding='utf-8')
    movie = json.load(movie_json)

    genres_json = open('data/genres.json', encoding='utf-8')
    genres_list = json.load(genres_json)

    pprint(movie_info(movie, genres_list))
