> 출처 : [파이썬/장고 웹서비스 개발 완벽 가이드 with 리액트](https://www.inflearn.com/course/%ED%8C%8C%EC%9D%B4%EC%8D%AC-%EC%9E%A5%EA%B3%A0-%EC%9B%B9%EC%84%9C%EB%B9%84%EC%8A%A4/dashboard) 

> 출처 : 본인 대학교 학과 서버프로그래밍 강의

# 복습 겸 기본 다지기

---

![질문](https://velog.velcdn.com/images/chan9708/post/ba8c13a6-c974-48e5-b543-b49e5b98e047/image.png)

# 웹프레임워크가 왜 필요한가요?

## 우선, 웹서비스가 왜 필요한가요?

웹서비스는 서버의 역할을 합니다.
**모든 서비스의 근간**
: 어떤 서비스이든 웹서비스는 **당연히 잘해야하는 분야**.
: 덜 회자된다고 해서 지나간 유행이 아니다.
: (카카오톡/트위터도 처음에는 Ruby on Rails로 웹베이스로 API 제공)

그렇다면 **웹프레임워크**는 무엇이냐?
: 웹서비스를 만들때마다 반복되는 것들을 표준화해서 묶어놓은 것.
: 거의 모든 언어마다 웹프레임워크가 존재.

---

# 다양한 파이썬 웹프레임워크

![django](https://velog.velcdn.com/images/chan9708/post/212bef5a-6a00-430c-8499-2aa65500e24d/image.png)

## Django

: 백엔드 개발에 필요한 거의 모든 기능을 제공하는, 웹 프로그램을 쉽고 빠르게 만들 수 있는 웹 프레임워크입니다.
: **중복된 작업을 최대한 줄여주는 최고의 프레임워크.**

- **프레임워크** - 애플리케이션 개발에 바탕이 되는 템플릿과 같은 역할을 하는 클래스들과 인터페이스의 집합입니다.

![Flask](https://velog.velcdn.com/images/chan9708/post/10864389-eea8-4e92-b13a-8178e0c18dc8/image.png)

## Flask

: A micro framework
: 백엔드 개발에 필요한 일부분의 기능을 제공한다.
: ORM으로서 SQLAlchemy를 주로 이용

그 외에 Sanic, Tornado가 존재한다.

---

# Django의 강점

1. **Python 생태계**

- 최근에 가장 많이 사용하고 매우 넓은 범위에서 이용되는 대중화된 언어입니다.
- 표현력이 좋고, 가독성이 높은 코드입니다.

2. **건강한 커뮤니티**
3. **_풀스택_ 웹프레임워크**

- 백엔드 개발에 필요한 거의 모든 것을 Django에서 직접 지원합니다.
  - API 개발에 필요한 거의 모든 것을 django-rest-framework에서 지원
- 완결성이 있고 안전합니다.

4. **10년동안 충분히 발전하고 성숙되었습니다.**
5. **확장성이 매우 큽니다.**
6. **유지 보수가 쉬워서 재사용하기 좋습니다.**
7. **다양한 운영체제에서 작동하여 이식성이 좋습니다.**

---

# Django는 MTV 프레임워크

![](https://velog.velcdn.com/images/chan9708/post/5a0cc7a9-e419-4dc5-94a5-031b9565f6fc/image.png)

(이름만 다를 뿐, MVC 입니다. [Model, View, Controller])

- **Model** -> Django의 **Model**
  - 데이터베이스에 저장되는 데이터를 CRUD 하는 부분입니다.
- **View** -> Django의 **Template**
  - 사용자에게 보여지는 UI 부분입니다.
- **Controller** -> Django의 **View**
  - 프로그램의 비즈니스 로직을 구현하여 데이터를 요청 및 가져오고 가져온 데이터를 Template에 전달합니다.
- 해당 다이어그램에는 존재하지 않지만, **URL conf**가 URL를 분석하여 View에 전달합니다.

## MVT 처리과정

1. 클라이언트로 부터 요청을 받으면 URLconf를 이용하여 URL 을 분석합니다.

2. URL 분석 결과를 통해 해당 URL 에 대한 처리를 담당할 View 를 결정합니다.

3. View 는 자신의 로직을 실행 하면서 만일 데이터 베이스 처리가 필요하면 해당 모델에 요청하고 그 결과를 반환을 받습니다.

4. View 는 자신의 로직 처리가 끝나면 Template 을 사용하여 클라이언트에 전송할 HTML 파일을 생성합니다.

5. View 는 최종 결과로 HTML 파일을 클라이언트에 보내어 응답을 보냅니다.

---

## MVT 패턴 코드 작성하는 순서

### 1. 프로젝트 뼈대를 세웁니다.

- 프로젝트 및 앱 개발에 필요한 디렉토리와 파일 생성합니다.

### 2. Model 코딩합니다.

- 테이블 관련 사항을 개발합니다. **<span style='background-color: #fff5b1'>(models.py, admin.py)</span>**

### 3. URLconf 코딩합니다.

- URL 및 View 매핑 관계를 정의합니다. **<span style='background-color: #fff5b1'>(urls.py 파일)</span>**

### 4. template 코딩합니다.

- 화면 UI를 개발합니다. **<span style='background-color: #fff5b1'>(templates/ 디렉토리 하위의 \*.html 파일)</span>**

### 5. View 코딩합니다.

- 애플리케이션 로직 개발합니다. **<span style='background-color: #fff5b1'>(views.py 파일)</span>**

---

# 마무리 및 당부의 말씀

![](https://velog.velcdn.com/images/chan9708/post/55391556-b203-4a26-b3f7-d52aa4a153cc/image.png)

## 백엔드는 서비스의 중심이다.

> 보기 좋은 떡이 먹기에도 좋다고, 프론트에 대한 열망은 숨길 수 없다.
> 하지만, 일에도 순서가 있다.
> **백엔드는 서비스의 중심이다.**
> **백엔드/서비스운영**을 **먼저** 탄탄하게 하고, 그 후에 프론트/앱을 고민하는 것이 순서이다.
