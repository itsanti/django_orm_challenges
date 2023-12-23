"""
В этом задании вам предстоит работать с моделью поста в блоге. У него есть название, текст, имя автора, статус
(опубликован/не опубликован/забанен), дата создания, дата публикации, категория (одна из нескольких вариантов).

Ваша задача:
- создать соответствующую модель (в models.py)
- создать и применить миграцию по созданию модели (миграцию нужно добавить в пул-реквест)
- заполнить вашу локальную базу несколькими ноутбуками для облегчения тестирования
- реализовать у модели метод to_json, который будет преобразовывать объект книги в json-сериализуемый словарь
- по очереди реализовать каждую из вьюх в этом файле, проверяя правильность их работу в браузере
"""
from django.http import HttpRequest, HttpResponse
from challenges.models import Post
from datetime import datetime, timedelta


def last_posts_list_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть 3 последних опубликованных поста.
    """
    posts = Post.objects.order_by('-published_at')[:3]
    data = '[]'
    if posts:
        data = f"[{','.join([post.to_json() for post in posts])}]"
    return HttpResponse(data, content_type="application/json")


def posts_search_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть все посты, которые подходят под поисковый запрос.
    Сам запрос возьмите из get-параметра query.
    Подходящесть поста можете определять по вхождению запроса в название или текст поста, например.
    """
    query = request.GET.get('query')
    data = '[]'
    if query:
        posts = Post.objects.filter(title__icontains=query) | Post.objects.filter(text__icontains=query)
        data = f"[{','.join([post.to_json() for post in posts])}]"
    return HttpResponse(data, content_type="application/json")

def untagged_posts_list_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть все посты без категории, отсортируйте их по автору и дате создания.
    """
    posts = Post.objects.filter(category__exact='').order_by('author', '-created_at')
    data = '[]'
    if posts:
        data = f"[{','.join([post.to_json() for post in posts])}]"
    return HttpResponse(data, content_type="application/json")


def categories_posts_list_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть все посты все посты, категория которых принадлежит одной из указанных.
    Возьмите get-параметр categories, в нём разделённый запятой список выбранных категорий.
    """
    categories = request.GET.get('categories', '').upper()
    categories = set(filter(lambda cat: cat in Post.Category.values, categories.split(',')))
    posts = Post.objects.filter(category__in=categories)
    data = '[]'
    if posts:
        data = f"[{','.join([post.to_json() for post in posts])}]"
    return HttpResponse(data, content_type="application/json")


def last_days_posts_list_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть посты, опубликованные за последние last_days дней.
    Значение last_days возьмите из соответствующего get-параметра.
    """
    last_days = int(request.GET.get('last_days', 0))
    posts = Post.objects.filter(status=Post.Status.PUBLISHED,
                                published_at__gte=datetime.now()-timedelta(days=last_days))
    data = '[]'
    if posts:
        data = f"[{','.join([post.to_json() for post in posts])}]"
    return HttpResponse(data, content_type="application/json")
