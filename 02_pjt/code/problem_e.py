import requests
from pprint import pprint


def credits(title):
    Search_URL = 'https://api.themoviedb.org/3/search/movie'
    Search_params = {
        'api_key' : '5056d5947b6f2c6e202377ace3152f12', 
        'language' : 'ko-KR',
        'query' : title,
        'region' : 'KR',
    }
    Search_response = requests.get(Search_URL, params = Search_params).json()

    movies_list = Search_response['results']
    if len(movies_list) == 0:
        return None
    else:
        movie_id = movies_list[0]['id']
    
    Credit_URL = f'https://api.themoviedb.org/3/movie/{movie_id}/credits'
    Credit_params = {
        'api_key' : '5056d5947b6f2c6e202377ace3152f12', 
        'language' : 'ko-KR',
        'movie_id' : movie_id,
    }
    Credit_response = requests.get(Credit_URL, params = Credit_params).json()
    print(Credit_response)
    cast_list = Credit_response['cast']
    crew_list = Credit_response['crew']
    movie_dict = {'cast' : [], 'directing' : []}

    for cast in cast_list:
        if cast['cast_id'] < 10:
            movie_dict['cast'].append(cast['name'])
    
    for crew in crew_list:
        if crew['department'] == 'Directing':
            movie_dict['directing'].append(crew['name'])
 

    # return movie_dict




# 아래의 코드는 수정하지 않습니다.
if __name__ == '__main__':
    """
    제목에 해당하는 영화가 있으면 해당 영화 id를 통해 영화 상세정보를 검색하여 주연배우 목록(cast)과 스태프(crew) 중 연출진 목록을 반환
    영화 id 검색에 실패할 경우 None을 반환
    """
    pprint(credits('기생충'))
    # {'cast': ['Song Kang-ho', 'Lee Sun-kyun', ..., 'Jang Hye-jin'], 'crew': ['Bong Joon-ho', 'Park Hyun-cheol', ..., 'Yoon Young-woo']}
    pprint(credits('검색할 수 없는 영화'))
    # None
