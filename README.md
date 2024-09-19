# SIBI

---


# 프로젝트 이름
스파르타 뉴스

## 📖 목차
1. [프로젝트 소개](#프로젝트-소개)
2. [팀소개](#팀소개)
3. [프로젝트 계기](#프로젝트-계기)
4. [주요기능](#주요기능)
5. [개발기간](#개발기간)
6. [기술스택](#기술스택)
7. [서비스 구조](#서비스-구조)
8. [와이어프레임](#와이어프레임)
9. [API 명세서](#API-명세서)
10. [ERD](#ERD)
11. [프로젝트 파일 구조](#프로젝트-파일-구조)
12. [Trouble Shooting](#trouble-shooting)
    
## 👨‍🏫 프로젝트 소개
IT 뉴스링크와 관련 글을 올릴 수 있는 뉴스 서비스입니다.


## 팀소개
    - 팀명:  시비조
    - 팀원:  조준호, 김영빈, 김채림, 박연재
    - github: https://github.com/duswo3o/SIBI

## 프로젝트 계기


## 💜 주요기능

- 기능 1
  - 회원가입을 하기 위해서는 username, password, email, first_name, last_name, brithday이 필수적으로 입력되어야 합니다
  - 회원인 유저는 게시글 작성 및 수정, 삭제가 가능합니다
  - 회원인 유저는 게시글에 댓글 작성 및 수정 삭제가 가능합니다
  - 회원인 유저는 게시글과 댓글에 좋아요를 누를 수 있습니다
  - 회원인 유저는 다른 유저를 팔로우 할 수 있습니다

- 기능 2
  - 작성
    - 게시글 작성은 제목과 내용을 필수적으로 포함해야 하며 이미지와 해시태그는 선택적으로 포함할 수 있습니다
    - 댓글 작성에는 내용을 필수적으로 포함해야 합니다
  - 조회
    - 게시글 조회는 모든 사람이 가능합니다
  - 수정 및 삭제
    - 본인이 작성한 게시글 및 댓글만 수정, 삭제가 가능합니다

- 기능 3
  - 네이버 기사의 url을 입력하면 해당 기사를 요약해줍니다
  - 네이버 기사의 headline 뉴스의 요약된 내용을 제공합니다
    - 매일 11시에 크롤링되는 기사를 보여줍니다
    - 보여주는 헤드라인 기사는 5개입니다

- 기능 4


## ⏲️ 개발기간
- 2024.09.11(수) ~ 2024.09.19(목)

## 📚️ 기술스택

### ✔️ Language

    ● python

### ✔️ Version Control

    ● Git
    ● GitHub

### ✔️ IDE

    ● Visual Studio Code
    ● PyCharm

### ✔️ Framework

    ● Django


### ✔️  DBMS

      ● SQLite3

### ✔️ COMMUNICATION

      ● slack
      ● zep
      ● notion


## 서비스 구조



## 와이어프레임

![image](readme-img/wireframe.png)

## API 명세서

- [SIBI_news 명세서](https://www.notion.so/teamsparta/8f9ba157cb8646d7a90c0d1827347c28?v=6d56ff1742c641789351681daa5daf0b&pvs=4)

## ERD

![img](readme-img/spartanews_erd.png)

## 프로젝트 파일 구조

```
📦 
├─ README.md
├─ SIBI_NEWS
│  ├─ __init__.py
│  ├─ asgi.py
│  ├─ settings.py
│  ├─ urls.py
│  └─ wsgi.py
├─ accounts
│  ├─ __init__.py
│  ├─ admin.
│  ├─ apps.py
│  ├─ migrations
│  │  ├─ 0001_initial.py
│  │  └─ __init__.py
│  ├─ models
│  ├─ serializers.py
│  ├─ tests.py
│  ├─ urls.py
│  ├─ validators.py
│  └─ views.py
├─ headline_crawling.py
├─ manage.py
├─ media
│  └─ images
│     ├─ pngwing.com_9.png
│     ├─ pngwing.com_9_JjSePaS.png
│     ├─ pngwing.com_9_YrpN9ne.png
│     └─ pngwing.com_9_kMyzdKD.png
├─ openai_test.py
├─ posts
│  ├─ __init__.py
│  ├─ adm
│  ├─ apps.py
│  ├─ crawling.py
│  ├─ migrations
│  │  ├─ 0001_initial.py
│  │  └─ __init__.py
│  ├─ models.
│  ├─ serializers.py
│  ├─ tests.py
│  ├─ urls.py
│  ├─ validators.py
│  └─ views.py
└─ requirements.txt
```
©generated by [Project Tree Generator](https://woochanleee.github.io/project-tree-generator)


## Trouble Shooting
