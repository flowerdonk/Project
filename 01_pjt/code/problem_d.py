import json
from pprint import pprint


def max_revenue(movies):
    max_title = ''
    max_number = 0

    for movie in movies:
        id = movie['id']
        movie_json = open(f'data/movies/{id}.json', encoding='utf-8')
        detail = json.load(movie_json)

        reve = detail.get('revenue')
        if reve > max_number:
            max_number = reve
            max_title = detail.get('title')

    return max_title
        
        
# 아래의 코드는 수정하지 않습니다.
if __name__ == '__main__':
    movies_json = open('data/movies.json', encoding='utf-8')
    movies_list = json.load(movies_json)
    
    print(max_revenue(movies_list))
