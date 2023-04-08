# CEOS 17기 백엔드 스터디

## 참고 사이트
https://inma.tistory.com/88

## 모든 데이터를 가져오는 api 만들기
# error 1) AttributeError: module ‘.views’ has no attribute CommentList
![Untitled (3)](https://user-images.githubusercontent.com/90204371/230721440-e80f2ec0-45ee-43b6-a0e0-9b2d6fc57323.png)
path 명을 제대로 적어주지 않아서 문제가 생긴 것이었다.
https://forum.djangoproject.com/t/django-attributeerror-module-views-has-no-attribute/17241

# error 2) django.db.migrations.exceptions.NodeNotFoundError: Migration 
![Untitled (4)](https://user-images.githubusercontent.com/90204371/230721439-17a6119f-6bd4-42da-9f57-672d1756eea3.png)

migration 에러가 도대체 몇번이나 난건지 ㅠㅅㅠ

그때마다 각 앱에 있는 migration 파일들을 아예 지우고 다시 makemigrations → migrate 를 해줬다. 기존에 migration 파일이 있으면 안되는 것이다. 정현이가 조언해준 덕분에 해결할 수 있었다.
> I had the same problem. It is because of the inconsistent migration history. So I deleted the migrations directory in all installed apps and then called `python manage.py makemigrations` command. The new migrations had no problem.
> 

심지어는 mysql에 있는 eveyrtime 테이블을 아예 지워버리기도 했다. (feat. 현우오빠)

# error 3) django migrate gets error "table already exists"
https://antilibrary.org/911
이 또한 migrations 에러였는데 

> python [manage.py](http://manage.py) migrate —fake <appname>
> 

으로 마치 마이그레이션이 완료된 것처럼 해준다.

# error 4) 404 error
![Untitled (5)](https://user-images.githubusercontent.com/90204371/230721437-cca17258-aa72-48f0-8206-67a34383ccea.png)

아무리 코드를 살펴봐도 잘못된 게 없는데 postman에서 404 에러가 발생했다. 알고보니 url뒤에 enter가 아스키코드 값으로 인식되어 에러가 난 것이었다.. 탁균오빠와 상훈이랑 도합 4시간은 삽질한 것 같다.

오류를 고친 이후에는 아래와 같이 결과가 잘 나타났다.
![Untitled (9)](https://user-images.githubusercontent.com/90204371/230721430-fa5658d9-424b-4b90-97ce-755bcf3a172e.png)
![Untitled (8)](https://user-images.githubusercontent.com/90204371/230721434-788dd9c9-425a-40ab-b5ee-33204d0a6b6e.png)
![Untitled (7)](https://user-images.githubusercontent.com/90204371/230721435-caf504c2-7748-4cc2-8eb0-b5c4d9266b57.png)
![Untitled (6)](https://user-images.githubusercontent.com/90204371/230721436-f9611ca7-2b87-41a3-9101-0ed69cb48c9e.png)

# viewset & filterset
1) viewset 이란?    
- mixins 와 viewsets를 상속받아서 적용  
- 함수를 따로 만들지 않아도 get post 등의 함수가 구현되어 있음
- Mixins 란 : 특정한 클래스에 상속을 통해 기능을 추가하는 것.  
class PostViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):  
    serializer_class = PostSerializer  
    queryset = Post.objects.all()  
    
2) FilterSet 이란?   
> filtering 작업( queryset에서 특정 queryset을 고르는 작업 ) 을 손쉽게 사용하도록 DRF(Django REST Framework)에서 제공하는 속성.  
클라이언트가 접근하는 API url에 붙은 query parameter을 자동으로 필터의 옵션으로 인식하고 필터링을 함.  
>
FilterSet 사용 방법  

- class Meta :  
    - filterable한 모델 정의  
    - 사용할 필드 정의  
    - Disable fields : exclude  
    - Ordering : order_by  
    - Group fields : together 
    
import django_filters  

class PostFilter(django_filters.FilterSet):  
    class Meta:  
        model = Post  
        fields = ['author', 'content', 'upload_date']  
        order_by = ['upload_date']  

## 회고
하면 할 수록 백엔드 flow에 대한 이해도가 높아지는 것 같아서 뿌듯하다. 그리고 회고 쓰는 skill도 향상된 것 같다. 좀 더 가독성있게 쓸 수 있게 되었다.  

그리고 저번에도 띄어쓰기를 해서 인식이 안되는 문제가 있었고 이번에도 enter가 아스키 코드로 해석돼서 안되는 문제가 있었다. 형식 실수를 하면 안되겠구나 하는 걸 뼈저리게 느꼈다 ㅎ 그리고 postman도 파이참 터미널을 보고 에러를 잡아낼 수 있다는 것을 알게 되었다.  



