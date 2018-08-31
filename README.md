# Django Admin 예쁘게 활용하기

Django Admin 커스터마이징을 통해 Admin 페이지를 예쁘고 효율적으로 활용할 수 있는 방법에 대해 소개하도록 하겠습니다.  
_본 포스팅에는 Django 프로젝트 시작에 관한 내용은 포함하지 않으며, Admin 커스터마이징에 관한 내용만 포함합니다._

# [Django Admin이 뭔가요?](https://docs.djangoproject.com/ko/2.0/intro/tutorial02/#introducing-the-django-admin)
직원들이나 고객들이 컨텐츠의 내용을 수정하기 위한 관리 사이트를 만드는것은 딱히 창의적일 필요없는 지루한 작업입니다. 이런 이유로, Django 는 모델에 대한 관리용 인터페이스를 모두 자동으로 생성합니다.
Django는 사이트 관리자가 컨텐츠를 편집할 수 있는 통합적인 인터페이스를 생성하는 문제를 해결합니다. Admin 사이트는 사이트 방문자를 위한 것이 아니라, 사이트 관리자를 위한 것입니다.

# Admin Customizing
## (1) DataBase 준비하기
저는 서버를 운영하고 있지 않기 때문에 mysql에서 제공하는  employee sample 데이터를 활용하여 Admin 페이지를 커스터마이징 해보겠습니다.  
운영 중인 서버가 있는 독자 분들께서는 운영하고 계신 데이터베이스를 이용하시면 됩니다.  
제가 사용한 Employee data는 [여기](https://dev.mysql.com/doc/employee/en/) 에서 받을 수 있습니다.
<figure>
   <img src="{{ "/img/django_admin/employees-schema.png" | absolute_url }}" />
   <figcaption>Employees schema</figcaption>
</figure>

> **데이터베이스 생성하기**   
> 사전에 mysql이 설치되어 있어야 합니다.  
(1) https://github.com/datacharmer/test_db 레파지토리를 다운받습니다.  
`$ git clone https://github.com/datacharmer/test_db `  
(2) 다운받은 폴더로 이동합니다.  
(3) sql 파일을 통해 데이터 베이스를 생성합니다.  
`$ mysql -u user -p < employees.sql`

## (2) Database 연동 및 모델 생성하기
생성한 mysql 데이터베이스를 Django와 연동을 해야합니다.  
Django 기본 데이터베이스 설정은 SQLite로, settings.py 파일을 보면 아래와 같이 작성되어 있습니다.
```python
# project/settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```
데이터베이스의 설정을 mysql로 변경하도록 하겠습니다.
```python
# project/settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'employees', # 데이터베이스 이름
        'USER': 'root', # 접속 사용자 이름
        'PASSWORD': 'password', # 접속 비밀번호
        'HOST': 'localhost',
        'PORT': '3306', # 기본 포트
    }
}
```
데이터베이스를 연동한 후 모델 파일을 작성해주어야 합니다.  
데이터베이스가 이미 있는 경우(구조, 데이터 포함) 일일히 models.py에 모델을 정의하는게 번거로운 작업일 수 있는데, Django는 `inspectdb` 라는 기능을 제공하여 settings.py에 연결되어 있는 데이터베이스의 구조를 가져와 models.py에 작성할 수 있습니다.
```python
# manage.py가 존재하는 위치에서 명령어 실행
$ python manage.py inspectdb > project/models.py
```
위의 코드 실행 후 models.py 파일을 열어보시면 모델이 정의되어있는 것을 확인할 수 있습니다.

> **models.py 파일 수정**  
> inspectdb 명령어를 통해 생성된 모델을 그대로 사용하면 에러가 발생하기 때문에 Salaries 테이블을 살짝 수정해주었습니다.  
> (1) Salaries 테이블에 자동증가와 primary_key 속성을 가진 id 컬럼을 추가합니다.
```python
# mysql 접속 후
mysql> ALTER TABLE salaries ADD COLUMN id INT NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST;
```
> (2) models.py 파일에 id 속성을 추가합니다.  
>
```python
# models.py 파일
class Salaries(models.Model):
    id = models.AutoField(primary_key=True) # 추가된 속성
    emp_no = models.ForeignKey(Employees, models.DO_NOTHING, db_column='emp_no')
    salary = models.IntegerField()
    from_date = models.DateField()
    to_date = models.DateField()
    class Meta:
        managed = False
        db_table = 'salaries'
        unique_together = (('id', 'emp_no', 'from_date'),)
```

모델의 정의가 완료되었으면 변경 사항을 반영해줍니다.
```python
# manage.py가 존재하는 위치에서 명령어 실행
python manage.py makemigrations app_name
python manage.py migrate app_name
```

## (3) Admin 페이지 꾸미기
Admin 페이지 꾸미기에 앞서 관리자를 먼저 생성해야 합니다.
```python
# manage.py가 존재하는 위치에서 명령어 실행
python manage.py createsuperuser
```
`python manage.py runserver` 로 서버 구동 후, 127.0.0.1:8000/admin 주소에 접속하면 아래의 화면을 볼 수 있습니다.
<figure>
   <img src="{{ "/img/django_admin/admin_login.png" | absolute_url }}" />
   <figcaption>Admin login 화면</figcaption>
</figure>

생성한 관리자로 로그인을 했을 때, 아래와 같은 화면이 나오면 잘 동작하고 있는 것입니다.
<figure>
   <img src="{{ "/img/django_admin/admin_init.png" | absolute_url }}" />
   <figcaption>Admin 첫 화면</figcaption>
</figure>

이제 Admin을 꾸며보도록 하겠습니다.  

### 1. Admin에 모델 등록하기
Admin에 모델을 커스텀하지 않고 등록하는 방법은 아래와 같습니다.
```python
# admin.py
from django.contrib import admin
from .models import * # 모든 모델을 불러옵니다.

admin.site.register(Departments)
admin.site.register(DeptEmp)
admin.site.register(DeptManager)
admin.site.register(Employees)
admin.site.register(Salaries)
admin.site.register(Titles)
```
모델만 등록된 Admin 페이지를 보겠습니다.  
<figure>
   <img src="{{ "/img/django_admin/admin_model.png" | absolute_url }}" />
   <figcaption>Admin에 등록된 모델들</figcaption>
</figure>
<figure>
   <img src="{{ "/img/django_admin/employees_model.png" | absolute_url }}" />
   <figcaption>Employees</figcaption>
</figure>

데이터 가독성이 전혀 없을 뿐만 아니라 보기 좋지 않습니다.  

그러나 이번 포스팅은 어드민 커스텀이 목적이기 때문에 `admin.ModelAdmin` 상속을 통해 커스터마이징 후 등록하도록 하겠습니다.
```python
# admin.py
from django.contrib import admin
from .models import  Employees

class EmployeesAdmin(admin.ModelAdmin):
    list_display = ['emp_no', 'first_name', 'last_name', 'gender', 'birth_date', 'hire_date'] # 커스터마이징 코드

admin.site.register(Departments, DepartmentsAdmin)
```

커스텀 모델을 등록하는 방법을 알았으니, 커스터마이징 옵션에 대해 알아보도록 하겠습니다.

### 2. list_display
list_display는 Admin 사이트에 보여질 필드를 정의하는 옵션입니다.
- list_display 옵션을 따로 지정하지 않으면 각 object의 `__str__()` 값을 보여줍니다.
- 외래키가 설정되어있다면, 관련 object의 `__str__()` 값을 보여줍니다.
- ManyToManyField는 지원하지 않습니다.

list_display 옵션 적용 방법은 아래와 같습니다.
```python
# admin.py
class EmployeesAdmin(admin.ModelAdmin):
    list_display = ['emp_no', 'first_name', 'last_name', 'gender', 'birth_date', 'hire_date']
```
> **list_display_links 옵션**  
> list_display_links 옵션은 링크 기능을 추가할 필드를 지정하는 옵션입니다.  
> 옵션을 지정하지 않으면 첫 번째에 위치하는 필드만 링크(클릭)가 가능합니다.
> list_display_links 옵션 적용 방법은 아래와 같습니다.
> ```python
# admin.py
class EmployeesAdmin(admin.ModelAdmin):
    list_display = ['emp_no', 'first_name', 'last_name', 'gender', 'birth_date', 'hire_date']
    list_display_links = ['emp_no', 'first_name']
```

### 3. list_filter
list_filter는 Admin 사이트에 필터를 활성화할 항목을 설정하는 옵션입니다.
list_filter 옵션은 아래와 같이 tuple 형태로 작성해주어야 합니다.
```python
# admin.py
class EmployeesAdmin(admin.ModelAdmin):
    list_display = ['emp_no', 'first_name', 'last_name', 'gender', 'birth_date', 'hire_date']
    list_filter = ('gender', 'hire_date', 'birth_date',)
```
> **Date range filter 옵션**  
> DateField를 list_filter 옵션에 추가하면 기본적으로 제공되는 필터링 옵션은 아래 4가지 항목입니다.  
- Today
- Past 7 days
- This month
- This year  
>
> 그러나 현실에서는 날짜의 범위를 지정하여 필터링하는 경우가 더 많기 때문에, 기간 설정 필터링을 지원하는 패키지를 설치하여줍니다.  
다양한 date range filter 패키지가 있지만 저는 [django-admin-rangefilter](https://github.com/silentsokolov/django-admin-rangefilter) 를 설치하였습니다.  
>
> 설치 방법은 `pip`를 이용하여 패키지를 설치한 후  `INSTALLED_APPS`에 추가하여주면 됩니다.
```python
# command 창
$ pip install django-admin-rangefilter
```
```python
# settings.py
INSTALLED_APPS = (
    ...
    'rangefilter',
    ...
)
```
> 이용 방법은 아래와 같습니다.  
```python
# admin.py
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter  # 모듈 불러오기
class EmployeesAdmin(admin.ModelAdmin):
    list_display = ['emp_no', 'first_name', 'last_name', 'gender', 'birth_date', 'hire_date']
    list_filter = ('gender',
        ('hire_date', DateRangeFilter),
        ('birth_date', DateRangeFilter),
    )
```

### 4. search_fields
search_fields는 사용자가 입력하는 검색어를 찾을 필드를 지정하는 옵션입니다.  
검색 필드 지정 시, 상단에 검색 바가 활성화되며, 지정된 필드에 사용자 입력 단어가 포함된 행을 보여줍니다.  
search_fields 옵션 적용 방법은 아래와 같습니다.
```python
# admin.py
class EmployeesAdmin(admin.ModelAdmin):
    list_display = ['emp_no', 'first_name', 'last_name', 'gender', 'birth_date', 'hire_date']
    list_filter = ('gender',
        ('hire_date', DateRangeFilter),
        ('birth_date', DateRangeFilter),
    )
    search_fields = ['emp_no', 'first_name', 'last_name']
```

위에서 설명드린 옵션들을 적용한 후 Admin 화면을 보면 훨씬 직관적이고 데이터 검색에 용이하게 화면이 구성되었습니다.
<figure>
   <img src="{{ "/img/django_admin/admin_custom.png" | absolute_url }}" />
   <figcaption>옵션 적용 후 Admin 화면</figcaption>
</figure>

# Admin Styling
위의 단계까지만 적용해도 괜찮지만 이번 포스팅은 Admin 페이지를 예쁘게 꾸미는 것이 목표이므로, 밋밋한 어드민 페이지에 옷을 입혀주도록 하겠습니다.  
이미 Styling 패키지들이 존재하기 때문에 패키지를 설치하고 적용만 해주면 됩니다. 저는 [django-suit](http://djangosuit.com/)를 적용해보도록 하겠습니다.

> **Admin Styling Packages**  
> Django-suit 이외의 다른 패키지들은 [사이트](https://djangopackages.org/grids/g/admin-styling/)를 참고하셔서 본인이 원하는 패키지를 설치하시면 됩니다.  

## 설치방법
### (1) pip를 통해 django-suit를 설치합니다.
공식 문서에서는 stable version(18.08.01 기준 0.2.25버전)을 설치하라고 권장하고 있지만, Django 2.0 버전 이상에서는 stable 버전 설치 시 에러가 발생하기 때문에 저는 최신 버전인 `0.2.26` 버전을 설치하도록 하겠습니다.

```python
# command
$ pip install django-suit==0.2.26
```
### (2) INSTALLED_APPS에 suit를 등록합니다.
`'suit'`를 반드시 `django.contrib.admin'`보다 상위에 등록해야 합니다.  
또한, `django-cms`와 같은  third-party app을 이용중에 있다면 `'suit'`가 상위에 등록되어야 합니다.
```python
# settings.py
INSTALLED_APPS = (
    ...
    'suit',
    'django.contrib.admin',
)
```
### (3) TEMPLATES를 수정합니다.
`Django 1.9` 버전을 기준으로 수정 항목이 조금 다르기 때문에 사용 중인 버전을 확인하시고 수정하시기 바랍니다.
#### Django >= 1.9 버전 사용자
```python
# settings.py
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request', # Make sure you have this line
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```
#### Django < 1.9 버전 사용자
```python
# settings.py
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
)
```
모든 설정을 마치고 난 후 Django-suit가 적용된 화면을 보도록 하겠습니다.
<figure>
   <img src="{{ "/img/django_admin/suit_login.png" | absolute_url }}" />
   <figcaption>suit 적용 후 login 화면</figcaption>
</figure>

<figure>
   <img src="{{ "/img/django_admin/suit_home.png" | absolute_url }}" />
   <figcaption>suit 적용 후 home 화면</figcaption>
</figure>
<figure>
   <img src="{{ "/img/django_admin/suit_employees.png" | absolute_url }}" />
   <figcaption>suit 적용 후 employees 화면</figcaption>
</figure>

위의 모든 과정을 마친 후 Django Admin이 전보다 더 깔끔하고 예뻐진 것을 볼 수 있습니다!  
제가 이번 포스팅에서 소개해드린 것 외에도 Admin에서 사용할 수 있는 기능들이 더 많으니, [Django 공식 문서-admin](https://docs.djangoproject.com/en/2.0/ref/contrib/admin/#customizing-the-adminsite-class)를 참고하셔서 운영중인 시스템에 맞게 잘 커스텀하셔서 사용하시면 될 것 같습니다.
