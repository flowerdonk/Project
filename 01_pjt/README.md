# PJT 01

### 이번 PJT를 통해 배운 내용

- Python을 활용한 데이터 수집
- 파일 입출력, 데이터 구조
- 데이터를 가공하고 JSON 형태로 구성
- 

---

## A. 제공되는 영화 데이터의 주요내용 수집 (problem_a)

> 📌 **요구사항**
> 
> 제공된 샘플 영화 데이터(json 파일)에서 필요한 정보만 추출해 반환하는 함수 작성
> 
> 필요한 정보 : id, title, poster_path, vote_average, overview, genre_ids

- **결과 :**
  
  - 문제 접근 방법 및 코드 설명
    
    ✔ 함수 인자로 전달한 데이터를 담은 딕셔너리를 함수 내부에서 또 다른 딕셔너리에 담기
    
    ```python
    def movie_info(movie):
    
      result = {
          'id' : movie['id'], 
          'title' : movie['title'],
          'poster_path' : movie.get('poster_path'), 
          'vote_average' : movie.get('vote_average'),
          'overview' : movie.get('overview'),
          'genre_ids' : movie.get('genre_ids')
      }
    
      return result
    
    if __name__ == '__main__':
      movie_json = open('data/movie.json', encoding='utf-8')
      movie_dict = json.load(movie_json)
    
      pprint(movie_info(movie_dict))
    ```
  1. `if` 문
     
      data/movie.json 파일을 여는 변수 `movie_json` 생성
     
      이후 해당 파일의 데이터를 담는 딕셔너리 변수 `movie_dict` 생성
     
      이 때, `movie_dict` 는 `{ 'id' : 80, 'title' : '쇼생크 탈출', ...}` 형식
     
      함수 호출
  
  2. `movie_info(movie)` 함수 내부
     
      새로운 딕셔너리 `result` 생성, 인자로 받은 딕셔너리에서 값 추출
     
      `result` 반환

    - 이 문제에서 어려웠던 점
    
    파일을 열고 그 내부의 데이터를 활용해보는 첫 번째 문제였기 때문에, 교수님의 설명을 따라가기에 벅찼다. 

<aside>
💡 **내가 생각하는 이 문제의 포인트**

`file_json = open('file_name', encoding='utf-8')` → 파일(폴더) 열기
`container = json.load(file_json)` → 연 파일에서 데이터를 옮겨오기

</aside>

---

## B. 제공되는 영화 데이터의 주요내용 수정 (problem_b)

> 📌 **요구 사항**
> 
> 제공된 샘플 영화 데이터(json 파일)에서 필요한 정보만 추출 및 수정해 반환하는 함수 작성
> 
> 필요한 정보 : id, title, poster_path, vote_average, overview, genre_names

- **결과 :**
  
  - 문제 접근 방법 및 코드 설명
    
    ✔ 함수 인자로 받은 데이터 딕셔너리 값들을 각각 key, value로 갖는 새로운 딕셔너리 생성
    
    ```
    def movie_info(movie, genres):
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
    
    if __name__ == '__main__':
      movie_json = open('data/movie.json', encoding='utf-8')
      movie = json.load(movie_json)
    
      genres_json = open('data/genres.json', encoding='utf-8')
      genres_list = json.load(genres_json)
    
      pprint(movie_info(movie, genres_list))
    ```
  1. `if` 문
     
      data/movie.json 파일을 여는 변수 `movie_json` 생성
     
      이후 해당 파일의 데이터를 담는 딕셔너리 변수 `movie` 생성
     
      data/genres.json 파일을 여는 변수 `genres_json` 생성
     
      이후 해당 파일의 데이터를 담는 리스트 변수 `genres_list` 생성
     
      이 때, `genres_list` 은 `[{’id’ : 80, ‘name’ : ‘drama’}, … ]` 형식
     
      함수 호출
  
  2. `movie_info(movie, genres)` 함수
     
      장르 코드 = key, 장르 이름 = value를 갖는 딕셔너리 `genre_names` 생성
     
      `genres_list` 에서 불러온 데이터 원소 하나하나에서 key를 통해 값 추출
     
      출력 가독성을 위한 장르 이름 리스트 `movie_genre` 생성
     
      새로운 딕셔너리 `result` 생성, 인자로 받은 딕셔너리에서 값 추출
     
      `result` 반환

    - 이 문제에서 어려웠던 점
    
    `genre_names` 딕셔너리를 생성한다는 아이디어를 떠올리기까지에 시간이 오래 걸렸다.

<aside>
💡 **내가 생각하는 이 문제의 포인트**

딕셔너리로 받은 `movie` 값 접근 방식 → `movie.get('key')` 
리스트로 받은 `genres_list` 값 접근 방식 → `genres_list['idx']`

</aside>

---

## C. 다중 데이터 분석 및 수정 (problem_c)

> 📌 **요구 사항**
> 
> 20개의 항목이 들어간 데이터(json 파일)에서 필요한 정보 목록만 추출해 반환하는 함수 작성
> 
> 필요한 정보 : id, title, poster_path, vote_average, overview, genre_names
> 
> ⇒ 향후 커뮤니티 서비스에서 제공되는 영화 목록을 제공하기 위한 기능

- **결과 :**
  
  - 문제 접근 방법 및 코드 설명
    
    ✔ 수 많은 딕셔너리를 포함한 리스트 속 값들에 접근하기 위해 다양한 반복문 활용
    
    ```python
    def movie_info(movies, genres):
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
    
    if __name__ == '__main__':
      movies_json = open('data/movies.json', encoding='utf-8')
      movies_list = json.load(movies_json)
    
      genres_json = open('data/genres.json', encoding='utf-8')
      genres_list = json.load(genres_json)
    
      pprint(movie_info(movies_list, genres_list))
    ```
  1. `if` 문
     
      data/movies.json 파일을 여는 변수`movies_json` 생성
     
      이후 해당 파일의 데이터를 담는 리스트 변수`movies_list` 생성
     
      이 때, `movies_list` 은 `[{ 'id' : 8, 'title' : '쇼생크', ...}, { 'id' : ...}, ...]` 형식
     
      data/genres.json 파일을 여는 변수`genres_json` 생성
     
      이후 해당 파일의 데이터를 담는 리스트 변수`genres_list` 생성
     
      함수 호출
  
  2. `movie_info(movies, genres)` 함수
     
      장르 코드 = key, 장르 이름 = value를 갖는 딕셔너리 `genre_names` 생성
     
      `genres_list` 에서 불러온 데이터 원소 하나하나에서 key를 통해 값 추출
     
      각각 영화 세부 내용을 담을 딕셔너리를 담기 위한 리스트 `result` 생성 
     
      반복문으로 `movies_list` 에서 불러온 각각 영화 세부 내용 딕셔너리 하나하나 확인
     
      회차마다 장르 이름을 담을 리스트 `movie_genre` 형성, 갯수가 정해지지 않아 반복문 실행 
     
      새로운 딕셔너리 `result` 생성, 인자로 받은 딕셔너리에서 값 추출
     
      `result` 반환

    - 이 문제에서 어려웠던 점
    
    리스트 속 딕셔너리의 값에 접근해야하는데, 이 값의 갯수가 고정되어 있지 않아 
    반복문에서 iterable 변수를 찾아내는데 시간이 걸렸다.

<aside>
💡 **내가 생각하는 이 문제의 포인트**

`movies` 리스트 내부 `movie` 딕셔너리 각각 요소 접근 `for movie in movies: ...`
값 추출 → `movie.get('key')`

</aside>

---

## D. 알고리즘을 사용한 데이터 출력 (problem_d)

> 📌 **요구 사항**
> 
> 한 폴더에 들어있는 다양한 데이터(json 파일) 속 내용을 비교해 정렬하여 출력하는 함수 작성
> 
> 내용이 같은 데이터는 X

- **결과 :**
  
  - 문제 접근 방법 및 코드 설명
    
    ✔ 최댓값 value를 찾기 위해 최댓값 변수가 변동되면, 해당 key의 값을 저장
    
    ```python
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
    
    if __name__ == '__main__':
      movies_json = open('data/movies.json', encoding='utf-8')
      movies_list = json.load(movies_json)
    
      print(max_revenue(movies_list))
    ```
  1. `if` 문
     
      data/movies.json 파일을 여는 변수`movies_json` 생성
     
      이후 해당 파일의 데이터를 담는 리스트 변수`movies_list` 생성
     
      함수 호출
  
  2. `max_revenue(movies)` 함수
     
      가장 높은 수익 숫자, 이름을 담을 변수 `max_title`, `max_number` 생성
     
      반복문으로 `movies_list` 에서 불러온 각각 영화 세부 내용 딕셔너리 하나하나 확인
     
      이 때, `movies_list` 에서 사용하는 정보는 오직 `'id'`
     
      각각 `'id'` 를 받아 이를 사용해 data/movies/ 폴더 내부 id.json 파일에 접근
     
      해당 데이터들을 담는 `detail` 딕셔너리 생성 후 수익을 담는 `reve` 변수 생성
     
      최댓값을 찾으면 해당 key를 통해 값에 접근하여 최대 수익 이름을 `max_title` 변수에 담기
     
      `max_title` 반환

    - 이 문제에서 어려웠던 점
    
    data/movies/ 폴더 내부 id.json 파일에 접근하는 방법을 떠올리기가 가장 힘들었다.
    `movies_list` 에서 사용하는 것은 `id` 로, 이를 통해 f-string 방법을 사용하는 것도 어려웠다.

<aside>
💡 **내가 생각하는 이 문제의 포인트**

f-string 사용 → `movie_json = open(f'data/movies/{id}.json', encoding='utf-8')`

</aside>

---

## E. 알고리즘을 사용한 데이터 출력 (problem_e)

> 📌 **요구 사항**
> 
> 한 폴더에 들어있는 다양한 데이터(json 파일) 속 공통된 내용을 가진 데이터의 목록을 작성하여 출력하는 함수 작성
> 
> ⇒ 커뮤니티 서비스에서 추천 기능의 일부로 사용

- **결과 :**
  
  - 문제 접근 방법 및 코드 설명
    
    ✔ 딕셔너리 속 값을 새로운 리스트에 담아, 원소가 공통되는 것을 찾아 또 새로운 리스트에 담기
    
    ```python
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
    
    if __name__ == '__main__':
      movies_json = open('data/movies.json', encoding='utf-8')
      movies_list = json.load(movies_json)
    
      print(dec_movies(movies_list))
    ```
  1. `if` 문
     
      data/movies.json 파일을 여는 변수`movie_json` 생성
     
      이후 해당 파일의 데이터를 담는 리스트 변수`movie_list` 생성
     
      함수 호출
  
  2. `dec_movies(movies)` 함수
     
      12월에 상영한 영화 제목들을 담는 리스트 `december` 생성
     
      반복문으로 `movies_list` 에서 불러온 각각 영화 세부 내용 딕셔너리 하나하나 확인
     
      이 때, `movies_list` 에서 사용하는 정보는 오직 `'id'`
     
      각각 `'id'` 를 받아 이를 사용해 data/movies/ 폴더 내부 id.json 파일에 접근
     
      해당 데이터들을 담는 `detail` 딕셔너리 생성 후 상영 날짜를 담는 `date` 변수 생성
     
      string 형식인 `date` 에서 불필요한 문자 ‘-’ 제거 후 `date_list` 리스트에 담음
     
      수익을 담는 `reve` 변수 생성 후 수익이 0이 아닌, 즉, 상영이 이미 된 영화들 만을 다룸
     
      `date_list` 의 달을 나타내는 1번째 원소가 12일 때, 이를 `december` 리스트에 담음
     
      `december` 반환

    - 이 문제에서 어려웠던 점
    
    수 많은 영화 데이터 중에서 상영되지 않은 영화도 있었는데, 혹시나 해당 영화가 상영 예정일이 내가 찾는 정보와 수가 일치하게 된다면 오류를 일으킬 수 있다는 생각이 들었다.(현재 정보가 그렇지 않다고 하더라도)
    
    따라서 이를 제거하기 위해서 조건문을 추가해야 했다. 

<aside>
💡 **내가 생각하는 이 문제의 포인트**

string에서 불필요한 문자 제거 후 리스트화 → `list(string_name.split('Delimiter'))`

</aside>

---

# 후기

- 딕셔너리와 리스트, 그리고 리스트 속 딕셔너리와 딕셔너리 속 딕셔너리의 원소들에 접근하는 방법이 가장 헷갈렸고, 또 많이 틀렸었다. 하지만 이 연습문제들을 통해 감을 잡게 되었다.
- 로직을 짤 때마다 디버깅하고, print를 해보며 확인하는 습관을 들이게되어, 내가 어느 부분에서 실수를 하고 있는지 파악할 수 있게 되었다 (+오류 구글링 능력)
- 파일에 접근하는 방법, 그리고 폴더에 접근하는 방법을 여러번 반복 연습할 수 있었고, 데이터를 내가 생성한 컨테이너에 담아 처리하는 방법을 익힐 수 있었다.