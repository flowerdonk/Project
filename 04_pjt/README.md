# PJT 04 - Django

### 이번 PJT를 통해 배운 내용

- 데이터를 생성, 조회, 수정, 삭제할 수 있는 Web application 제작
- Django web framework를 사용한 데이터 처리
- Django Model과 ORM에 대한 이해
- Django ModelForm을 활용한 사용자 요청 데이터 유효성 검증
- Django Static files 관리 및 image file 업로드

---

### 📌 공통 요구사항

✅ 영화 데이터의 생성, 조회, 수정, 삭제가 가능한 애플리케이션을 완성

✅ Django 프로젝트의 이름은 `mypjt`, 앱 이름은 `movies`로 지정

1. Model
    
    `fields` : title, audience, release_date, genre, score, poster_url, description, actor_image
    
2. URL
    1. `/movies/` : 전체 영화 목록 페이지 조회
    2. `/movies/create/` : 새로운 영화 생성 페이지 조회 & 단일 영화 데이터 저장
    3. `/movies/<pk>/` : 단일 영화 상세 페이지 조회
    4. `/movies/<pk>/update/` : 기존 영화 수정 페이지 조회 & 단일 영화 데이터 수정
    5. `/movies/<pk>/delete/` : 단일 영화 데이터 삭제
3. View
    1. `index` : 전체 영화 데이터 조회 및 index.html 렌더링
    2. `create` : create.html 렌더링 유효성 검증 및 
    영화 데이터 저장 후 detail.html 리다이렉트
    3. `detail` : 단일 영화 데이터 조회 및 detail.html 렌더링
    4. `update` : 수정 대상 영화 데이터 조회 및 update.html 렌더링 유효성 검증 및 
    영화 데이터 수정 후 detail.html 리다이렉트
    5. `delete` : 단일 영화 데이터 삭제 및 index.html 리다이렉트
4. Form
    1. Movie 모델의 데이터 검증, 저장, 에러메시지, HTML을 관리 위해 ModelForm 사용
    2. genre 필드
        1. select element를 출력해 코미디, 공포, 로맨스 장르 데이터를 선택 가능
    3. score 필드
        1. input element의 type은 number로 설정
        2. input element attribute 중 step은 0.5, min은 0, max는 5로 설정
    4. release_date 필드
        1. input element의 type은 date로 설정

---

## A. 기본 설정

> 📌 **요구사항**
> 
> 1. `base.html` - “공통 부모 템플릿”
>     1. 모든 템플릿 파일은 base.html을 상속받아 사용
>     2. 주어진 header.jpg를 화면 상단에 배치
> 2. `mypjt/`
>     1. `movies/` 로 접근 시, 어플의 urls로 이동
> 3. `movies/models.py`
>     1. fields 설정
> 4. `movies/forms.py`
>     1. DB에 저장할 fields 세부 내용 설정

- **결과 :** `base.html`
    - 문제 접근 방법 및 코드 설명
    
    ✔ 모든 페이지에서 볼 수 있는 헤더, 페이지마다 달라지는 content
    
    ```html
    # templates/base.html
    
    {% load static %}
    
    <head>
    		...
      <title>Movies</title>
    </head>
    <body>
      <img src="{% static 'images/header.jpg' %}" alt="header">
    
      {% block content %}
      
      {% endblock content %}
    		...
    </body>
    ```
    
    1. header
        
        block 바깥으로 빼서 모든 페이지에서 볼 수 있게 함
        
    2. block
        
        상속 : 각각의 페이지에서 content에 보여질 부분을 block에 담음
        
    
- **결과 :** `mypjt/`
    - 문제 접근 방법 및 코드 설명
    
    ✔ 기본 URL 설정, 이미지 업로드 및 저장을 위한 기본 설정
    
    ```python
    # mypjt/urls.py
    
    from django.contrib import admin
    from django.urls import path, include
    from django.conf import settings
    from django.conf.urls.static import static
    
    urlpatterns = [
        path('admin/', admin.site.urls),
        path('movies/', include('movies.urls')),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    ```
    
    ```python
    # mypjt/settings.py
    
    INSTALLED_APPS = [
        'movies',
    			...
    ]
    
    TEMPLATES = [
        {
    	        ...
            'DIRS': [BASE_DIR / 'templates'],
    					...
        },
    ]
    
    STATIC_URL = '/static/'
    STATICFILES_DIRS = [ 
        BASE_DIR / 'static', 
    ]
    
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'
    ```
    
    1. static
        
        static 구조 : `static/images/`
        
        settings 경로 설정
        
    2. media
        
        media 구조 : `media/`
        
        settings 경로 설정 및 프로젝트 URL `static` 추가
        
- **결과 :** `movies/models.py`
    - 문제 접근 방법 및 코드 설명
    
    ✔ fields 데이터 유형 및 역할 확인
    
    ```python
    # movies/models.py
    
    from django.db import models
    
    class Movie(models.Model):
        title = models.CharField(max_length=20)
        audience = models.IntegerField()
        release_date = models.DateField(auto_now_add=False)
        genre = models.CharField(max_length=30)
        score = models.FloatField()
        poster_url = models.CharField(max_length=50)
        description = models.TextField()
        actor_image = models.ImageField()
    ```
    
    1. fields
        
        각 필드당 입력받는 타입을 생각해서 유형 및 길이 지정
        
- **결과 :** `movies/forms.py`
    - 문제 접근 방법 및 코드 설명
    
    ✔ 각 필드 세부 내용 제어
    
    ```python
    # movies/forms.py
    
    from django import forms
    from .models import Movie
    
    class MovieForm(forms.ModelForm):
        genre = forms.ChoiceField(
            choices=[('선택', 'None'), ('Comedy', 'Comedy'), ('Thriller', 'Thriller'), ('Romance', 'Romance')], 
        )
    
        score = forms.FloatField(
            min_value= 0,
            max_value= 5,
            widget= forms.NumberInput(
                attrs={
                    'step' : 0.5,
                }
            )
        )
        release_date = forms.DateField(
            widget= forms.DateInput(
                attrs={
                    'type':'date',
                }
            ),
        )
        class Meta:
            model = Movie
            fields = '__all__'
    ```
    
    1. fields
        
        genre의 경우 선택지 제공 → 리스트 활용
        
        attribute로 단위 상세 설정
        

<aside>
💡 **내가 생각하는 이 문제의 포인트**

각각의 페이지에서 노출할 요소를 분류 및 선택하기 → DTL : `block` 사용

</aside>

---

## B. INDEX

> 📌 **요구 사항**
> 
> 
> “전체 영화 목록 조회 페이지”
> 
> 1. 데이터베이스에 존재하는 모든 영화의 목록 표시
> 2. 적절한 HTML 요소를 사용하여 영화 제목 및 평점 표시,
> 제목 클릭 시 해당 영화의 상세 조회 페이지(detail.html)로 이동

- **결과 :**
    - 문제 접근 방법 및 코드 설명
    
    ✔ DB에 저장된 모든 정보 전달 및 출력
    
    ```python
    # movies/urls.py
    
    from django.urls import path
    from . import views
    
    app_name = 'movies'
    urlpatterns = [
        path('', views.index, name='index'),
    			...
    ]
    ```
    
    ```python
    # movies/views.py
    
    from django.shortcuts import render
    from django.views.decorators.http import require_safe
    from .models import Movie
    
    @require_safe
    def index(request):
        movies = Movie.objects.all()
        context = {
            'movies' : movies
        }
        return render(request, 'movies/index.html', context)
    ```
    
    ```html
    # movies/index.html
    
    {% extends 'base.html' %}
    
    {% block content %}
      <h1>INDEX</h1><br>
      <a href="{% url 'movies:create' %}">CREATE</a>
      <hr>
    
      {% for movie in movies %}
        <a href="{% url 'movies:detail' movie.pk%}">{{movie.title}}</a>
        <p>{{movie.score}}</p>
        <hr>
      {% endfor %}
    
    {% endblock content %}
    ```
    
    1. `views.py`
        
        `Movie.objects.all()` : Movie 객체들 모두 불러와 `movies`에 저장 → 전달
        
    2. `movies/index.html`
        
        DTL `for` : 전달받은 `movies` 에서 객체 하나하나 출력 (비어있을 시 반복 X)
        
    
    - 이 문제에서 어려웠던 점
        
        전달한 딕셔너리 ‘키’값 정확히 파악 및 DTL에 활용
        

<aside>
💡 **내가 생각하는 이 문제의 포인트**

DB에 저장된 객체 목록들 전달 → 활용 구조 파악

</aside>

---

## C. DETAIL

> 📌 **요구 사항**
> 
> 
> “영화 상세 정보 페이지”
> 
> 1. 특정 영화 상세 정보 표시
> 2. 해당 영화 수정 및 삭제 버튼 표시
> 3. 전체 영화 목록 조회 페이지(index.html)로 이동하는 링크 표시

- **결과 :**
    - 문제 접근 방법 및 코드 설명
    
    ✔ pk값으로 접근, 정보 전달
    
    ```python
    # movies/urls.py
    
    from django.urls import path
    from . import views
    
    app_name = 'movies'
    urlpatterns = [
    			...
        path('<int:pk>/', views.detail, name='detail'),
    			...
    ]
    ```
    
    ```python
    # movies/views.py
    
    from django.shortcuts import render
    from django.views.decorators.http import require_safe
    from .models import Movie
    
    @require_safe
    def detail(request, pk):
        movie = Movie.objects.get(pk=pk)
        context = {
            'movie' : movie,
        }
        return render(request, 'movies/detail.html', context)
    ```
    
    ```html
    # movies/detail.html
    
    {% extends 'base.html' %}
    
    {% block content %}
      <h1>DETAIL</h1>
      <hr>
      <h1>{{movie.title}}</h1><br>
      <p>Audience : {{movie.audience}}</p>
      <p>Release Dates : {{movie.release_date}}</p>
      <p>Genre : {{movie.genre}}</p>
      <p>Score : {{movie.score}}</p>
      <p>Poster : {{movie.poster_url}}</p>
      <p>Actor : </p>
      <img src="{{movie.actor_image.url}}" alt="{{article.actor_image}}">
      <p>{{movie.description}}</p>
    
      <a href="{% url 'movies:update' movie.pk %}">UPDATE</a>
      <form action="{% url 'movies:delete' movie.pk %}" method="POST">
        {% csrf_token %}
        <input type="submit" value="DELETE">
      </form>
      <a href="{% url 'movies:index' %}">BACK</a>
    {% endblock content %}
    ```
    
    1. `views.py`
        
        `Movie.objects.get(pk=pk)` : url에서 전달받은 특정 pk의 객체 불러오기
        
    2. `detail.html`
        
        해당 pk 객체의 fields 정보들 출력
        
        `<img>` : `MEDIA_ROOT` 에 저장된 입력받은 이미지 출력
        src = 업로드 파일의 경로, alt = 업로드 파일의 파일 이름
        
        `update` : a 태그 → pk값만 가지고 이동하면 되기 때문
        
        `delete` : form 태그 → 데이터를 조작해야하기 때문
        
    
    - 이 문제에서 어려웠던 점
        
        입력받은 이미지를 `media` 에 저장하고, 이를 보여주는 것
        
        `a` 태그와 `form` 태그에 적절한 활용
        

<aside>
💡 **내가 생각하는 이 문제의 포인트**

Media Files 적용 및 활용

</aside>

---

## D. CREATE

> 📌 **요구 사항**
> 
> 
> “영화 생성 페이지”
> 
> 1. 특정 영화를 생성하기 위한 HTML form 요소 표시
> 2. 표시되는 form은 Movie 모델 클래스에 기반한 ModelForm
> 3. 작성한 정보는 제출(submit)시 단일 영화 데이터를 저장하는 URL로 요청과 함께 전송
> 4. 전체 영화 목록 조회 페이지(index.html)로 이동하는 링크(back) 표시
> 5. actor_image에 해당하는 이미지는 직접 업로드 가능

- **결과 :**
    - 문제 접근 방법 및 코드 설명
    
    ✔ form 형성 구조 파악
    
    ```python
    # movies/urls.py
    
    from django.urls import path
    from . import views
    
    app_name = 'movies'
    urlpatterns = [
    			...
        path('create/', views.create, name='create'),
    			...
    ]
    ```
    
    ```python
    # movies/views.py
    
    from django.shortcuts import render, redirect
    from django.views.decorators.http import require_http_methods
    from .forms import MovieForm
    
    @require_http_methods(['GET', 'POST'])
    def create(request):
        if request.method == 'POST':
            form = MovieForm(request.POST, request.FILES)
            if form.is_valid():
                movie = form.save()
                return redirect('movies:detail', movie.pk)
        else:
            form = MovieForm()
    
        context = {
            'form' : form,
        }
        return render(request, 'movies/create.html', context)
    ```
    
    ```html
    # movies/create.html
    
    {% extends 'base.html' %}
    
    {% block content %}
      <h1>CREATE</h1>
      <hr>
      <form action="{% url 'movies:create' %}" method="POST" enctype="multipart/form-data">
        {% csrf_token %}
        {{form.as_p}}
        <input type="submit" value="Submit">
      </form>
      <hr>
      <a href="{% url 'movies:index' %}">BACK</a>
    {% endblock content %}
    ```
    
    1. `views.py`
        
        메소드가 `POST` 일 때와 `GET` 일 때를 구별
        
        `GET` : 처음 버튼을 눌렀을 때, 빈 폼을 가지고 `create.html` 로 이동
        
        `POST` : 빈 폼에 정보를 입력했을 때 이를 폼에 저장, `detail.html` 로 이동
        
    2. `create.html`
        
        `{{form.as_p}}` : Django form 활용
        
    
    - 이 문제에서 어려웠던 점
        
        이미지를 입력받기 때문에 `request.FILES` , `enctype` 확인 필수
        

<aside>
💡 **내가 생각하는 이 문제의 포인트**

메소드 `POST` , `GET` 구별 및 각각의 로직 설정

</aside>

---

## E. UPDATE

> 📌 **요구 사항**
> 
> 
> “영화 수정 페이지”
> 
> 1. 특정 영화를 수정하기 위한 HTML form 요소 표시
> 2. 표시되는 form은 Movie 모델 클래스에 기반한 ModelForm
> 3. HTML input 요소에는 기존 데이터 출력
> 4. Reset 버튼은 사용자의 모든 입력을 초기 값으로 재설정
> 5. 작성한 정보는 제출(submit)시 단일 영화 데이터를 수정하는 URL로 요청과 함께 전송
> 6. 영화 상세 정보 페이지(detail.html)로 이동하는 링크(back) 표시

- **결과 :**
    - 문제 접근 방법 및 코드 설명
    
    ✔ 수정할 데이터를 전달하고, 전달받아 갱신
    
    ```python
    # movies/urls.py
    
    from django.urls import path
    from . import views
    
    app_name = 'movies'
    urlpatterns = [
    			...
        path('<int:pk>/update/', views.update, name='update'),
    			...
    ]
    ```
    
    ```python
    # movies/views.py
    
    from django.shortcuts import render, redirect
    from django.views.decorators.http import require_http_methods
    from .models import Movie
    from .forms import MovieForm
    
    @require_http_methods(['GET', 'POST'])
    def update(request, pk):
        movie = Movie.objects.get(pk=pk)
        if request.method == 'POST':
            form = MovieForm(request.POST, request.FILES, instance=movie)
            if form.is_valid():
                form.save()
                return redirect('movies:detail', movie.pk)
        else:
            form = MovieForm(instance=movie)
        context = {
            'form' : form, 
            'movie' : movie,
        }
        return render(request, 'movies/update.html', context)
    ```
    
    ```html
    # movies/update.html
    
    {% extends 'base.html' %}
    
    {% block content %}
      <h1>UPDATE</h1>
      <hr>
      <form action="{% url 'movies:update' movie.pk %}" method="POST" enctype="multipart/form-data">
        {% csrf_token %}
        {{form.as_p}}
        <input type="reset" value="Reset">
        <input type="submit" value="Submit">
      </form>
      <hr>
      <a href="{% url 'movies:index' %}">BACK</a>
    {% endblock content %}
    ```
    
    1. `views.py`
        
        `GET` : 수정할 객체를 form에 불러오고 다시 전달
        
        `POST` : 전달받은 수정할 form을 입력받은 값으로 갱신(해당 instance 그대로)
        
    2. `update.html`
        
        `reset` : 수정을 확정하기 전에 해당 객체 다시 불러오기
        
    
    - 이 문제에서 어려웠던 점
        
        수정할 instance를 전달하고(`GET`) 이를 수정하고 다시 전달(`POST`)하는 과정
        

<aside>
💡 **내가 생각하는 이 문제의 포인트**

수정할 form을 instance로 전달하고, 전달받아 갱신하는 과정

</aside>

---

## F. DELETE

> 📌 **요구 사항**
> 
> 
> 데이터 삭제
> 
> 1. `detail.html` 에서 데이터 삭제 가능

- **결과 :**
    - 문제 접근 방법 및 코드 설명
    
    ✔ `html` 따로 생성 없이 `detail.html`에서 진행되도록 구현
    
    ```python
    # movies/urls.py
    
    from django.urls import path
    from . import views
    
    app_name = 'movies'
    urlpatterns = [
    			...
    		path('<int:pk>/delete/', views.delete, name='delete'),
    			...
    ]
    ```
    
    ```python
    # movies/views.py
    
    from django.shortcuts import redirect
    from django.views.decorators.http import require_POST
    from .models import Movie
    
    @require_POST
    def delete(request, pk):
        movie = Movie.objects.get(pk=pk)
        movie.delete()
        return redirect('movies:index')
    ```
    
    1. `views.py`
        
        삭제할 데이터의 pk 값을 받아 이를 삭제
        
        삭제 후 `index.html` 로 이동
        

<aside>
💡 **내가 생각하는 이 문제의 포인트**

데이터 삭제 메소드 활용 및 후처리

</aside>

---

# 후기

- 특정 데이터에 접근하고, 해당 데이터를 딕셔너리에 저장해 전달하고, 전달 받은 데이터를 처리하는 일련의 과정을 훈련할 수 있었다.
- 데이터를 전달하거나 데이터에 접근할 때 사용해야하는 문법에 익숙해질 수 있었다.
- DB에 데이터를 저장하고 삭제하기까지를 눈으로 확인할 수 있어서 이해가 쉬웠다.