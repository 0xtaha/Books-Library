from ..models import Book

class BookModelServices:

    @classmethod
    def get_all(cls, page, psize):
        query = Book.select()
        print(query)
        total_books_count = query.count()
        query = query.paginate(page, psize)
        return total_books_count, query
    

    @classmethod
    def get_by_id(cls, book_id):
        return Book.get_or_none(Book.id == book_id)
        