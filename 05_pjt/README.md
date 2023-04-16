# PJT 05 - 사용자 인증 기반 DB 설계

### 이번 PJT를 통해 배운 내용

- 데이터를 생성, 조회, 수정, 삭제할 수 있는 Web application 제작
- Django web framework를 사용한 데이터 처리
- Django Model과 ORM에 대한 이해
- Django Authentication System에 대한 이해

---

## 📌 공통 **요구사항**

✅ 커뮤니티 웹 서비스의 데이터 구성 단계

✅ 영화 데이터의 생성, 조회, 수정, 삭제가 가능한 애플리케이션을 완성

✅ 로그인, 로그아웃, 회원가입, 회원탈퇴, 회원정보수정, 비밀번호변경이 가능한 애플리케이션 완성

✅ Django 프로젝트의 이름은 mypjt, 앱 이름은 movies와 accounts로 지정

1. Model
    1. Movie
        
        `fields` : title, description
        
    2. User
        
        AbstractUser 모델 클래스를 상속받는 커스텀 모델 사용
        
2. URL
    1. movies
        1. `/movies/` : 전체 영화 목록 페이지 조회
        2. `/movies/create/` : 새로운 영화 생성 페이지 조회 & 단일 영화 데이터 저장
        3. `/movies/<pk>/` : 단일 영화 상세 페이지 조회
        4. `/movies/<pk>/update/` : 기존 영화 수정 페이지 조회 & 단일 영화 데이터 수정
        5. `/movies/<pk>/delete/` : 단일 영화 데이터 삭제
    2. accounts
        1. `/accounts/login/` : 로그인 페이지 조회 & 세션 데이터 생성 및 저장 (로그인) 
        2. `/accounts/logout/` : 세션 데이터 삭제 (로그아웃)
        3. `/accounts/signup/` : 회원 생성 페이지 조회 & 단일 회원 데이터 생성 (회원가입)
        4. `/accounts/delete/` : 단일 회원 데이터 삭제 (회원탈퇴)
        5. `/accounts/update/` : 회원 수정 페이지 조회 & 단일 회원 데이터 수정 (회원정보수정)
        6. `/accounts/password/` : 비밀번호 수정 페이지 조회 & 단일 비밀번호 데이터 수정
        (비밀번호변경)
3. View
    1. movies
        1. `index` : 전체 영화 데이터 조회 및 index.html 렌더링 → `GET`
        2. `create` : create.html 렌더링, 유효성 검증 및 영화 데이터 저장 후 detail.html 리다이렉트 → `GET` & `POST`
        3. `detail` : 단일 영화 데이터 조회 및 detail.html 렌더링 → `GET`
        4. 수정 대상 영화 데이터 조회 및 update.html 렌더링, 유효성 검증 및 영화 데이터 수정 후 detail.html 리다이렉트 → `GET` & `POST`
        5. `delete` : 단일 영화 데이터 삭제 및 index.html 리다이렉트 → `POST`
    2. accounts
        1. `login` : login.html 렌더링 & 회원의 로그인 과정 진행 → `GET` & `POST`
        2. `logout` : DB와 클라이언트 쿠키에서 세션 데이터 삭제 → `POST`
        3. `signup` : signup.html 렌더링, 유효성 검증 및 회원 데이터 저장 후 index.html 리다이렉트 → `GET` & `POST`
        4. `update` : 수정 대상 회원 데이터 조회 및 update.html 렌더링, 유효성 검증 및 회원 데이터 수정 후 index.html 리다이렉트 → `GET` & `POST`
        5. `delete` : 단일 회원 데이터 삭제 및 index.html 리다이렉트 → `POST`
        6. `change_password` : change_password.html 렌더링, 비밀번호 변경 및 index.html 리다이렉트 → `GET` & `POST`
        

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
> 5. `accounts/models.py`
>     1. AbstractUser
> 6. `accounts/forms.py`
>     1. custom

- **결과 :** `base.html`
    - 문제 접근 방법 및 코드 설명
    
    ✔ 로그인 여부에 따라 달라지는 화면
    
    ```html
    <body>
      {% if user.is_authenticated %}
        <p>Hello, {{user}}</p>
        <a href="{% url 'accounts:update' %}">회원 정보 수정</a>
        <form action="{% url 'accounts:logout' %}" method="POST">
          {% csrf_token %}
          <input type="submit" value="Logout">
        </form>
        <form action="{% url 'accounts:delete' %}">
          {% csrf_token %}
          <input type="submit" value="회원탈퇴">
        </form>
      {% else %}
        <a href="{% url 'accounts:login' %}">Login</a>
        <a href="{% url 'accounts:signup' %}">Signup</a>
      {% endif %}
      <hr>
      
      {% block content %}
      
      {% endblock content %}
    </body>
    ```
    
- **결과 :** `mypjt/urls.py`
    
    ```python
    from django.contrib import admin
    from django.urls import path, include
    from django.conf import settings
    from django.conf.urls.static import static
    
    urlpatterns = [
        path('admin/', admin.site.urls),
        path('movies/', include('movies.urls')),
        path('accounts/', include('accounts.urls')),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    ```
    

- **결과 :** `movies/urls.py`
    
    ```python
    from django.urls import path
    from . import views
    
    app_name = 'movies'
    urlpatterns = [
        path('', views.index, name='index'),
        path('create/', views.create, name='create'),
        path('<int:pk>/', views.detail, name='detail'),
        path('<int:pk>/update/', views.update, name='update'),
        path('<int:pk>/delete/', views.delete, name='delete'),
    ]
    ```
    
- **결과 :** `accounts/urls.py`
    
    ```python
    from django.urls import path
    from . import views
    
    app_name = 'accounts'
    urlpatterns = [
        path('login/', views.login, name='login'),
        path('logout/', views.logout, name='logout'),
        path('signup/', views.signup, name='signup'),
        path('delete/', views.delete, name='delete'),
        path('update/', views.update, name='update'),
        path('password/', views.change_password, name='change_password'),
    ]
    ```
    
- **결과 :** `movies/models.py`
    - 문제 접근 방법 및 코드 설명
    
    ✔ 모델 필드 지정
    
    ```python
    from django.db import models
    
    class Movie(models.Model):
        title = models.CharField(max_length=20)
        description = models.TextField()
    ```
    
- **결과 :** `movies/forms.py`
    - 문제 접근 방법 및 코드 설명
    
    ✔ 폼에 나타날 필드 지정
    
    ```python
    from django import forms
    from .models import Movie
    
    class MovieForm(forms.ModelForm):
    
        class Meta:
            model = Movie
            fields = '__all__'
    ```
    
- **결과 :** `accounts/models.py`
    - 문제 접근 방법 및 코드 설명
    
    ✔ AbstractUser 모델 클래스를 상속
    
    ```python
    from django.db import models
    from django.contrib.auth.models import AbstractUser
    
    class User(AbstractUser):
        pass
    ```
    
- **결과 :** `accounts/forms.py`
    - 문제 접근 방법 및 코드 설명
    
    ✔ 커스텀 폼 클래스 생성
    
    ```python
    from django.contrib.auth.forms import UserCreationForm, UserChangeForm
    from django.contrib.auth import get_user_model
    
    class CustomUserCreationForm(UserCreationForm):
    
        class Meta(UserCreationForm.Meta):
            model = get_user_model()
    
    class CustomUserChangeForm(UserChangeForm):
    
        class Meta(UserChangeForm.Meta):
            model = get_user_model()
            fields = ('first_name', 'last_name',)
    ```
    

<aside>
💡 **내가 생각하는 이 문제의 포인트**

유저 CRUD의 Model과 Form의 구조 파악

</aside>

---

## B. INDEX

> 📌 **요구 사항**
> 
> 
> “전체 영화 목록 조회 페이지”
> 
> - 데이터베이스에 존재하는 모든 영화의 목록을 표시
> - 적절한 HTML 요소를 사용하여 영화 제목을 표시
> - 제목을 클릭 시 해당 영화의 상세 조회 페이지(detail.html)로 이동

- **결과 :**
    - 문제 접근 방법 및 코드 설명
    
    ✔ 모델에 저장된 데이터 전부 불러오고, DTL을 사용해 출력하기
    
    ```python
    # movies/views.py
    from django.shortcuts import render, redirect
    from .models import Movie
    from django.views.decorators.http import require_safe
    
    @require_safe
    def index(request):
        movies = Movie.objects.all()
        context = {
            'movies':movies,
        }
        return render(request, 'movies/index.html', context)
    ```
    
    ```html
    {% comment %} movies/index.html {% endcomment %}
    
    {% extends 'base.html' %}
    
    {% block content %}
      <h1>INDEX</h1>
      <a href="{% url 'movies:create' %}">[CREATE]</a>
      <hr>
    
      {% for movie in movies %}
        <a href="{% url 'movies:detail' movie.pk %}">{{movie.title}}</a>
      {% endfor %}
      <hr>
    {% endblock content %}
    ```
    

<aside>
💡 **내가 생각하는 이 문제의 포인트**

DTL: `{% for movie in movies %}` `{% endfor %}`

</aside>

---

## C. DETAIL

> 📌 **요구 사항**
> 
> 
> “영화 상세 정보 페이지”
> 
> - 특정 영화의 상세 정보를 표시
> - 해당 영화의 수정 및 삭제 버튼을 표시
> - 전체 영화 목록 조회 페이지(index.html)로 이동하는 링크를 표시

- **결과 :**
    - 문제 접근 방법 및 코드 설명
    
    ✔ 특정 데이터 접근을 위한 PK값 전달
    
    ```python
    # movies/views.py
    from django.shortcuts import render
    from .models import Movie
    from django.views.decorators.http import require_safe
    
    @require_safe
    def detail(request, pk):
        movie = Movie.objects.get(pk=pk)
        context = {
            'movie':movie,
        }
        return render(request, 'movies/detail.html', context)
    ```
    
    ```html
    {% comment %} movies/detail.html {% endcomment %}
    
    {% extends 'base.html' %}
    
    {% block content %}
      <h1>DETAIL</h1>
      <hr>
      <h2>{{movie.title}}</h2>
      <p>{{movie.description}}</p>
      <a href="{% url 'movies:update' movie.pk %}">UPDATE</a>
      <form action="{% url 'movies:delete' movie.pk%}" method="POST">
        {% csrf_token %}
        <input type="submit" value="DELETE">
      </form>
      <a href="{% url 'movies:index' %}">BACK</a>
      <hr>
    {% endblock content %}
    ```
    
    1. `movie = Movie.objects.get(pk=pk)`
        
        지정 pk값 데이터에 접근
        

<aside>
💡 **내가 생각하는 이 문제의 포인트**

view에서 PK값을 전달하고, 이를 템플릿에서 사용

</aside>

---

## D. CREATE

> 📌 **요구 사항**
> 
> 
> “영화 생성 페이지”
> 
> - 특정 영화를 생성하기 위한 HTML form 요소를 표시
> - 표시되는 form은 Movie 모델 클래스에 기반한 ModelForm
> - 작성한 정보는 제출(submit)시 단일 영화 데이터를 저장하는 URL로 요청과 함께 전송
> - 전체 영화 목록 조회 페이지(index.html)로 이동하는 링크를 표시

- **결과 :**
    - 문제 접근 방법 및 코드 설명
    
    ✔ form 활용
    
    ```python
    # movies/views.py
    from django.shortcuts import render, redirect
    from .forms import MovieForm
    from django.views.decorators.http import require_http_methods
    
    @require_http_methods(['GET', 'POST'])
    def create(request):
        if request.method == "POST":
            form = MovieForm(request.POST)
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
    {% comment %} movies/create.html {% endcomment %}
    
    {% extends 'base.html' %}
    
    {% block content %}
      <h1>CREATE</h1>
      <hr>
      <form action="{% url 'movies:create' %}" method="POST">
        {% csrf_token %}
        {{form.as_p}}
        <input type="submit" value="Submit">
      </form>
      <hr>
      <a href="{% url 'movies:index' %}">BACK</a>
    {% endblock content %}
    ```
    
    1. `request.method != "POST"`
        
        페이지 첫 접근시 빈 폼 출력 → `form = MovieForm()`
        
    2. `request.method == "POST"`
        
        빈 폼에 내용 입력 후 저장 시 해당 폼을 저장 
        
        → `form = MovieForm(request.POST)` , `movie = form.save()`
        
    

<aside>
💡 **내가 생각하는 이 문제의 포인트**

GET 방식으로 접근 시 빈 폼 출력 → POST 방식으로 접근 시 폼 저장

</aside>

---

## E. UPDATE

> 📌 **요구 사항**
> 
> 
> “영화 수정 페이지”
> 
> - 특정 영화를 수정하기 위한 HTML form 요소를 표시
> - 표시되는 form은 Movie 모델 클래스에 기반한 ModelForm
> - HTML input 요소에는 기존 데이터를 출력
> - Reset 버튼은 사용자의 모든 입력을 초기 값으로 재설정
> - 작성한 정보는 제출(submit)시 단일 영화 데이터를 수정하는 URL로 요청과 함께 전송
> - 영화 상세 정보 페이지(detail.html)로 이동하는 링크를 표시

- **결과 :**
    - 문제 접근 방법 및 코드 설명
    
    ✔ 지정 데이터 수정을 위한 접근 및 수정
    
    ```python
    # movies/views.py
    from django.shortcuts import render, redirect
    from .models import Movie
    from .forms import MovieForm
    from django.views.decorators.http import require_http_methods
    
    @require_http_methods(['GET', 'POST'])
    @login_required
    def update(request, pk):
        movie = Movie.objects.get(pk=pk)
        if request.method == "POST":
            form = MovieForm(request.POST, instance=movie)
            if form.is_valid():
                form.save()
                return redirect('movies:detail', movie.pk)
        else:
            form = MovieForm(instance=movie)
        
        context = {
            'form':form,
            'movie':movie,
        }
        return render(request, 'movies/update.html', context)
    
    @require_POST
    def delete(request, pk):
        movie = Movie.objects.get(pk=pk)
        movie.delete()
        return redirect('movies:index')
    ```
    
    ```html
    {% comment %} movies/update.html {% endcomment %}
    
    {% extends 'base.html' %}
    
    {% block content %}
      <h1>UPDATE</h1>
      <hr>
    
      <form action="{% url 'movies:update' movie.pk %}" method="POST">
        {% csrf_token %}
        {{form.as_p}}
        <input type="reset" value="Reset">
        <input type="submit" value="Submit">
      </form>
      <hr>
      <a href="{% url 'movies:detail' movie.pk %}">BACK</a>
    {% endblock content %}
    ```
    
    1. `movie = Movie.objects.get(pk=pk)`
        
        지정 데이터 PK 값을 이용해 접근
        
    2. `request.method != "POST"`
        
        수정을 위해 해당 데이터를 담은 폼 전달 → `form = MovieForm(instance=movie)`
        
    3. `request.method == "POST"`
        
        지정 폼에 내용 입력 후 저장 시 해당 폼을 저장 
        
        → `form = MovieForm(request.POST, instance=movie)`
        
    4. `movie = Movie.objects.get(pk=pk)`
        
        삭제할 데이터 접근 및 `movie.delete()`
        
    - 이 문제에서 어려웠던 점
        
        PK로 데이터 접근, instance로 지정 데이터 폼 전달
        

<aside>
💡 **내가 생각하는 이 문제의 포인트**

수정을 위해서  GET일 때도, POST일 때도 instance로 지정 데이터 접근

</aside>

---

## F. LOGIN

> 📌 **요구 사항**
> 
> 
> “로그인 페이지”
> 
> - 로그인을 위한 HTML form 요소를 표시
> - 작성한 정보는 제출(submit)시 로그인 URL로 요청과 함께 전송

- **결과 :**
    - 문제 접근 방법 및 코드 설명
    
    ✔  AuthenticationForm, login 로직 활용
    
    ```python
    # accounts/views.py
    from django.shortcuts import render, redirect
    from django.contrib.auth.forms import AuthenticationForm
    from django.views.decorators.http import require_http_methods, require_POST
    from django.contrib.auth import login as auth_login
    
    @require_http_methods(['GET', 'POST'])
    def login(request):
        if request.user.is_authenticated:
            return redirect('movies:index')
        
        if request.method == "POST":
            form = AuthenticationForm(request, request.POST)
            if form.is_valid():
                auth_login(request, form.get_user())
                return redirect(request.GET.get('next') or 'movies:index')
        else:
            form  = AuthenticationForm()
    
        context = {
            'form': form,
        }
        return render(request, 'accounts/login.html', context)
    
    @require_POST
    def logout(request):
        auth_logout(request)
        return redirect('movies:index')
    ```
    
    ```html
    {% comment %} accounts/login.html {% endcomment %}
    
    {% extends 'base.html' %}
    
    {% block content %}
      <h1>Login</h1>
    
      <form action="{% url 'accounts:login' %}" method="POST">
        {% csrf_token %}
        {{form.as_p}}
        <input type="submit" value="Submit">
      </form>
    {% endblock content %}
    ```
    
    1. `request.user.is_authenticated`
        
        로그인 상태의 유저라면 인덱스로 이동
        
    2. `request.method != "POST"`
        
        빈 폼 출력 → `form  = AuthenticationForm()`
        
    3. `request.method == "POST"`
        
        빈 폼에 내용 입력 후 로그인
        
        → `form = AuthenticationForm(request, request.POST)` , `auth_login(request, form.get_user())`
        
    - 이 문제에서 어려웠던 점
        
        장고 내장 로그인 폼 사용 및 해당 폼으로 로그인
        

<aside>
💡 **내가 생각하는 이 문제의 포인트**

`AuthenticationForm()` , `auth_login(request, form.get_user())`

</aside>

---

## G. SIGNUP

> 📌 **요구 사항**
> 
> 
> “회원가입 페이지”
> 
> - 회원가입을 위한 HTML form 요소를 표시
> - 작성한 정보는 제출(submit)시 회원가입 URL로 요청과 함께 전송

- **결과 :**
    - 문제 접근 방법 및 코드 설명
    
    ✔ 커스텀 폼 사용
    
    ```python
    # accounts/views.py
    from django.shortcuts import render, redirect
    from .forms import CustomUserCreationForm
    from django.contrib.auth import login as auth_login
    from django.views.decorators.http import require_http_methods
    
    @require_http_methods(['GET', 'POST'])
    def signup(request):
        if request.method == "POST":
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                auth_login(request, user)
                return redirect('movies:index')
        else:
            form = CustomUserCreationForm()
    
        context = {
            'form':form,
        }
        return render(request, 'accounts/signup.html', context)
    ```
    
    ```html
    {% comment %} accounts/signup.html {% endcomment %}
    
    {% extends 'base.html' %}
    
    {% block content %}
      <h1>Signup</h1>
      <form action="{% url 'accounts:signup' %}" method="POST">
        {% csrf_token %}
        {{form.as_p}}
        <input type="submit" value="Submit">
      </form>
    {% endblock content %}
    ```
    
    1. `request.method != "POST"`
        
        빈 폼 출력 → `form = CustomUserCreationForm()`
        
    2. `request.method == "POST"`
        
        빈 폼에 내용 입력 후 저장 시 해당 폼을 저장 후 로그인
        
        → `form = CustomUserCreationForm(request.POST)` , `user = form.save()` , `auth_login(request, user)`
        

<aside>
💡 **내가 생각하는 이 문제의 포인트**

빈 폼 출력 → 폼 내용 작성 → 폼 내용 저장 → 로그인의 순서 기억

</aside>

---

## H. UPDATE

> 📌 **요구 사항**
> 
> 
> “회원정보수정 페이지”
> 
> - 회원정보수정을 위한 HTML form 요소를 표시
> - 작성한 정보는 제출(submit)시 회원정보수정 URL로 요청과 함께 전송

- **결과 :**
    - 문제 접근 방법 및 코드 설명
    
    ✔ 커스텀 폼 사용, 회원 탈퇴 시 데이터 삭제 후 로그아웃
    
    ```python
    # accounts/views.py
    from django.shortcuts import render, redirect
    from .forms import CustomUserChangeForm
    from django.views.decorators.http import require_http_methods
    
    @require_http_methods(['GET', 'POST'])
    def update(request):
        if request.method == "POST":
            form = CustomUserChangeForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                return redirect('movies:index')
        else:
            form = CustomUserChangeForm(instance=request.user)
        
        context = {
            'form':form,
        }
        return render(request, 'accounts/update.html', context)
    
    @require_POST
    def delete(request):
        request.user.delete()
        auth_logout(request)
        return redirect('movies:index')
    ```
    
    ```html
    {% comment %} accounts/update.html {% endcomment %}
    
    {% extends 'base.html' %}
    
    {% block content %}
      <h1>회원 정보 수정</h1>
      <form action="{% url 'accounts:update' %}" method="POST">
        {% csrf_token %}
        {{form.as_p}}
        <input type="submit" value="Submit">
      </form>
    {% endblock content %}
    ```
    
    1. `request.method != "POST"`
        
        수정을 위해 해당 데이터를 담은 폼 전달 
        
        → `form = CustomUserChangeForm(instance=request.user)`
        
    2. `request.method == "POST"`
        
        지정 폼에 내용 입력 후 저장 시 해당 폼을 저장 
        
        → `form = CustomUserChangeForm(request.POST, instance=request.user)`
        
    
    - 이 문제에서 어려웠던 점
        
        기존 CRUD에서 사용한 instance와 다른 접근 방식 `request.user`
        

<aside>
💡 **내가 생각하는 이 문제의 포인트**

기존 CRUD에서 데이터에 접근하는 방식과는 다른 접근 방식 → `user` 키워드

</aside>

---

## I. CHANGE_PASSWORD

> 📌 **요구 사항**
> 
> 
> “비밀번호변경 페이지”
> 
> - 비밀번호변경 을 위한 HTML form 요소를 표시
> - 작성한 정보는 제출(submit)시 비밀번호변경 URL로 요청과 함께 전송

- **결과 :**
    - 문제 접근 방법 및 코드 설명
    
    ✔ PasswordChangeForm, update_session_auth_hash 사용
    
    ```python
    # accounts/views.py
    from django.shortcuts import render, redirect
    from django.contrib.auth.forms import PasswordChangeForm
    from django.contrib.auth import update_session_auth_hash
    from django.views.decorators.http import require_http_methods
    
    @require_http_methods(['GET', 'POST'])
    def change_password(request):
        if request.method == "POST":
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                return redirect('movies:index')
        else:
            form = PasswordChangeForm(request.user)
        
        context = {
            'form':form,
        }
        return render(request, 'accounts/change_password.html', context)
    ```
    
    ```html
    {% comment %} accounts/change_password.html {% endcomment %}
    
    {% extends 'base.html' %}
    
    {% block content %}
      <h1>비밀번호 변경</h1>
      <form action="{% url 'accounts:change_password' %}" method="POST">
        {% csrf_token %}
        {{form.as_p}}
        <input type="submit" value="Submit">
      </form>
    {% endblock content %}
    ```
    
    1. `request.method != "POST"`
        
        기존 비밀번호를 담은 폼 전달 → `form = PasswordChangeForm(request.user)`
        
    2. `request.method == "POST"`
        
        비밀번호 변경 후 내용 저장 → `form.save()`
        
    3. `update_session_auth_hash(request, form.user)`
        
        비밀번호 변경 후 로그아웃 막기
        

<aside>
💡 **내가 생각하는 이 문제의 포인트**

기존 비밀번호 출력 → 비밀번호 변경 → 폼 저장 → 로그아웃 방지

</aside>

---

# 후기

- 여러번 반복해서 작성하다보니 익숙해져서 시간이 매우 절약되었다.
- CRUD와 유저CRUD에서 데이터에 접근하는 방식이 차이가 있는 것이 헷갈리지만, 반복해서 작성하다보면 익숙해질 것 같다.