"""
В этом задании вам предстоит работать с моделью ноутбука. У него есть бренд (один из нескольких вариантов),
год выпуска, количество оперативной памяти, объём жесткого диска, цена, количество этих ноутбуков на складе
и дата добавления.

Ваша задача:
- создать соответствующую модель (в models.py)
- создать и применить миграцию по созданию модели (миграцию нужно добавить в пул-реквест)
- заполнить вашу локальную базу несколькими ноутбуками для облегчения тестирования
  (я бы советовал использовать для этого shell)
- реализовать у модели метод to_json, который будет преобразовывать объект ноутбука в json-сериализуемый словарь
- по очереди реализовать каждую из вьюх в этом файле, проверяя правильность их работу в браузере
"""
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from challenges.models import Laptop
from http import HTTPStatus

def laptop_details_view(request: HttpRequest, laptop_id: int) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть json-описание ноутбука по его id.
    Если такого id нет, вернуть 404.
    """
    try:
        laptop = Laptop.objects.get(id=laptop_id)
    except Laptop.DoesNotExist:
        return HttpResponseNotFound()
    return HttpResponse(laptop.to_json(), content_type="application/json")


def laptop_in_stock_list_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть json-описание всех ноутбуков, которых на складе больше нуля.
    Отсортируйте ноутбуки по дате добавления, сначала самый новый.
    """
    laptops = Laptop.objects.filter(quantity__gt=0).order_by('-created_at')
    data = '[]'
    if laptops:
        data = f"[{','.join([laptop.to_json() for laptop in laptops])}]"
    return HttpResponse(data, content_type="application/json")


def laptop_filter_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть список ноутбуков с указанным брендом и указанной минимальной ценой.
    Бренд и цену возьмите из get-параметров с названиями brand и min_price.
    Если бренд не входит в список доступных у вас на сайте или если цена отрицательная, верните 403.
    Отсортируйте ноутбуки по цене, сначала самый дешевый.
    """
    allowed_brands = [brand[0] for brand in Laptop._meta.get_field("brand").choices]
    brand = request.GET.get('brand')
    min_price = request.GET.get('min_price', -1)
    if not all([brand in allowed_brands, int(min_price) >= 0]):
        return HttpResponse('', status=HTTPStatus.FORBIDDEN, content_type="application/json")
    laptops = Laptop.objects.filter(brand=brand, price__gte=min_price).order_by('price')
    data = '[]'
    if laptops:
        data = f"[{','.join([laptop.to_json() for laptop in laptops])}]"
    return HttpResponse(data, content_type="application/json")

def last_laptop_details_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть json-описание последнего созданного ноутбука.
    Если ноутбуков нет вообще, вернуть 404.
    """
    laptop = Laptop.objects.last()
    if laptop:
        return HttpResponse(laptop.to_json(), content_type="application/json")
    return HttpResponseNotFound()
