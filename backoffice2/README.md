### 1. 로컬 실행 가이드.

```shell
# 프로젝트의 패키지 종속성에 따라 패키지들을 설치합니다.
$ pip install -r requirements.txt

# 현재는 SQLITE 파일을 그대로 업로드했기 때문에 마이그레이션 과정을 할 필요는 없지만, 마이그레이션 진행합니다.
$ python manage.py makemigrations
$ python manage.py migrate

# 프로젝트를 실행합니다.
$ python manage.py runserver

# Edge 또는 Firefox 등등 인터넷 접속하여 `http://127.0.0.1:8000/` 로 접속합니다.
# 현재는 과제의 확인을 원할하게 하기 위해서 urlpattern을 accounts로 설정하지 않았습니다.
# 따라서 위의 주소로 접속하면 됩니다.
```

---

### 2. DB Schema

![](https://velog.velcdn.com/images/chan9708/post/aedcc6ce-a49a-4621-a6d6-5b8bac1ea81c/image.png)

> **회원 정보**

* **email**
* **name**
* **phone_number**

> **회원 상태**

* **대기**
* **승인**
* **거절**
* **탈퇴**

> **회원 등급**

* **마스터 (Superuser)**
* **관리자**
* **일반**

> **CustomUser 사용을 위한 권한 설정**

* **is_active** 
* **is_staff**
* **is_superuser** 

> **권한 설정**

* **permission_approve**
* **permission_list**
* **permission_edit**
* **permission_delete**

> **시간 및 텍스트 정보**
* date_joined = models.DateTimeField(default=timezone.now)
<br>
* date_rejected = models.DateTimeField(blank=True, null=True)
* reject_reason = models.TextField(blank=True, null=True)
<br>
* date_secession = models.DateTimeField(blank=True, null=True)
* secession_reason = models.TextField(blank=True, null=True) 

---

### WARNING

BO를 설계하는데 모델링을 하나로 처리한 점은 실제로 이용하기엔 무리가 많습니다.
다만, 요구 조건의 View, Template의 동작을 즉각 확인하고 구현하기 위하여 `단일 모델`로 구축했습니다.

> 실 사용에 사용되는 모델이라면,
> **1. User 모델**
> **2. Role 모델**
> **3. Permission 모델**
>  
> 최소한 이 3가지는 분리했을 것입니다.

---
---

### 3. 프로젝트 설계 구조

```shell
D:.
└─backoffice
    ├─accounts
    │  ├─migrations
    │  └─templates
    │     ├─registration # 회원 가입, 로그인 템플릿
    │     ├─standby      # 회원 가입 승인 | 거절 | 대기 리스트
    │     └─user         # 승인된 회원들 리스트
    │  
    └─backoffice
```

> **1. View의 구조**
```python
# 메인 페이지 렌더링
def home(request):
# AJAX 요청을 받아 이메일 중복 검사를 수행
def check_email(request):
# 회원 가입 페이지를 렌더링하고 회원 가입 요청을 처리
class SignUpView(CreateView):
# 로그인 페이지를 렌더링하고 로그인 요청을 처리
class CustomLoginView(LoginView):
# 마스터 및 관리자 권한을 가진 사용자들이 승인 대기중인 사용자 목록 보기 처리
class StandbyUserListView(ListView):
# 마스터 및 관리자 권한을 가진 사용자들이 승인 대기중인 사용자들의 상세 정보 보기 처리
class StandbyUserDetailView(DetailView):
# 사용자들이 등록된 모든 사용자 목록 보기 처리
class UserListView(ListView):
# 사용자들이 등록된 모든 사용자 상세 정보 보기 처리
class UserDetailView(DetailView):
# 특정 사용자의 권한을 업데이트
def update_permission(request, pk):
# 특정 사용자의 레벨을 업데이트
def update_level(request, pk):
#  특정 사용자의 정보를 업데이트
def update_user_info(request, pk):
# 특정 사용자의 가입 신청을 거절
def reject_user(request, pk):
# 특정 사용자의 가입 신청을 승인
def approve_user(request, pk):
# 특정 사용자를 탈퇴 처리
def secession_user(request, pk):
```

---

### +a

* **회원 검색 기능**

HTML 부분
```html
<div>
  <form method="GET" action="{% url 'accountapp:user_list' %}">
    <input type="text" name="q" placeholder="이메일 검색">
    <button type="submit">검색</button>
  </form>
</div>
```
Python 부분
```python
class UserListView(ListView):
    model = CustomUser
    template_name = 'user/user_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        queryset = CustomUser.objects.filter(status__in=['A', 'S'])
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(email__icontains=search_query)
        return queryset
```

> get_queryset 메서드는 이 뷰에서 사용할 쿼리셋을 반환합니다. 
> CustomUser 모델의 status 필드가 'A' 또는 'S'인 사용자들만 필터링하여 queryset을 만들고, GET 요청의 'q' 파라미터에 값이 있다면 해당 값을 이용하여 이 queryset을 검색합니다.
> 이 뷰에서는 users라는 컨텍스트 변수를 템플릿에서 사용할 수 있도록 컨텍스트에 추가합니다. 이 변수에는 위에서 구성한 쿼리셋의 결과가 할당됩니다.