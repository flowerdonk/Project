import json


def dec_movies(movies):
    december = []

    for movie in movies:
        id = movie['id']
        movie_json = open(f'data/movies/{id}.json', encoding='utf-8')
        detail = json.load(movie_json)

        date = detail.get('release_date')
        date_list = list(date.split('-'))
        reve = detail.get('revenue')
        if reve:
            if int(date_list[1]) == 12:
                december.append(movie.get('title'))            

    return december
        

# 아래의 코드는 수정하지 않습니다.
if __name__ == '__main__':
    movies_json = open('data/movies.json', encoding='utf-8')
    movies_list = json.load(movies_json)
    
    print(dec_movies(movies_list))
