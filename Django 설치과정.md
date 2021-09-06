## AWS EC2 :: Django 설치 및 실행



```sh
# django 설치
$ pip install django
```



```sh
# project 생성
$ django-admin startproject [프로젝트 이름:OJO]
```



```sh
# settings.py에서 셋팅

$ vi ./mysite/settings.py  // open settings.py file 

...
ALLOWED_HOSTS = ['*']
...

TIME_ZONE = 'Asia/Seoul
```



브라우저에서 접근하기 전 EC2의 보안 정책에서 8000번 포트를 열어 주어야한다.

```sh
$ python manage.py runserver 0.0.0.0:8000
```



#### VScode 확인

VSCode에 python 플러그인을 설치한 후 확인

