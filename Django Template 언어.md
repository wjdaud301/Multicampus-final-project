## ## Django 템플릿 언어 정리



Django의 `템플릿 언어`(template language)는 강력함과 편리함 사이의 균형을 잡고자 설계되었다. 템플릿 언어를 사용하면 HTML 작업을 훨씬 수월하게 할 수 있다.

`변수`, `필터`, `태그`, `주석` 등 4가지 기능을 제공한다.



장고 공식 문서에 나와있는 예제

```html
{% extends "base_generic.html" %}

{% block title %}{{ section.title }}{% endblock %}

{% block content %}
<h1>{{ section.title }}</h1>

{% for story in story_list %}
<h2>
  <a href="{{ story.get_absolute_url }}">
    {{ story.headline|upper }}
  </a>
</h2>
<p>{{ story.tease|truncatewords:"100" }}</p>
{% endfor %}
{% endblock %}
```



---



### 1. 템플릿 변수

템플릿 변수를 사용하면 **view에서 template으로 객체를 전달**할 수 있다.

- `{{ 변수 }}`와 같이 생겼다.

- `점(.)`은 변수의 속성에 접근할 때 사용한다.

  위의 예제에서는 `{{ section.title }}` 와 같이 사용했다. view에서 `section` 객체를 html 문서로 보내
  `title`속성을 출력할 수 있도록 지원하는 것이다.
  
  

---



### 2. 템플릿 필터 

템플릿필터는 **변수의 값을 특정 형식으로 변환**할 때 사용한다. 변수 다음에 `파이프(|)`를 넣은 다음 적용하고자 하는 필터를 명시한다.

- **여러 개의 필터를 연속적으로 사용할 수 있다.**

  `{{ text|escape|linebreaks }}`는 text 컨텐츠를 escape한 다음, 행 바꿈을 `<p>` 태그로 바꾸기 위해 종종

  사용되곤 한다.

- **몇몇 필터는 `:` 문자를 통해 인자를 취한다.**

  필터 인자는 `{{ bio|truncatewords:30 }}` 과 같이 사용하는데, 이것은 `bio`변수의 처음 30단어를 보여준다.

  <u>필터 인자에 공백이 포함된 경우에는 반드시 따옴표로 둘러싸야한다.</u>



### default

변수가 false 또는 비어 있는 경우, 지정된 defalut를 사용한다.

```django
{{ value|default:"nothing" }}
```

`value`가 제공되지 않았거나 비어 있는 경우, 위에서는 “`nothing`“을 출력한다.



### length

값의 길이를 반환한다. 문자열과 목록에 대하여 사용할 수 있다.

```django
{{ value|length }}
```

`value`가 `['a', 'b', 'c', 'd']`라면, 결과는 `4`가 된다.



### upper

위의 예제에서 사용한 필터.

```django
{{ story.headline|upper }}
```

'story.headline'의 값을 대문자 형식으로 변환한다.



---



### 3. 템플릿 태그

HTML 자체는 프로그래밍 로직을 구현할 수 없지만, 템플릿 태그를 사용하면 if문, for문처럼 흐름을 제어할 수 있다.

- `{% tag %}` 와 같이 생겼다.
- `{% extends %}`와 같이 단독으로 사용할 수 있는 템플릿 태그들도 있지만, `{% if %}` 처럼 뒤에 `{% endif %}` 템플릿 태그를 **반드시 닫아주어야 하는** 것들도 있다.



### for

배열의 각 원소에 대하여 루프.

```django
<ul>
{% for student in student_list %}
    <li>{{ student.name }}</li>
{% endfor %}
</ul>
```

`student_list`에 들어 있는 선수의 목록을 출력하기 위해 위의 예제처럼 사용할 수 있다.





### if / else

변수가 `true`이면 블록의 컨텐츠를 표시. if 태그 내에 템플릿 필터 및 각종 연산자를 사용할 수 있다.

```django
{% if student_list %}
    총 학생 수 : {{ student_list|length }}
{% else %}
    학생이 없어요!
{% endif %}
```





### block 및 extentds

중복되는 html 파일 내용을 반복해서 작성해야하는 번거로움을 줄여준다. 



---



## 4. 템플릿 코멘트

HTML 문서 상에서 주석이 필요할 때 사용한다.

장고에서는 두 가지 형식의 코멘트 형식을 제공한다.

#### 한 줄

```django
{# 주석 내용 #} 
```

개행 허용되지 않음.

#### 여러 줄

```django
{% comment %}
주석 내용
{% endcomment %}
```

