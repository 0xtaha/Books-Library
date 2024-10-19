import datetime
from flask import request
from ....connections_handeller import RedisConnector
from flask_restx import abort
from ...support.security import get_identity
from ...support import exceptions
from ....models_services.book_model_services import BookModelServices as Book
from ....models_services.review_model_services import ReviewModelService as Review
from ....models_services.user_model_services import UserModelServices as User
from ....default_config import DefaultConfig

class BookServices:

    @classmethod
    def get_list(cls, args):
        if args['page_size'] > 200 :
            abort(400, 'Page size is too big')
        if args['page_number'] < 0:
            abort(400, "page number cannot be lower than 0")
        
        count, books = Book.get_all(page=args['page_number'], psize=args['page_size'])
        return { 
            'total_count' : count,
            'books' : [book.serialize() for book in books]
            }
    
    @classmethod
    def get_book(cls, book_id):
        book = Book.get_by_id(book_id)
        if not book:
            abort(400, 'Invalied Book ID')
        return book.serialize()

    @classmethod
    def get_book_reviews(cls, book_id):
        book = Book.get_by_id(book_id)
        if not book:
            abort(400, 'Book Invalied')
            
        reviews = Review.get_by_book(book)
        return [review.serialize() for review in reviews]
    
    @classmethod
    def get_book_content(cls, book_id):
        book = Book.get_by_id(book_id)
        if not book:
            abort(400, 'Book Invalied')
        return book.serialize_with_content()
    
    @classmethod
    def create_review_on_book(cls, user_id, book_id, desc):
        book = Book.get_by_id(book_id)
        if not book:
            abort(400, 'Book Invalied')
        
        user = User.get_user_by_id(user_id)
        if not user:
            abort(400, 'User Invalied')
        old_review = Review.get_by_user_and_book(user=user, book=book)
        if old_review:
            abort(400, 'User has a review on this Book, cannot add a new one')
        
        if not Review.create(
            book=book,
            user=user,
            desc=desc
        ) :
            abort(400, 'user cannot add more than one review on the same book')
        return {
            'status' : 'created'
        }

    @classmethod
    def get_book_and_reviews(cls, book_id):
        book_dict = cls.get_book(book_id)
        book_dict['reviews'] = cls.get_book_reviews(book_id)
        return book_dict