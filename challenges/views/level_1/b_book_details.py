"""
В этом задании вам нужно реализовать функцию get_book, которая по id книги получает саму книгу из БД.
Не забудьте обработать случай, когда указан несуществующий id, тогда функция должна возвращать None,
а не выкидывать исключение.

Чтобы проверить, работает ли ваш код, запустите runserver и сделайте GET-запрос на 127.0.0.1:8000/book/<id книги>/.
Если всё отработало без ошибок и ручка возвращает вам описание книги в json-формате, задание выполнено.
Существующий id книги вы можете взять из предыдущего задания.

Сделать get-запрос вы можете как с помощью Postman, так и просто в браузере.
"""
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseNotFound

from challenges.models import Book


def get_book(book_id: int) -> Book | None:
    try:
        return Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return None

def book_details_handler(request: HttpRequest, book_id: int) -> HttpResponse:
    book = get_book(book_id)

    if book is None:
        return HttpResponseNotFound()

    return JsonResponse({
        "id": book.pk,
        "title": book.title,
        "author_full_name": book.author_full_name,
        "isbn": book.isbn,
    })
