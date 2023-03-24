# PJT 03 - WEB(Cinema)

### 이번 PJT를 통해 배운 내용

- HTML을 통한 웹 페이지 마크업 이해
- CSS 라이브러리의 이해와 활용
- Bootstrap 컴포넌트 및 Grid system을 활용한 반응형 레이아웃 구성

---

## A. Navigation Bar

> 📌 **요구사항**
> 
> - Navbar
>     1. Bootstrap Navbar Component를 참고합니다.
>     2. 스크롤을 하더라도 항상 화면 상단에 고정되어 있습니다.
>     3. 로고 이미지는 제공된 logo.png를 사용합니다.
>     4. 로고 이미지는 하이퍼링크 역할을 하며, 클릭 시 02_home.html로 이동해야 합니다.
>     5. 내비게이션 메뉴 중 Home, Community는 하이퍼링크 역할을 하며,
>     클릭 시 각각 02_home.html, 03_community.html로 이동해야 합니다.
>     6. 내비게이션 메뉴 중 Login은 클릭 시 Bootstrap Modal Component가 나타납니다.
>     7. Modal Component 내부에는 HTML form 요소를 배치합니다.
>     8. Viewport의 가로 크기 별 반응형 디자인은 스크린 샷 예시를 참고하여 일치하도록 합니다.

- **결과 :**
    - 문제 접근 방법 및 코드 설명
    
    ✔ 모든 페이지에서 볼 수 있어야 하기 때문에, `block` 에 포함시키지 않고 `base.html` 에 구현
    
    ---
    
    - Navigation
        
        ```html
        #1  <nav class="navbar navbar-expand-md navbar-dark bg-dark d-flex fixed-top"  data-bs-theme="dark">
        #2    <div class="container-fluid">
        #3      <a class="box" href="{% url 'cinema:home' %}">
        #4        <img style="height: 40px" src="{%static 'images/logo.png'%}" alt="logo">
        #5      </a>
        #6      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        #7        <span class="navbar-toggler-icon"></span>
        #8      </button>
        #9      <div class="collapse navbar-collapse" id="navbarNav">
        #10       <ul class="navbar-nav">
        #11         <li class="nav-item active">
        #12           <a class="nav-link" aria-current="page" href="{% url 'cinema:home' %}" style="text-decoration: none;">
        #13             <div class="text-white">Home</div>
        #14           </a>
        #15         </li>
        #16         <li class="nav-item active pe-2">
        #17           <a class="nav-link" href="{% url 'cinema:community' %}" style="text-decoration: none;">
        #18             <div class="text-white">Community</div>
        #19           </a>
        #20         </li>
        #21         <li class="nav-item active my-2">
        #22           <div class="text-white" data-bs-toggle="modal" data-bs-target="#exampleModal" style="cursor: pointer;">Login</div>
        #23         </li>
        #24       </ul>
        #25     </div>
        #26   </div>
        #27 </nav>
        ```
        
        1. `#1` 
            
            navigation bar : 검정 색상, `flex` , `fixed-top` - 상단 고정
            
        2. `#2`
            
            반응형 웹을 위해 `container` 에 담기, `container-fluid` - 화면에 꽉 채우기
            
        3. `#3` 
            
            로고 들어가는 박스, 클릭 시 `home.html` 로 이동
            
            Django `naming URL patterns` : `{%static 'cinema:home'%}`
            
        4. `#4`
            
            로고, `static` 이용해 상대적 위치의 폴더 내부 이미지 가져오기
            
            Django `naming URL patterns` : `{%static 'images/logo.png'%}`
            
        5. `#6`
            
            toggler : `#9` 의 id를 받음, 버튼 클릭 시 `#9` 활성화
            
        6. `#9 ~ #20`
            
            toggler 활성화 시 보이는 메뉴, 각각 `home.html` , `community.html` 으로 이동
            
            Django `naming URL patterns` : `{% url 'cinema:home' %}`, `{% url 'cinema:community' %}`
            
        7. `#21`
            
            로그인, 클릭 시 모달 활성화
            
            `data-bs-toggle="modal"` , `data-bs-target="#exampleModal"` : 이후 등장하는 모달
            
    - Modal
        
        ```html
        #1  <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        #2    <div class="modal-dialog">
        #3      <div class="modal-content">
        #4        <div class="modal-header">
        #5          <h1 class="modal-title fs-5" id="exampleModalLabel">Login</h1>
        #6          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        #7        </div>
        #8        <form action="{% url 'cinema:login' %}" method="GET">
        #9          <div class="modal-body">
        #10           <div class="p-2">
        #11             <label for="email" class="form-label fs-5">Email address</label>
        #12             <input type="email" id="email" name="email" class="form-control rounded-0">
        #13             <div fs-6>We'll never share your email with anyone else.</div>
        #14           </div>
        #15           <div class="p-2">
        #16             <label for="pw" class="form-label fs-5">Pasword</label>
        #17             <input type="text" id="pw" name="pw" class="form-control rounded-0">
        #18           </div>
        #19           <div class="m-auto form-check">
        #20             <input type="checkbox" class="form-check-input" id="exampleCheck1" name="check">
        #21             <label class="form-check-label" for="exampleCheck1">Check me out</label>
        #22           </div>
        #23         </div>
        #24         <div class="modal-footer">
        #25           <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
        #26           <button type="submit" class="btn btn-primary">Submit</button>
        #27         </div>
        #28       </form>
        #29     </div>
        #30   </div>
        #31 </div>
        #32 <footer class="fixed-bottom" style="text-align: center">Web bootstrap PJT by @FLOWERDONK</footer>
        ```
        
        1. `#4 ~ #7`
            
            모달 헤더
            
        2. `#8 ~`
            
            `<form action="{% url 'cinema:login' %}" method="GET">` : Django 로그인 정보 `login.html` 로 전달
            
        3. `#24 ~ #27`
            
            `close`로 닫거나, 정보 입력 후 `submit`
            
        
    
    ---
    

<aside>
💡 **내가 생각하는 이 문제의 포인트**

`flex` , `position` , `button` , `link` 익숙해지기

</aside>

---

## B. Home

> 📌 **요구 사항**
> 
> - Header
>     1. Bootstrap Carousel Component로 구성합니다.
>     2. 이미지는 최소 3장 이상 사용하며 자동으로 전환됩니다.
> - Section
>     1. Section 내부의 개별 요소(article)들은 Bootstrap Card Component로 구성합니다.
>     2. 개별 요소들은 좌우 일정한 간격을 가집니다. (간격은 자유롭게 설정 가능)
>     3. Viewport의 가로 크기가 576px 미만일 경우 한 행에 1개씩 표시됩니다.
>     4. Viewport의 가로 크기가 576px 이상일 경우 한 행에 2개 이상 표시됩니다.
>     5. Viewport의 가로 크기 별 반응형 디자인은 스크린 샷 예시를 참고하여 일치하도록
>     합니다.

- **결과 :**
    - 문제 접근 방법 및 코드 설명
        
        ✔ `carousel` , `card` 사용
        
        ---
        
        - Carousel
            
            ```html
            #1  <div class="container-fluid">
            #2    <div class="row" style="height: 55px"></div>
            #3    <header class="row">
            #4      <div id="carouselExampleAutoplaying" class="carousel slide" data-bs-ride="carousel">
            #5        <div class="carousel-inner">
            #6          <div class="carousel-item active">
            #7            <img src="{%static 'images/header1.jpg'%}" class="d-block w-100" alt="header1">
            #8          </div>
            #9          <div class="carousel-item">
            #10           <img src="{%static 'images/header2.jpg'%}" class="d-block w-100" alt="header2">
            #11         </div>
            #12         <div class="carousel-item">
            #13           <img src="{%static 'images/header3.jpg'%}" class="d-block w-100" alt="header3">
            #14         </div>
            #15       </div>
            #16       <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleAutoplaying" data-bs-slide="prev">
            #17         <span class="carousel-control-prev-icon" aria-hidden="true"></span>
            #18         <span class="visually-hidden">Previous</span>
            #19       </button>
            #20       <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleAutoplaying" data-bs-slide="next">
            #21         <span class="carousel-control-next-icon" aria-hidden="true"></span>
            #22         <span class="visually-hidden">Next</span>
            #23       </button>
            #24     </div>
            #25   </header>
            .
            .
            .
            ```
            
            1. `#4 ~`
                
                회전하는 메인 사진들
                
            
        - Card
            
            ```html
            .
            .
            .
            #1  <main class="row p-5">
            #2    <div class="row">
            #3      <b class="text-center fs-1">Boxoffice</b>
            #4    </div>
            #5    <div class="row row-cols-1 row-cols-md-3 g-4">
            #6      <div class="col">
            #7        <div class="card">
            #8          <img src="{%static 'images/movie1.jpg'%}" class="card-img-top" alt="movie1">
                        <div class="card-body">
                          <h5 class="card-title">쇼생크 탈출</h5>
                          <p class="card-text">촉망 받던 은행 부지점장 ‘앤디(팀 로빈슨 分)’는 아내와 그 애인을 살해한 혐의로 종신형을 받고 쇼생크 교도소에 수감된다. 강력범들이 수감된 이곳에서 재소자들은 짐승 취급 당하고, 혹여 간수 눈에 잘못 보였다가는 개죽음 당하기 십상이다. 처음엔 적응 못하던 ‘앤디’는 교도소 내 모든 물건을 구해주는 ‘레드(모건 프리먼 分)’와 친해지며 교도소 생활에 적응하려 하지만, 악질 재소자에게 걸려 강간까지 당한다. 그러던 어느 날, 간수장의 세금 면제를 도와주며 간수들의 비공식 회계사로 일하게 되고, 마침내는 소장의 검은 돈까지 관리해주게 된다. 덕분에 교도소 내 도서관을 열 수 있게 되었을 무렵, 신참내기 ‘토미(길 벨로우스 分)’로부터 ‘앤디’의 무죄를 입증할 기회를 얻지만, 노튼 소장은 ‘앤디’를 독방에 가두고 ‘토미’를 무참히 죽여버리는데...</p>
                        </div>
                      </div>
                    </div>
                    <div class="col">
                      <div class="card">
                        <img src="{%static 'images/movie2.jpg'%}" class="card-img-top" alt="movie2">
                        <div class="card-body">
                          <h5 class="card-title">죽은 시인의 사회</h5>
                          <p class="card-text">미국 입시 명문고 웰튼 아카데미, 공부가 인생의 전부인 학생들이 아이비리그로 가기 위해 고군분투하는 곳. 새로 부임한 영어 교사 ‘키팅’은 자신을 선생님이 아닌 “오, 캡틴, 나의 캡틴”이라 불러도 좋다고 말하며 독특한 수업 방식으로 학생들에게 충격을 안겨 준다. 점차 그를 따르게 된 학생들은 공부보다 중요한 인생의 의미를 하나씩 알아가고 새로운 도전을 시작한다. 하지만 이를 위기로 여긴 다른 어른들은 이들의 용기 있는 도전을 시간 낭비와 반항으로 단정 지으며 그 책임을 ‘키팅’ 선생님에게 전가하는데...</p>
                        </div>
                      </div>
                    </div>
                    <div class="col">
                      <div class="card">
                        <img src="{%static 'images/movie3.jpg'%}" class="card-img-top" alt="movie3">
                        <div class="card-body">
                          <h5 class="card-title">다크나이트 라이즈</h5>
                          <p class="card-text">다크 나이트 신화의 전설이 끝난다. 배트맨이 조커와의 대결을 끝으로 세상에서 모습을 감춘 8년 후, 하비 덴트의 죽음에 대한 책임을 떠안은 배트맨은 모든 것을 희생하며 떠나고.. 범죄방지 덴트법으로 인해 한동안 평화가 지속되던 고담시의 파멸을 예고하며 나타난 마스크를 쓴 잔인한 악당, 최강의 적 베인이 등장한다. 베인은 배트맨이 스스로 택한 유배 생활에 종지부를 찍게 하지만, 다시 돌아온 배트맨에게 베인은 만만한 상대가 아니다. 자신을 거부한 사람들의 고통을 지켜볼 것인가, 정의의 수호자로 나설 것인가. 배트맨은 승패를 알 수 없는 마지막 전투를 시작하려 하는데…</p>
                        </div>
                      </div>
                    </div>
                    <div class="col">
                      <div class="card">
                        <img src="{%static 'images/movie4.jpg'%}" class="card-img-top" alt="movie4">
                        <div class="card-body">
                          <h5 class="card-title">그랜드 부다페스트 호텔</h5>
                          <p class="card-text">1927년 세계대전이 한창이던 어느 날, 세계 최고의 부호 마담 D.가 의문의 살인을 당한다. 유력한 용의자로 지목된 사람은 바로 전설적인 호텔 지배인이자 그녀의 연인 ‘구스타브’! 구스타브는 누명을 벗기 위해 충실한 로비보이 ‘제로’에게 도움을 청하고, 그 사이 구스타브에게 남겨진 마담 D.의 유산을 노리던 그녀의 아들 ‘드미트리’는 무자비한 킬러를 고용해 [그랜드 부다페스트 호텔]을 찾게 되는데…</p>
                        </div>
                      </div>
                    </div>
                    <div class="col">
                      <div class="card">
                        <img src="{%static 'images/movie5.jpg'%}" class="card-img-top" alt="movie5">
                        <div class="card-body">
                          <h5 class="card-title">그녀</h5>
                          <p class="card-text">다른 사람의 편지를 써주는 대필 작가로 일하고 있는 ‘테오도르’는 타인의 마음을 전해주는 일을 하고 있지만 정작 자신은 아내와 별거 중인 채 외롭고 공허한 삶을 살아가고 있다. 어느 날, 스스로 생각하고 느끼는 인공지능 운영체제 ‘사만다’를 만나게 되고, 자신의 말에 귀를 기울이며 이해해주는 ‘사만다’로 인해 조금씩 상처를 회복하고 행복을 되찾기 시작한 ‘테오도르’는 어느새 점점 그녀에게 사랑의 감정을 느끼게 되는데...</p>
                        </div>
                      </div>
                    </div>
                    <div class="col">
                      <div class="card">
                        <img src="{%static 'images/movie6.jpg'%}" class="card-img-top" alt="movie6">
                        <div class="card-body">
                          <h5 class="card-title">위대한 쇼맨</h5>
                          <p class="card-text">쇼 비즈니스의 창시자이자, 꿈의 무대로 전세계를 매료시킨 남자 ‘바넘’의 이야기에서 영감을 받아 탄생한 오리지널 뮤지컬 영화 <위대한 쇼맨>. <레미제라블> 이후 다시 뮤지컬 영화로 돌아온 휴 잭맨부터 잭 에프론, 미셸 윌리엄스, 레베카 퍼거슨, 젠다야까지 할리우드 최고의 배우들이 합류해 환상적인 앙상블을 선보인다. 여기에 <미녀와 야수> 제작진과 <라라랜드> 작사팀의 합류로 더욱 풍성해진 비주얼과 스토리, 음악까지 선보일 <위대한 쇼맨>은 ‘우리는 누구나 특별하다’는 메시지로 관객들에게 재미는 물론, 감동까지 선사할 것이다. THIS IS ME! 우리는 누구나 특별하다!</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </main>
              </div>
            ```
            
            1. `#2 ~ #4`
                
                home 페이지 header : `Bodoffice`
                
            2. `#5`
                
                `row-cols-1` : 행, 열 1개씩
                
                `row-cols-md-3` : md 이상 3개씩
                
            3. `#8`
                
                영화 카드들 
                
                `class="card-img-top"` 이미지를 해당 카드의 상단에 배치
                
        
        ---
        

<aside>
💡 **내가 생각하는 이 문제의 포인트**

이미지 다양한 방식으로 첨부하기

</aside>

---

## C. Community

> 📌 **요구 사항**
> 
> - Aside (게시판 목록)
>     1. HTML aside 요소로 이루어져 있습니다.
>     2. Bootstrap List Group Component로 구성합니다.
>     3. 내부의 각 항목은 클릭이 가능한 하이퍼링크이지만, URL은 별도로 없습니다.
>     4. Viewport의 가로 크기가 992px 미만일 경우
>     HTML main 요소 영역 전체만큼의 너비를 가집니다.
>     5. Viewport의 가로 크기가 992px 이상일 경우
>     HTML main 요소 영역 기준으로 좌측 1/6 만큼의 너비를 가집니다.
>     6. Viewport의 가로 크기 별 반응형 디자인은 스크린 샷 예시를 참고하여
>     일치하도록 합니다.
> - Section (게시판)
>     1. 게시판은 HTML section 요소로 이루어져 있습니다.
>     2. 게시판은 Viewport의 가로 크기에 따라 전혀 다른 요소를 표시합니다.
>     • Viewport의 가로 크기가 992px 미만일 경우
>     게시판은 HTML article 요소의 집합으로 표시되며,
>     HTML main 요소 영역 전체만큼의 너비를 가집니다.
>     • Viewport의 가로 크기가 992px 이상일 경우
>     게시판은 Bootstrap Tables Content로 구성되며,
>     HTML main 요소 영역 기준으로 우측 5/6 만큼의 너비를 가집니다.
> - Pagination
>     1. Bootstrap Pagination Component로 구성합니다.
>     2. 게시판 하단에 위치하며 너비는 자유롭게 설정합니다.
>     3. 자신의 영역 안에서 수평 중앙 정렬되어 있습니다.
>     4. 내부의 각 항목은 클릭이 가능한 하이퍼링크이지만, URL은 별도로 없습니다.

- **결과 :**
    - 문제 접근 방법 및 코드 설명
        
        ✔ 표 구현하는 다양한 방식 연습
        
        ---
        
        - Aside
            
            ```html
            #1  <div class="container">
            #2    <div class="row" style="height: 55px"></div>
            #3    <h1 class="row">community</h1>
            #4    <div class="row">
            #5      <div class="col-12 col-lg-2">
            #6        <ul class="list-group w-100">
            #7          <li class="list-group-item"><a href="#" style="text-decoration: none;">Boxoffice</a></li>
            #8          <li class="list-group-item"><a href="#" style="text-decoration: none;">Movies</a></li>
            #9          <li class="list-group-item"><a href="#" style="text-decoration: none;">Genres</a></li>
            #10         <li class="list-group-item"><a href="#" style="text-decoration: none;">Actors</a></li>
            #11       </ul>
            #12     </div>
            ```
            
            1. `#6`
                
                Aside : 카테고리별 선택 - 링크 연결
                
                `list-group` : 리스트로 카테고리 구현
                
            
        - Section(lg)
            
            ```html
            #1  <div class="col d-none d-lg-block">
            #2    <table class="table table-striped">
            #3      <thead>
            #4        <tr class="table-dark">
            #5          <th scope="col">영화 제목</th>
            #6          <th scope="col">글 제목</th>
            #7          <th scope="col">작성자</th>
            #8          <th scope="col">작성 시간</th>
            #9        </tr>
            #10     </thead>
            #11     <tbody>
            #12       <tr>
            #13         <th scope="row">Great Movie title</th>
            #14         <td>Best Movie Ever</td>
            #15         <td>user</td>
            #16         <td>1 minute ago</td>
            #17       </tr>
                      <tr>
                        <th scope="row">Great Movie title</th>
                        <td>Movie Test</td>
                        <td>user</td>
                        <td>1 minute ago</td>
                      </tr>
                      <tr>
                        <th scope="row">Great Movie title</th>
                        <td>Movie Test</td>
                        <td>user</td>
                        <td>1 minute ago</td>
                      </tr>
                      <tr>
                        <th scope="row">Great Movie title</th>
                        <td>Movie Test</td>
                        <td>user</td>
                        <td>1 minute ago</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            ```
            
            1. `#1`
                
                Section(large) : lg 이상 크기에서 보이는 영화 정보 데이터가 담긴 표
                
                `d-none d-lg-block` : 기본 `none` , lg 사이즈에서 보임
                
            2. `#3 ~`
                
                제목 : `<thread>` - `<tr>` - `<th>`
                
                내용 : `<tbody>` - `<tr>` - `<th>` , `<td>`
                
            
        - Section(default)
            
            ```html
            #1  <div class="row mt-3">
            #2    <div class="col d-lg-none">
            #3      <div class="row border border-2 border-start-0 border-end-0 border-bottom-0">
            #4        <a href="#" class="list-group-item list-group-item-action" aria-current="true">
            #5          <div class="w-100">
            #6            <h1 class="mb-1">Best Movie Ever</h1>
            #7          </div>
            #8          <p class="mb-1">Great Movie Title</p>
            #9          <div>user</div>
            #10         <p class="my-2">1 minute ago</p>
            #11       </a>
            #12     </div>
                    <div class="row border border-2 border-start-0 border-end-0 border-bottom-0">
                      <a href="#" class="list-group-item list-group-item-action">
                        <div class="w-100">
                          <h1 class="mb-1">Movie Test</h1>
                        </div>
                        <p class="mb-1">Great Movie Title</p>
                        <div>user</div>
                        <p class="my-2">1 minute ago</p>
                      </a>
                    </div>
                    <div class="row border border-2 border-start-0 border-end-0 border-bottom-0">
                      <a href="#" class="list-group-item list-group-item-action">
                        <div class="w-100">
                          <h1 class="mb-1">Movie Test</h1>
                        </div>
                        <p class="mb-1">Great Movie Title</p>
                        <div>user</div>
                        <p class="my-2">1 minute ago</p>
                      </a>
                    </div>
                  </div>
                </div>
            ```
            
            1. `#2`
                
                Section(default) : lg 미만 크기에서 보이는 영화 정보 데이터가 담긴 표
                
                `d-lg-none` : 기본 사이즈에선 보이다가, lg 사이즈 이상에선 사라짐
                
            
        - Page
            
            ```html
            #1  <div class="row">
            #2    <nav aria-label="Page navigation example">
            #3      <ul class="pagination justify-content-center">
            #4        <li class="page-item"><a class="page-link" href="#">Previous</a></li>
            #5        <li class="page-item"><a class="page-link" href="#">1</a></li>
                      <li class="page-item"><a class="page-link" href="#">2</a></li>
                      <li class="page-item"><a class="page-link" href="#">3</a></li>
                      <li class="page-item"><a class="page-link" href="#">Next</a></li>
                    </ul>
                  </nav>
                </div>
              </div>
            ```
            
            1. `#2`
                
                각 구역이 각각의 페이지로 넘어가는 네비게이션
                
            
        
        ---
        

<aside>
💡 **내가 생각하는 이 문제의 포인트**

`list` , `table` , `thread` , `page` 익숙해지기

</aside>

---

## D. Django

> 📌 **요구 사항**
> 
> 
> 위의 페이지를 Django로 구현
> 

- **결과 :**
    - 문제 접근 방법 및 코드 설명
    
    ✔ url → view → html 과정 반드시 기억
    
    ---
    
    - cinema
        - templates/cinema
            
            ```html
            # community.html
            
            {% extends 'base.html' %}
            {% load static %}
            
            {% block body %}
            <community contents>
            {% endblock body %}
            ```
            
            ```html
            # home.html
            
            {% extends 'base.html' %}
            {% load static %}
            
            {% block body %}
            <home contents>
            {% endblock body %}
            ```
            
            1. block
                
                `base.html` 에서 설정한 구역에 담을 내용 각각 적음
                
            
            ---
            
            ```html
            # login.html
            
            {% extends 'base.html' %}
            {% load static %}
            
            {% block popup %}
                <div class="container-fluid">
                    <div class="row" style="height: 60px"></div>
                    <h2>email : {{email}}</h2>
                    <h2>password : {{pw}}</h2>
                    <h2>check : {{check}}</h2>
                </div>
            {% endblock popup %}
            ```
            
            1. 데이터 출력
                
                전달 받은 데이터 출력
                
            
        
        ```python
        # urls.py
        
        from django.urls import path
        from . import views
        
        app_name = 'cinema'
        urlpatterns = [
            path('login/', views.login, name = 'login'),
            path('home/', views.home, name = 'home'),
            path('community/', views.community, name = 'community'),
        ]
        ```
        
        1. `config` → `cinema`
            
            `config/urls.py` 에서 `cinema/urls.py` 로 이동
            
            이후 `cinema/views.py` 에서 `html` 로 데이터 전송
            
        
        ---
        
        ```python
        # views.py
        
        from django.shortcuts import render
        
        def login(request):
            email = request.GET.get('email')
            pw = request.GET.get('pw')
            check = request.GET.get('check')
            
            context = {
                'email' : email,
                'pw' : pw,
                'check' : check,
            }
            return render(request, 'cinema/login.html', context)
        
        def home(request):
            return render(request, 'cinema/home.html')
        
        def community(request):
            return render(request, 'cinema/community.html')
        ```
        
        1. login
            
            `request` 에서 받은 데이터 변수에 저장
            
            *이후 유효성 검사를 진행해야 하나 구현하지 X*
            
            데이터 전송을 위해 딕셔너리 형태로 변환 후 리턴
            
        
    - config
        
        ```python
        # settings.py
        
        INSTALLED_APPS = [
            'cinema',
        ]
        
        TEMPLATES = [
            {
                'DIRS': [BASE_DIR / 'templates'],
                'APP_DIRS': True,
            },
        ]
        
        STATIC_URL = '/static/'
        
        STATICFILES_DIRS = [
            BASE_DIR / 'static',
        ]
        ```
        
        1. 어플
            
            `INSTALLED_APPS` 에 생성한 어플 `cinema` 추가
            
        2. 템플릿
            
            상대적 경로 설정
            
        3. `STATIC`
            
            이미지 첨부할 상대적 경로 설정
            
        
        ---
        
        ```python
        # urls.py
        
        from django.urls import path, include
        
        urlpatterns = [
            path('cinema/', include('cinema.urls')),
        ]
        ```
        
        1. `url`
            
            `cinema/` 접속 시 cinema 어플의 `views` 로 접근 가능하도록 경로 `include`
            
        
    - static/images
        1. images
            
            상대적 위치에서 이미지를 찾을 수 있도록 가장 바깥 폴더 하위 폴더 생성
            
            `settings.py` 에 관련 내용 추가
            
        
    - templates
        
        ```python
        # base.html
        
        <body>
          {% load static %}
          {% block popup %}
          {% endblock popup %}
          <navigation>
        	<modal>
          {% block body %}   
          {% endblock body %}
          <footer>
        </body>
        ```
        
        1. block
            
            각각의 html 파일에서 사용할 컨텐츠 나누기 `popup` , `body` , …
            
        
    
    ---
    

<aside>
💡 **내가 생각하는 이 문제의 포인트**

Django 구조, 데이터 전송 방법 및 순서 익히기

</aside>

---

# 후기

- Django 가상환경 생성부터 서버를 여는 것 까지의 과정을 연습할 수 있었다.
- Bootstrap을 활용한 flex 구조와 다양한 요소 구현에 익숙해질 수 있었다.