import json
from pprint import pprint # pprint는 이 방식으로 임포트!


def movie_info(movie):
    # print(movie) 전달받는 인자 확인(사용할 내용 확인)
    # id, title, poster_path, vote_average, overview, genre_ids
    result = {
        'id' : movie['id'], 
        'title' : movie['title'],
        'poster_path' : movie.get('poster_path'), 
        'vote_average' : movie.get('vote_average'),
        'overview' : movie.get('overview'),
        'genre_ids' : movie.get('genre_ids')
    }
    return result



# 아래의 코드는 수정하지 않습니다.
if __name__ == '__main__':
    movie_json = open('data/movie.json', encoding='utf-8')
    movie_dict = json.load(movie_json)
    
    pprint(movie_info(movie_dict))
