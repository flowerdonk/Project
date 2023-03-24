# PJT 02

### 이번 PJT를 통해 배운 내용

- Python 기본 문법 습득
- 데이터 구조에 대한 분석과 이해
- 요청과 응답에 대한 이해
- API의 활용과 API 문서 숙지

---

## A. 인기 영화 조회 (problem_a)

> 📌 **요구사항**
> 
> 
> 인기 영화 목록을 응답 받아 개수를 출력
> 

- **결과 :**
    - 문제 접근 방법 및 코드 설명
    
    ✔ 인기 영화(딕셔너리) 내부 목록(리스트)에 접근
    
    ```python
    def popular_count():
        URL = 'https://api.themoviedb.org/3/movie/popular'
        params = {
        'api_key' : '5056d5947b6f2c6e202377ace3152f12', 
        'language' : 'ko-KR',
        'region' : 'KR'
        }
    
        response = requests.get(URL, params = params).json()
    
        return len(response['results'])
    ```
    
    1. `URL` , `params`
        
        주소, 함수 파라미터로 전달할 내용들
        
    2. `response` 
        
        `requests` 내부 메소드 `.get()` 을 통해 `.json()` 형태의 인기 영화 목록을 받음
        
        `response` : `{'page' : 1, 'results' : [{'adult' : False, ... , }, ...], ...}`
        
    3. `return` 
        
        인기 영화 목록의 갯수를 `len()` 을 통해 반환
        
    
    - 이 문제에서 어려웠던 점
    
    새로운 형태의 데이터 구조에 익숙해지는 것
    

<aside>
💡 **내가 생각하는 이 문제의 포인트**

딕셔너리/리스트 구조 파악

</aside>

---

## B. 특정 조건에 맞는 인기 영화 조회 1 (problem_b)

> 📌 **요구 사항**
> 
> 
> 인기 영화 목록 중 평점이 8점 이상인 영화 목록 출력
> 

- **결과 :**
    - 문제 접근 방법 및 코드 설명
    
    ✔ 인기 영화(딕셔너리)에서 목록(리스트)를 받고, 목록 안의 영화 데이터들(딕셔너리)에 접근
    
    ```python
    def vote_average_movies():
        URL = 'https://api.themoviedb.org/3/movie/popular'
        params = {
        'api_key' : '5056d5947b6f2c6e202377ace3152f12', 
        'language' : 'ko-KR',
        'region' : 'KR'
        }
    
        response = requests.get(URL, params = params).json()
        movie_list = response['results']
        high_movies = []
    
        for movie in movie_list:
          if movie['vote_average'] >= 8.0:
            high_movies.append(movie)
    
        return high_movie
    ```
    
    1. `URL` , `params`
        
        주소, 함수 파라미터로 전달할 내용들
        
    2. `response` 
        
        `requests` 내부 메소드 `.get()` 을 통해 `.json()` 형태의 인기 영화 목록을 받음
        
        `response` : `{'page' : 1, 'results' : [{'adult' : False, ... , }, ...], ...}`
        
    3. `movie_list`
        
        `response` 중에서 `'results'` 값을 `movie_list` 에 담음
        
    4. `high_movies`
        
        평점이 8.0 이상인 영화를 찾아 이를 `high_movies`  리스트에 담음
        
    5. `return` 
        
        `high_movies` 반환
        
    - 이 문제에서 어려웠던 점
    
    딕셔너리/리스트/딕셔너리 구조에서 최하단 딕셔너리의 값에 접근하는 방법
    

<aside>
💡 **내가 생각하는 이 문제의 포인트**

딕셔너리/리스트/딕셔너리 구조 파악

</aside>

---

## C. 특정 조건에 맞는 인기 영화 조회 2 (problem_c)

> 📌 **요구 사항**
> 
> 
> 인기 영화 목록을 평점이 높은 순으로 5개의 영화 데이터 목록 출력
> 

- **결과 :**
    - 문제 접근 방법 및 코드 설명
    
    ✔ 인기 영화(딕셔너리)에서 목록(리스트)를 받고, 목록 안의 영화 데이터들(딕셔너리) 정렬
    
    ```python
    def ranking():
        URL = 'https://api.themoviedb.org/3/movie/popular'
        params = {
        'api_key' : '5056d5947b6f2c6e202377ace3152f12', 
        'language' : 'ko-KR',
        'region' : 'KR'
        }
    
        response = requests.get(URL, params = params).json()
        movie_list = response['results']
        Top5_movies = []
    
        movie_list = sorted(movie_list, key = lambda item : item['vote_average'], reverse=True)
    
        for i in range(5):
          Top5_movies.append(movie_list[i])
    
        return Top5_movies 
    ```
    
    1. `URL` , `params`
        
        주소, 함수 파라미터로 전달할 내용들
        
    2. `response` 
        
        `requests` 내부 메소드 `.get()` 을 통해 `.json()` 형태의 인기 영화 목록을 받음
        
        `response` : `{'page' : 1, 'results' : [{'adult' : False, ... , }, ...], ...}`
        
    3. `movie_list`
        
        `response` 중에서 `'results'` 값을 `movie_list` 에 담음
        
        이후 `sorted()` 를 통해 `'vote_average'` 키를 기준으로 내림차순 정렬
        
    4. `Top5_movies`
        
        정렬된 `movie_list` 의 앞에서 5번째까지의 원소를 담는 리스트 
        
    5. `return` 
        
        `Top5_movies` 반환
        
    
    - 이 문제에서 어려웠던 점
    
    새로 배운 람다함수를 활용한 정렬 방식을 적용하는 것
    

<aside>
💡 **내가 생각하는 이 문제의 포인트**

람다를 활용한 정렬 → `sorted(dict, key = lambda item : item['key'], reverse=True)`

</aside>

---

## D. 특정 추천 영화 조회 (problem_d)

> 📌 **요구 사항**
> 
> 
> 제공된 영화 제목(’기생충’, ‘그래비티’, ‘검색할 수 없는 영화’) 검색, 추천 영화 목록 출력
> 

- **결과 :**
    - 문제 접근 방법 및 코드 설명
    
    ✔ 첫 번째 데이터에서 추출한 정보로 두 번째 데이터 접근
    
    ```python
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
    ```
    
    1. `Search_URL` , `Search_params`
        
        주소, 함수 파라미터로 전달할 내용들
        
        인자로 받은 영화 제목을 `'query' : {title}` 에 넣음
        
    2. `Search_response` 
        
        `requests` 내부 메소드 `.get()` 을 통해 `.json()` 형태의 인기 영화 목록을 받음
        
        `Search_response` : `{'page':1, 'results':[{'adult' : False, ...}, ...], ...}`
        
    3. `movie_list`
        
        `Search_response` 중에서 `'results'` 값을 `movie_list` 에 담음
        
    4. `if`
        
        조건문을 통해 리스트가 비어있을 경우 `return None` 후 함수에서 벗어남
        
        비어있지 않은 경우, `movie_id` 변수에 `movies_list` 첫 번째 원소의 `'id'` 값 담음
        
    5. `Reco_URL` , `Reco_params`
        
        파라미터에 앞에서 구한 영화의 id 값 넣기 `'movie_id' : {movie_id}`
        
    6. `Reco_response` 
        
        `requests` 내부 메소드 `.get()` 을 통해 `.json()` 형태의 인기 영화 목록을 받음
        
        `Reco_response` : `{'page':1, 'results':[{'adult' : False, ...}, ...], ...}`
        
    7. `Reco_movies_list`
        
        `Reco_response` 중에서 `'results'` 값을 `Reco_movies_list` 에 담음
        
    8. `Recommend_list`
        
        `Reco_movies_list` 가 비어있지 않으면, `'title'` 값을 `Recommend_list` 에 담음
        
    9. `return` 
        
        `Recommend_list` 반환
        
    
    - 이 문제에서 어려웠던 점
    
    앞선 문제들과는 다르게 데이터 두 개에 접근
    → 처음 데이터에서 받은 내용을 두번째 데이터에 접근하기 위한 파라미터로 사용
    

<aside>
💡 **내가 생각하는 이 문제의 포인트**

스트링으로 사용 가능한 f-string → f’ ~ {} ‘

</aside>

---

## E. 출연진, 연출진 데이터 조회 (problem_e)

> 📌 **요구 사항**
> 
> 
> 제공된 영화 제목(’기생충’, ‘검색할 수 없는 영화’) 검색,
> 해당 영화의 출연진(cast)과 스태프(crew) 중 연출진(Directing)의 이름 출력
> 

- **결과 :**
    - 문제 접근 방법 및 코드 설명
    
    ✔ 첫 번째 데이터에서 추출한 정보로 두 번째 데이터 접근, 두 번째 데이터의 2개 정보에 접근
    
    ```python
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
        cast_list = Credit_response['cast']
        crew_list = Credit_response['crew']
        movie_dict = {'cast' : [], 'directing' : []}
    
        for cast in cast_list:
            if cast['cast_id'] < 10:
                movie_dict['cast'].append(cast['name'])
        
        for crew in crew_list:
            if crew['department'] == 'Directing':
                movie_dict['directing'].append(crew['name'])
    
        return movie_dict
    ```
    
    1. `Search_URL` , `Search_params`
        
        주소, 함수 파라미터로 전달할 내용들
        
        인자로 받은 영화 제목을 `'query' : {title}` 에 넣음
        
    2. `Search_response` 
        
        `requests` 내부 메소드 `.get()` 을 통해 `.json()` 형태의 인기 영화 목록을 받음
        
        `Search_response` : `{'page':1, 'results':[{'adult' : False, ...}, ...], ...}`
        
    3. `movie_list`
        
        `Search_response` 중에서 `'results'` 값을 `movie_list` 에 담음
        
    4. `if`
        
        조건문을 통해 리스트가 비어있을 경우 `return None` 후 함수에서 벗어남
        
        비어있지 않은 경우, `movie_id` 변수에 `movies_list` 첫 번째 원소의 `'id'` 값 담음
        
    5. `Credit_URL` , `Credit_params`
        
        파라미터에 앞에서 구한 영화의 id 값 넣기 `'movie_id' : {movie_id}`
        
    6. `Credit_response` 
        
        `requests` 내부 메소드 `.get()` 을 통해 `.json()` 형태의 인기 영화 목록을 받음
        
        `Credit_response` : `{'id':1, 'cast':[{'adult' : False, ...}, ...], 'crew':[{'adult' : False, ...}, ...]}`
        
    7. `cast_list` , `crew_list` 
        
        `Credit_response` 중에서 `'cast'` 값을 `cast_list` 에, `'crew'` 값을 `crew_list` 담음
        
    8. `movie_dict`
        
        `cast_list` 에서 `'cast_id'` 값이 10 미만인 이름 `movie_dict['cast']` 에, 
        `crew_list` 에서 `'department'` 값이 `'Directing'` 인 이름 `movie_dict['directing']`  추가
        
    9. `return` 
        
        `movie_dict` 반환
        
    
    - 이 문제에서 어려웠던 점
    
    이전까지의 데이터 구조와 완전 달랐던 `credits` 에 접근하는 것
    

<aside>
💡 **내가 생각하는 이 문제의 포인트**

데이터 → 데이터 (2개) 로의 연결 구조

</aside>

---

# 후기

- 매번 같은 형식이 아닌, 다양한 형식의 데이터를 다루는 법을 터득하게 되었다. 또한 데이터의 형식마다 접근해야하는 방법이 달라 어려움을 겪었지만, 여러번의 연습을 통해 데이터 구조 파악과 접근 방식에 대한 감을 잡을 수 있게 되었다.
- 딕셔너리 - 리스트 - 딕셔너리 구조에서 각각의 정보에 접근하는 방법을 차례대로 파악해갈 수 있었다.
- 무료 API를 TMDB에서 발급받고, 이를 활용해 데이터를 크롤링하는 연습을 할 수 있었다.