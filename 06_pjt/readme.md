# PJT 06 - 관계형 데이터베이스 설계

### 이번 PJT를 통해 배운 내용

- 데이터를 생성, 조회, 수정, 삭제할 수 있는 Web application 제작
- Django web framework를 사용한 데이터 처리
- Django Model과 ORM에 대한 이해
- Django Authentication System에 대한 이해
- Database many to one relationship(1:N) 및 many to many relationship(M:N) 에 대한 이해
- 페어로 진행, Git Fork - Pull Request 이용한 협력

---

## 📌 공통 **요구사항**

✅ 커뮤니티 웹 서비스의 데이터 구성 단계

✅ 영화 데이터의 생성, 조회, 수정, 삭제, 좋아요가 가능한 애플리케이션

✅ 로그인, 로그아웃, 회원가입, 회원탈퇴, 회원정보수정, 비밀번호변경, 팔로우가 가능
한 애플리케이션

✅ 앱 이름은 movies와 accounts로 지정

✅ Detail 페이지에서 댓글 및 대댓글 생성 가능

☑️ **좋아요, 팔로우, 댓글** 기능을 제외한 기능은 지난 pjt에서 구현했으므로 설명 생략

<aside>
💡 내가 맡은 파트

**“댓글 및 대댓글 기능 구현”**



---

## A. Model, Form

> 📌 **요구사항**
> 
> 
> “Comment”
> 
> | 필드명 | 데이터 유형 | 역할 |
> | --- | --- | --- |
> | content | varchar(100) | 댓글 내용 |
> | movie_id | integer | 외래 키(Movie 클래스 참조) |
> | user_id | integer | 외래 키(User 클래스 참조) |

- **결과 :**
    - 문제 접근 방법 및 코드 설명
    
    **✔ 댓글, 대댓글을 위한 모델 정의 및 어드민 등록**
    
    ```python
    # movies/models.py
    
    from django.db import models
    from django.conf import settings
    
    			...
    
    class Comment(models.Model):
        movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
        content = models.CharField(max_length=100)
        user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
        parent = models.ForeignKey(
            'self',    
            on_delete=models.CASCADE,
            null = True,
            related_name = 'replies',
        )
    
        def __str__(self):
            return self.content
    ```
    
    1. `movie`, `user` 필드
        - 각각 `Movie`, `User` 모델을 참조하는 필드들
            - 댓글을 생성할 때 필요한 게시글, 작성 유저 정보
    2. `parent` 필드
        - 참조하는 댓글의 유무에 따라 댓글, 대댓글 결정
        
    
    ```python
    # movies/forms.py
    
    from django import forms
    from .models import Movie, Comment
    
    			...
    
    class CommentForm(forms.ModelForm):
        
        class Meta:
            model = Comment
            fields = ('content', )
    ```
    
    1. `field` 지정
        - 유저에게 나타낼 필드 지정
            - `movie`, `user` 같은 경우에는 보여줄 필요가 없음
        
    
    ```python
    # movies/admin.py
    
    from django.contrib import admin
    from .models import Comment
    
    			...
    admin.site.register(Comment)
    ```
    
    1. `admin`
        - 어드민 사이트에서 생성, 조회, 수정, 삭제가 가능하도록 등록
    
    - 이 문제에서 어려웠던 점
        - 댓글 뿐 아니라 대댓글을 고려해 필드를 추가해주어야 했던 점
        - 댓글에서 유저에게 보여지는 필드는 오직 content 뿐이란 점

<aside>
💡 **내가 생각하는 이 문제의 포인트**

1. 댓글의 작성자 정보, 댓글이 작성된 게시글 정보를 저장하기 위한 필드 `movie`, `user`
2. 대댓글 유무 판단을 위한 필드 `parent`
</aside>

---

## B. DETAIL

> 📌 **요구 사항**
> 
> 
> “영화 상세 정보 페이지”
> 
> - 특정 영화의 상세 정보를 표시
> - 댓글을 작성할 수 있는 form을 표시
> - 댓글 삭제 버튼은 댓글 작성자에게만 표시
> - 해당 영화의 수정 및 삭제 버튼을 표시
> - 전체 영화 목록 조회 페이지(index.html)로 이동하는 링크를 표시

- **결과 :**
    - 문제 접근 방법 및 코드 설명
    
    **✔ 댓글 생성 폼과 댓글 목록을 유저에게 보여주기 위한 전달법**
    
    ### 1. 댓글 생성 및 삭제 url
    
    ```
    # movies/urls.py
    
    from django.urls import path
    from . import views
    
    app_name = 'movies'
    urlpatterns = [
    
    			...
    
        # Comment CREATE (댓글 생성)
        path('<int:pk>/comments/', views.comments_create, name='comments_create'),
    
        # Comment DELETE (댓글 삭제)
        path('<int:movie_pk>/comments/<int:comment_pk>/delete/', views.comments_delete, name='comments_delete'),
    ]
    ```
    
    1. `comments_create`
        - 게시글 pk 전달, 댓글 생성
    2. `comments_delete`
        - 게시글 pk, 댓글 pk 전달, 댓글 삭제
        
    
    ### 2. 댓글 폼, 댓글 목록 전달
    
    ```python
    # movies/views.py
    
    from django.shortcuts import render
    from .models import Movie
    from .forms import CommentForm
    from django.views.decorators.http import require_safe
    
    @require_safe
    def detail(request, pk):
        movies = Movie.objects.get(id=pk)
        comment_form = CommentForm()
        comments = movies.comment_set.all()
        re_comment_list = movies.comment_set.filter(parent__isnull=True) # 대댓글 리스트
        context = {
            'movies': movies,
            'comment_form': comment_form,
            'comments': comments,
            're_comment_list': re_comment_list,
        }
        return render(request, 'movies/detail.html', context)
    ```
    
    1. `comment_form`
        - 댓글 생성 폼(대댓글 포함)
    2. `comments`
        - 작성된 댓글 전체 목록
    3. `re_comment_list`
        - 작성된 대댓글 전체 목록
    
    - 이 문제에서 어려웠던 점
        - 댓글, 대댓글 작성 폼은 동일하다는 점
        - 댓글, 대댓글 목록을 따로 저장해서 전달해야한다는 점

<aside>
💡 **내가 생각하는 이 문제의 포인트**

1. 댓글 삭제 시, 댓글 pk 뿐만 아니라 게시글 pk도 전달
2. 댓글, 대댓글 목록을 각각 전달
</aside>

---

## C. 댓글

> 📌 **요구 사항**
> 
> - 로그인 한 회원만 댓글을 생성, 삭제 가능
> - 본인이 작성한 댓글에 대해서만 삭제 가능

- **결과 :**
    - 문제 접근 방법 및 코드 설명
    
    **✔ 댓글 생성 및 삭제 시 필요한 정보(게시글 pk, user 정보)**
    
    ### 1. 댓글 생성
    
    ```python
    # movies/views.py
    
    from django.shortcuts import redirect
    from .models import Movie, Comment
    from .forms import CommentForm
    from django.views.decorators.http import require_POST
    from django.contrib.auth.decorators import login_required
    
    @require_POST
    @login_required
    def comments_create(request, pk):
        if request.user.is_authenticated:
            movie = Movie.objects.get(pk=pk)
            comment_form = CommentForm(request.POST)
            parent_pk = request.POST.get('parent_pk')
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.movie = movie
                comment.user = request.user
    							...
                comment.save()
            return redirect('movies:detail', movie.pk)
        return redirect('accounts:login')
    ```
    
    1. `parent_pk`
        - 댓글 참조 여부 확인 → 댓글, 대댓글 판별
            - null이 아닐 경우 대댓글 로직 처리(*’D. 대댓글’* 참고)
    2. `comment_form.save(commit=False)`
        - 데이터베이스에 저장하기 전에 객체에 대한 추가적인 작업을 진행할 수 있도록 인스턴스만을 반환
        - `comment.movie`, `comment.user`
            - comment 모델에 필요한 필드들에 내용 채우기
    
    ### 2. 댓글 삭제
    
    ```python
    # movies/views.py
    
    from django.shortcuts import redirect
    from .models import Comment
    from django.views.decorators.http import require_POST
    from django.contrib.auth.decorators import login_required
    
    @require_POST
    @login_required
    def comments_delete(request, movie_pk, comment_pk):
        if request.user.is_authenticated:
            comment = Comment.objects.get(pk = comment_pk)
            if request.user == comment.user:
                comment.delete()    
            return redirect('movies:detail', movie_pk)
        return redirect('accounts:login')
    ```
    
    1. `request.user.is_authenticated`
        - 인증된 유저만 댓글 삭제 가능
    2. `request.user == comment.user`
        - 2차 검증, 댓글 작성자만 댓글 삭제 가능
    
    ### 3. 댓글 템플릿
    
    ```html
    {% comment %} movies/detail.html {% endcomment %}
    
    {% extends 'base.html' %}
    
    {% block content %}
      <h1>영화 상세 정보 페이지</h1>
    
    	  ...
    
    	{% comment %} 댓글 작성 {% endcomment %}
      <br>
      {% comment %} 댓글 {% endcomment %}
      <h5>댓글<h5>
      <form action="{% url 'movies:comments_create' movies.pk %}" method="POST">
        {% csrf_token %}
        {{comment_form}}
        <input type="submit" value="작성">
      </form>
      <hr>
    
    	{% comment %} 댓글 목록 {% endcomment %}
      <h5>댓글 목록<h5>
      <ul>
        {% for comment in comments %}
          <li>
    				{% comment %} 댓글 출력 {% endcomment %}
            {{comment.content}} - {{comment.user}}
    
    				{% comment %} 해당 댓글 작성자일 경우 수정, 삭제 출력 {% endcomment %}
            {% if request.user == comment.user %}
            <form action="{% url 'movies:comments_delete' movies.pk comment.pk %}" method="POST">
              {% csrf_token %}
              <input type="submit" value="삭제">
            </form>
            {% endif %}
          </li>
    
    				...
    
        {% endfor %}
      </ul>
    
    		...
    
    {% endblock content %}
    ```
    
    1. 댓글 출력
        - DTL `for` 사용
        - `{{comment.content}} - {{comment.user}}` : 댓글 내용 - 댓글 작성자
    2. `request.user == comment.user`
        - 요청 유저가 댓글을 작성한 유저일 경우 수정, 삭제 버튼 출력
    
    - 이 문제에서 어려웠던 점
        - 댓글 수정 및 삭제를 위한 유저 검증(view, template)
        - comment 모델에 반드시 지정해야할 외래 키 참조 필드(movie, user)

<aside>
💡 **내가 생각하는 이 문제의 포인트**

1. `comment_form.save(commit=False)` 를 활용해 모델 외래 키 참조 필드 값 지정
2. `request.user.is_authenticated`, `request.user == comment.user` 를 활용한 유저 검증
</aside>

---

## D. 대댓글

> 📌 **요구 사항**
> 
> 
> 대댓글은 댓글이며, 다른 댓글을 참조
> 
> - 즉, 댓글과 대댓글의 차이점은 참조하는 댓글의 유무
> - 참조하는 댓글이 있다면 대댓글
> - 참조하는 댓글이 없다면 그냥 댓글

- **결과 :**
    - 문제 접근 방법 및 코드 설명
    
    **✔ 댓글을 참조하는 경우가 대댓글, 대댓글일 경우를 댓글과 구분하려 처리**
    
    ### 1. 대댓글 model 추가 사항
    
    ```python
    # movies/models.py
    
    from django.db import models
    from django.conf import settings
    
    			...
    
    class Comment(models.Model):
    			...
        parent = models.ForeignKey(
            'self',    
            on_delete=models.CASCADE,
            null = True,
            related_name = 'replies',
        )
    			...
    ```
    
    1. `parent`
        - 외래 참조 키이나, 참조하는 모델이 자기 자신
        - 댓글, 대댓글 구별
            - `null` 일 경우, 댓글
            - 아닐 경우 참조하는 댓글이 있다는 것이므로, 대댓글
    
    ### 2. 대댓글 생성
    
    ```python
    # movies/views.py
    
    from django.shortcuts import redirect
    from .models import Movie, Comment
    from .forms import CommentForm
    from django.views.decorators.http import require_POST
    from django.contrib.auth.decorators import login_required
    
    @require_POST
    @login_required
    def comments_create(request, pk):
        if request.user.is_authenticated:
    				...
            if comment_form.is_valid():
    						...
                if parent_pk: # 답글
                    parent_comment = Comment.objects.get(pk=parent_pk)
                    comment.parent = parent_comment
    				...
    ```
    
    1. `parent_pk`
        - `null` 이 아닐 경우 대댓글이므로, `parent` 필드에 값 지정
    
    ### 3. 대댓글 템플릿
    
    ```html
    {% comment %} movies/detail.html {% endcomment %}
    
    {% extends 'base.html' %}
    
    {% block content %}
      <h1>영화 상세 정보 페이지</h1>
    
    	  ...
    
      <ul>
        {% for comment in comments %}
          <li>
    				{% comment %} 댓글 출력 {% endcomment %}
    
    					...
    
          </li>
    
    			{% comment %} 해당 댓글 대댓글 출력 {% endcomment %}
          {% for reply in comment.replies.all %}
            <p> >> {{reply.content}} </p>
          {% endfor %}
    
    			{% comment %} 해당 댓글 대댓글 작성 {% endcomment %}
          <form action="{% url 'movies:comments_create' movies.pk %}" method="POST">
            <input type="hidden" name="parent_pk" value="{{ comment.pk }}">
              {% csrf_token %}
              {{comment_form}} 
            <input type="submit" value="대댓글">
          </form>
    
        {% endfor %}
      </ul>
    
    		...
    
    {% endblock content %}
    ```
    
    1. 대댓글 출력
        - DTL `for` 사용
        - `{{reply.content}}` : 내용만 출력
    
    - 이 문제에서 어려웠던 점
        - 댓글과 구별되는 필드 `parent`

<aside>
💡 **내가 생각하는 이 문제의 포인트**

1. 자기 자신을 참조하는 외래키 필드`parent_pk` 가 있다면, `parent` 값 지정
</aside>

---

# 후기

- 처음으로 페어로 진행한 프로젝트로, 다른 사람의 코드 작성 방식과 나의 작성 방식이 매우 달라서 이에 적응하기가 어려워 상대방의 코드를 처음부터 끝까지 읽어가며 이해하는 과정에 시간이 걸렸다. 하지만 나와 다른 점을 통해 배워갈 점을, 예를 들면 주석을 적는 다는 것, 많이 얻어간 것 같아서 좋았다.
- 깃의 Folk & Pull Request 방식을 처음 사용해보았는데, 처음엔 그 방식에 적응하지 못해 어려웠지만, 어려움에 비해 유용함이 매우 커서 적응하기 위해 노력했다.
- 외래 키 참조 모델 필드를 처음 활용한 프로젝트였는데, 댓글 뿐 아니라 대댓글을 구현하는 것이 지금까지 구현해왔던 모델들에 비해 매우 어려워서 헷갈렸다. 하지만 이번 프로젝트로 인해 이에 좀 적응하게 된 것 같다.