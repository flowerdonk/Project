import requests
from pprint import pprint


def recommendation(title):
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
        
    Reco_URL = f'https://api.themoviedb.org/3/movie/{movie_id}/recommendations'
    Reco_params = {
    'api_key' : '5056d5947b6f2c6e202377ace3152f12',
    'movie_id' : movie_id,
    'language' : 'ko-KR',
    }
    Reco_response = requests.get(Reco_URL, params = Reco_params).json()
    Reco_movies_list = Reco_response['results']
    Recommend_list = []

    if len(Reco_movies_list) != 0:

        for movie in Reco_movies_list:
            Recommend_list.append(movie['title'])

    return Recommend_list


# 아래의 코드는 수정하지 않습니다.
if __name__ == '__main__':
    """
    제목에 해당하는 영화가 있으면 해당 영화의 id를 기반으로 추천 영화 목록 구성
    추천 영화가 없을 경우 []를 반환
    영화 id 검색에 실패할 경우 None을 반환
    (주의) 추천 영화의 경우 아래 예시 출력과 차이가 있을 수 있음
    """
    pprint(recommendation('기생충'))
    # ['조커', '1917', '조조 래빗', ..생략.., '살인의 추억', '펄프 픽션']
    pprint(recommendation('그래비티'))
    # []
    pprint(recommendation('검색할 수 없는 영화'))
    # None
