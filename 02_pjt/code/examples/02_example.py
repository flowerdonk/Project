# requests 사용 예시 2

import requests


# URL = 'https://api.agify.io'

# params = {
#     'name': 'michael',
#     'country_id': 'KR',
# }

# response = requests.get(URL, params=params).json()
# print(response)

URL = 'https://api.themoviedb.org/3/movie/315162'
movie_id = 1

params = {
    'api_key' : '5056d5947b6f2c6e202377ace3152f12', 
}

response = requests.get(URL, params = params).json()
print(response)