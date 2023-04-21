# PJT 07 - DB 설계를 활용한 REST API 설계

### 이번 PJT를 통해 배운 내용

- DRF(Django Rest Framework)를 활용한 API Server 제작
- Database many to one relationship(1:N)에 대한 이해
- Database many to many relationship(M:N)에 대한 이해

---

## A. Model, Serializer

> **📌 ERD (Entity-Relationship Diagram)**
> 
> 
> ![Untitled](PJT%2007%20-%20DB%20%E1%84%89%E1%85%A5%E1%86%AF%E1%84%80%E1%85%A8%E1%84%85%E1%85%B3%E1%86%AF%20%E1%84%92%E1%85%AA%E1%86%AF%E1%84%8B%E1%85%AD%E1%86%BC%E1%84%92%E1%85%A1%E1%86%AB%20REST%20API%20%E1%84%89%E1%85%A5%E1%86%AF%E1%84%80%E1%85%A8%200120fcfe719043018c503f871f03ae16/Untitled.png)
> 

- **결과 :**
    - 문제 접근 방법 및 코드 설명
    
    **✔ N:1 관계, M:N 관계 설정 및 필드 선택 직렬화**
    
    ### 1. Model
    
    ```python
    # movies/models.py
    
    from django.db import models
    
    class Actor(models.Model):
        name = models.CharField(max_length=100, null=True)
    
    class Movie(models.Model):
        actors = models.ManyToManyField(Actor)
        title = models.CharField(max_length=100)
        overview = models.TextField()
        release_date = models.DateTimeField()
        poster_path = models.TextField()
    
    class Review(models.Model):
        movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
        title = models.CharField(max_length=100)
        content = models.TextField()
    ```
    
    1. M:N
        - Actor와 Movie는 M:N 관계로 `ManyToManyField` 를 활용해 중개테이블 형성
            - 이후 단일 배우 조회, 단일 영화 조회 시 역참조, 참조를 통해 상대 데이터들을 불러옴
    2. N:1
        - Review는 Movie와 N:1 관계로 `ForeignKey`를 통해 무비 객체를 불러옴
    
    ### 2. Serializer
    
    ```python
    # movies/serializers.py
    
    from rest_framework import serializers
    from .models import Movie, Review, Actor
    
    class MovieSerializer(serializers.ModelSerializer):
        actors = serializers.SerializerMethodField()
        reviews = serializers.SerializerMethodField()
    
        class Meta:
            model = Movie
            fields = '__all__'
    
        def get_actors(self, movie):
            actors = movie.actors.all()
            return [{'name': actor.name} for actor in actors]
    
        def get_reviews(self, movie):
            reviews = movie.review_set.all()
            return [{'title': review.title, 'content':review.content} for review in reviews]
    ```
    
    1. `SerializerMethodField()`
        - Movie 모델에 없는 Review 모델의 내용을 담은 필드와, actors 필드의 내용 중 일부분만 가져오기 위해 사용
    2. `get_actors(self, movie)` 함수
        - Movie에 있는 ManyToMany 필드인 actor에서, 해당 actor를 정참조해 이름만을 불러와 리턴
    3. `get_reviews(self, movie)` 함수
        - 역참조를 통해 해당 영화의 댓글들을 전부 불러와서, 이름과 내용만을 리턴
    
    ```python
    class ActorSerializer(serializers.ModelSerializer):
        movies = serializers.SerializerMethodField()
    
        class Meta:
            model = Actor
            fields = '__all__'
        
        def get_movies(self, actor):
            movies = actor.movie_set.all()
            return [{'title': movie.title} for movie in movies]
    ```
    
    1. `SerializerMethodField()`
        - Actor 모델에 없는 Movie 모델의 내용을 담은 필드를 가져오기 위해 사용
    2. `get_movies(self, actor)`
        - Movie와의 ManyToMany 필드에서, 해당 배우의 영화들을 역참조해 제목만을 불러와 리턴
    
    ```python
    class ReviewSerializer(serializers.ModelSerializer):
    
        class Meta:
            model = Review
            fields = '__all__'
            read_only_fields = ('movie', )
    ```
    
    1. `read_only_fields`
        - 리뷰를 작성할 때 유저가 작성하는 것은 제목, 내용 뿐이므로 `movie` 는 읽기 전용 필드로 설정해 에러를 방지
    
    - 이 문제에서 어려웠던 점
        1. 불러들이는 데이터의 필드를 확인해 적절한 필드 형성
        2. 각각의 모델들에 없는 필드를 불러오기 위해 `SerializerMethodField()` 사용 후 함수로 내용 지정

<aside>
💡 **내가 생각하는 이 문제의 포인트**

1. `SerializerMethodField()` + 함수 정의를 통한 데이터 불러오기
</aside>

---

## B. 전체 배우 목록 제공

> 📌 **요구 사항**
> 
> - `api/v1/actors/` 접근 시, 전체 배우 목록 조회
> - 보여지는 필드는 `id`, `name`

- **결과 :**
    - 문제 접근 방법 및 코드 설명
    
    **✔ view함수에서 전달되는 데이터 필드 수정**
    
    ```python
    # movies/urls.py
    
    from django.contrib import admin
    from django.urls import path
    from . import views
    
    urlpatterns = [
        path('actors/', views.actor_list),
    	    ...
    ]
    ```
    
    1. 경로 설정
        - 'actors/'로 접근 시 `actor_list` 함수로 이동
    
    ```python
    # movies/views.py
    
    from django.shortcuts import get_list_or_404
    from rest_framework.decorators import api_view
    from rest_framework.response import Response
    
    from .serializers import ActorSerializer
    from .models import Actor
    
    @api_view(['GET'])
    def actor_list(request):
        if request.method == 'GET':
            actors = get_list_or_404(Actor)
            serializer = ActorSerializer(actors, many=True)
            data = serializer.data
            [item.pop('movies') for item in data]
            return Response(data)
    ```
    
    1. `serializer = ActorSerializer(actors, many=True)`
        - Actor에 있는 모든 데이터를 넣은 `actors` 를 직렬화
    2. `data = serializer.data`
        - 직렬화한 데이터를 변수에 대입 후 로직 처리(pop)
    
    - 이 문제에서 어려웠던 점
        1. 불러들인 데이터에서 내보내고 싶은 내용만 후가공하는 것

<aside>
💡 **내가 생각하는 이 문제의 포인트**

1. view 함수에서 로직 처리
</aside>

---

## C. 단일 배우 정보 제공

> 📌 **요구 사항**
> 
> - `api/v1/actors/1/` 접근 시, 단일 배우 정보 조회
> - 보여지는 필드는 `id`, `movies`, `name`

- **결과 :**
    - 문제 접근 방법 및 코드 설명
    
    **✔ 직렬화**
    
    ```python
    # movies/urls.py
    
    from django.contrib import admin
    from django.urls import path
    from . import views
    
    urlpatterns = [
    			...
        path('actors/<int:actor_pk>/', views.actor_detail),
    			...
    ]
    ```
    
    1. 경로 설정
        - 'actors/<int:actor_pk>/'로 접근 시, `actor_detail` 함수로 이동
    
    ```python
    # movies/views.py
    
    from django.shortcuts import get_object_or_404
    from rest_framework.decorators import api_view
    from rest_framework.response import Response
    
    from .serializers import ActorSerializer
    from .models import Actor
    
    @api_view(['GET'])
    def actor_detail(request, actor_pk):
        if request.method == 'GET':
            actor = get_object_or_404(Actor, pk=actor_pk)
            serializer = ActorSerializer(actor)
            return Response(serializer.data)
    ```
    
    1. `actor = get_object_or_404(Actor, pk=actor_pk)`
        - actor_pk를 가진 Actor 데이터를 불러옴
    2. `serializer = ActorSerializer(actor)`
        - 직렬화 후 전달

<aside>
💡 **내가 생각하는 이 문제의 포인트**

1. pk를 통해 특정 데이터 불러온 후 직렬화
</aside>

---

## D. 전체 영화 목록 제공

> 📌 **요구 사항**
> 
> - `api/v1/movies/` 접근 시, 전체 영화 목록 조회
> - 보여지는 필드는 `title`, `overview`

- **결과 :**
    - 문제 접근 방법 및 코드 설명
    
    ✔  **view함수에서 전달되는 데이터 필드 수정**
    
    ```python
    # movies/urls.py
    
    from django.contrib import admin
    from django.urls import path
    from . import views
    
    urlpatterns = [
    			...
        path('movies/', views.movie_list),
    			...
    ]
    ```
    
    1. 경로 설정
        - 'movies/'로 접근 시, `movie_list` 함수로 이동
    
    ```python
    # movies/views.py
    
    from django.shortcuts import render
    from django.shortcuts import get_list_or_404
    from rest_framework.decorators import api_view
    from rest_framework.response import Response
    
    from .serializers import MovieSerializer
    from .models import Movie
    
    @api_view(['GET'])
    def movie_list(request):
        if request.method == 'GET':
            movies = get_list_or_404(Movie)
            serializer = MovieSerializer(movies, many=True)
            data = serializer.data
            [item.pop('id') for item in data]
            [item.pop('release_date') for item in data]
            [item.pop('poster_path') for item in data]
            [item.pop('actors') for item in data]
            return Response(data)
    ```
    
    1. `data = serializer.data`
        - 직렬화 된 데이터 대입
    2. 특정 키 삭제
        
        `[item.pop('key') for item in data]`
        
    
    - 이 문제에서 어려웠던 점
        1. 직렬화 된 데이터를 따로 저장해 해당 로직에서만 전달할 내용을 수정하는 것

<aside>
💡 **내가 생각하는 이 문제의 포인트**

1. `data = serializer.data` 를 통해 데이터 가공을 가능하게 함(해당 로직에서만)
</aside>

---

## E. 단일 영화 정보 제공

> 📌 **요구 사항**
> 
> - `api/v1/movies/1/` 접근 시, 단일 영화 정보 조회
> - 보여지는 필드는 `id`, `actors`, `review_set`, `title`, `overview`, `release_date`, `poster_path`

- **결과 :**
    - 문제 접근 방법 및 코드 설명
    
    ✔ **직렬화**
    
    ```python
    # movies/urls.py
    
    from django.contrib import admin
    from django.urls import path
    from . import views
    
    urlpatterns = [
    	    ...
        path('movies/<int:movie_pk>/', views.movie_detail),
    	    ...
    ]
    ```
    
    1. 경로 설정
        - 'movies/<int:movie_pk>/'로 접근 시, `movie_detail` 함수로 이동
    
    ```python
    # movies/views.py
    
    from django.shortcuts import get_object_or_404
    from rest_framework.decorators import api_view
    from rest_framework.response import Response
    
    from .serializers import MovieSerializer
    from .models import Movie
    
    @api_view(['GET'])
    def movie_detail(request, movie_pk):
        if request.method == 'GET':
            movie = get_object_or_404(Movie, pk=movie_pk)
            serializer = MovieSerializer(movie)
            return Response(serializer.data)
    ```
    
    1. `movie = get_object_or_404(Movie, pk=movie_pk)`
        - movie_pk를 가진 Movie데이터를 불러옴
    2. `serializer = MovieSerializer(movie)`
        - 직렬화 후 전달

<aside>
💡 **내가 생각하는 이 문제의 포인트**

1. pk를 통해 특정 데이터 불러온 후 직렬화
</aside>

---

## F. 전체 리뷰 목록 제공

> 📌 **요구 사항**
> 
> - `api/v1/reviews/` 접근 시, 전체 리뷰 목록 조회
> - 보여지는 필드는 `title`, `content`

- **결과 :**
    - 문제 접근 방법 및 코드 설명
    
    ✔  **view함수에서 전달되는 데이터 필드 수정**
    
    ```python
    # movies/urls.py
    
    from django.contrib import admin
    from django.urls import path
    from . import views
    
    urlpatterns = [
    	    ...
        path('reviews/', views.review_list),
    	    ...
    ]
    ```
    
    1. 경로 설정
        - 'reviews/'로 접근 시, `review_list` 함수로 이동
    
    ```python
    # movies/views.py
    
    from django.shortcuts import get_list_or_40
    from rest_framework.decorators import api_view
    from rest_framework.response import Response
    
    from .serializers import ReviewSerializer
    from .models import Review
    
    @api_view(['GET'])
    def review_list(request):
        if request.method == 'GET':
            reviews = get_list_or_404(Review)
            serializer = ReviewSerializer(reviews, many=True)
            data = serializer.data
            [item.pop('id') for item in data]
            [item.pop('movie') for item in data]
            return Response(data)
    ```
    
    1. `data = serializer.data`
        - 직렬화 된 데이터 대입
    2. 특정 키 삭제
        
        `[item.pop('key') for item in data]`
        
    
    - 이 문제에서 어려웠던 점
        1. 직렬화 된 데이터를 따로 저장해 해당 로직에서만 전달할 내용을 수정하는 것

<aside>
💡 **내가 생각하는 이 문제의 포인트**

1. `data = serializer.data` 를 통해 데이터 가공을 가능하게 함(해당 로직에서만)
</aside>

---

## G. 단일 리뷰 조회 & 수정 & 삭제

> 📌 **요구 사항**
> 
> - `api/v1/reviews/1/` 접근 시, 단일 리뷰 조회, 수정, 삭제 가능
> - 보여지는 필드는 `id`, `movie`, `title`, `content`

- **결과 :**
    - 문제 접근 방법 및 코드 설명
    
    ✔  **view함수에서 전달되는 데이터 필드 수정**
    
    ```python
    # movies/urls.py
    
    from django.contrib import admin
    from django.urls import path
    from . import views
    
    urlpatterns = [
    	    ...
        path('reviews/<int:review_pk>/', views.review_detail),
    	    ...
    ]
    ```
    
    1. 경로 설정
        - 'reviews/<int:review_pk>/'로 접근 시, `review_detail` 함수로 이동
    
    ### 1. READ
    
    ```python
    # movies/views.py
    
    from django.shortcuts import get_object_or_404
    from rest_framework.decorators import api_view
    from rest_framework.response import Response
    from rest_framework import status
    
    from .serializers import ReviewSerializer
    from .models import Movie, Review
    
    @api_view(['GET','PUT','DELETE'])
    def review_detail(request, review_pk):
        review = get_object_or_404(Review, pk=review_pk)
        if request.method == 'GET':
            serializer = ReviewSerializer(review)
    	    ...
        data = serializer.data
        movie_pk = data["movie"]
        movie_title = Movie.objects.get(pk=movie_pk).title
        data["movie"] = {"title" : movie_title}
        return Response(data)
    ```
    
    1. `serializer = ReviewSerializer(review)`
        - 해당 리뷰 정보 직렬화
    2. 외래키 필드의 pk 값을 통해 다른 모델의 내용 일부 가져오기
        - `movie_pk = data["movie"]` : 외래키 필드인 `movie` 에 담겨있는 pk값을 변수에 대입
        - `movie_title = Movie.objects.get(pk=movie_pk).title` : 해당 pk를 통해 `Movie` 객체의 제목 불러오기
        - `data["movie"] = {"title" : movie_title}` : `movie` 키에 딕셔너리 대입
    
    ### 2. UPDATE
    
    ```python
    # movies/views.py
    
    from django.shortcuts import get_object_or_404
    from rest_framework.decorators import api_view
    from rest_framework.response import Response
    from rest_framework import status
    
    from .serializers import ReviewSerializer
    from .models import Movie, Review
    
    @api_view(['GET','PUT','DELETE'])
    def review_detail(request, review_pk):
        review = get_object_or_404(Review, pk=review_pk)
    	    ...
        elif request.method == 'PUT':
            serializer = ReviewSerializer(review, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
    	    ...
        data = serializer.data
        movie_pk = data["movie"]
        movie_title = Movie.objects.get(pk=movie_pk).title
        data["movie"] = {"title" : movie_title}
        return Response(data)
    ```
    
    1. `serializer = ReviewSerializer(review, data=request.data)`
        - review를 입력한 데이터로 수정 및 직렬화
    2. `serializer.is_valid(raise_exception=True)`
        - 유효성 검사 오류 시 ValidationError 예외를 발생시키기
    
    ### 3. DELETE
    
    ```python
    # movies/views.py
    
    from django.shortcuts import get_object_or_404
    from rest_framework.decorators import api_view
    from rest_framework.response import Response
    from rest_framework import status
    
    from .models import Movie, Review
    
    @api_view(['GET','PUT','DELETE'])
    def review_detail(request, review_pk):
        review = get_object_or_404(Review, pk=review_pk)
    	    ...
        elif request.method == 'DELETE':
            review.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    	    ...
    ```
    
    1. 리뷰 삭제
        - 삭제 후 `HTTP_204_NO_CONTENT` 상태 코드 반환
    
    - 이 문제에서 어려웠던 점
        1. 외래 키 필드에 값으로 들어있는 pk 값으로 `Movie`의 특정 객체에 접근하고, 해당 객체에서 원하는 정보를 가져와 다시 직렬화 데이터에 담는 과정

<aside>
💡 **내가 생각하는 이 문제의 포인트**

1. 외래 키 필드 값을 활용한 타 모델 객체 접근
2. view 함수에서 데이터 가공(해당 로직에서만)
</aside>

---

## H. 리뷰 생성

> 📌 **요구 사항**
> 
> - `api/v1/movies/1/reviews/` 접근 시, 리뷰 생성 가능
> - 보여지는 필드는 `id`, `movie`, `title`, `content`

- **결과 :**
    - 문제 접근 방법 및 코드 설명
    
    ✔ 데이터 입력 후 직렬화 된 내용 저장 
    
    ```python
    # movies/urls.py
    
    from django.contrib import admin
    from django.urls import path
    from . import views
    
    urlpatterns = [
    	    ...
        path('movies/<int:movie_pk>/reviews/', views.create_review),
    ]
    ```
    
    1. 경로 설정
        - 'movies/<int:movie_pk>/reviews/'로 접근 시, `create_review` 함수로 이동
    
    ```python
    # movies/views.py
    
    from django.shortcuts import get_object_or_404
    from rest_framework.decorators import api_view
    from rest_framework.response import Response
    from rest_framework import status
    
    from .serializers import ReviewSerializer
    from .models import Movie
    
    @api_view(['POST'])
    def create_review(request, movie_pk):
        movie = get_object_or_404(Movie, pk=movie_pk)
        if request.method == 'POST':
            serializer = ReviewSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(movie=movie)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
    ```
    
    1. `serializer = ReviewSerializer(data=request.data)`
        - 입력된 데이터 직렬화
    2. `serializer.is_valid(raise_exception=True)`
        - 유효성 검사 후 저장
        - 이후 `HTTP_201_CREATED` 상태 코드 반환

<aside>
💡 **내가 생각하는 이 문제의 포인트**

1. 입력된 데이터로 직렬화 생성 및 저장
</aside>

---

# 후기

- Driver와 Navigator로 역할을 나눈 페어 프로그래밍의 첫 시작이었는데, 코드 한 줄 한 줄을 같이 구성하고 구현해낸다는 느낌이 가장 크게 들었던 페어 프로젝트였다.
- 특히 혼자 구현할 때와 가장 큰 차이점이라 느껴졌던 점은 코드 구성을 하다 문제가 생기면, 해당 문제에 대한 현상 파악이 오직 나 자신의 머릿속에만 추상적으로 남아있었는데, 페어로 프로젝트를 진행하다 문제가 생기게되면 상대방에게 이를 구체적이며 직관적으로 설명해야 했다는 점이었다.
- 문제에 대해 서로 소통하며, 이를 말로 구체화하면서 현상에 대한 정확한 파악이 이루어지고, 이로 인해 해결책을 찾는 것이 더 쉽고 빨라질 수 있었던 것 같다.