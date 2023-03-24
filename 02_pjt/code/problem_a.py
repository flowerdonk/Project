import requests

def popular_count():
    URL = 'https://api.themoviedb.org/3/movie/popular'
    params = {
    'api_key' : '5056d5947b6f2c6e202377ace3152f12', 
    'language' : 'ko-KR',
    'region' : 'KR'
    }
    
    response = requests.get(URL, params = params).json()

    return len(response['results'])

# 아래의 코드는 수정하지 않습니다.
if __name__ == '__main__':
    """
    popular 영화목록의 개수 반환
    """
    print(popular_count())
    # 20
