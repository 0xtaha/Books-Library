from ..models import Review, User

class ReviewModelService:

    @classmethod
    def get_by_book(cls, book):
        return Review.select().where(
            Review.book == book
        ).join(User, on=(Review.user == User.id))
    

    @classmethod
    def get_by_user(cls, user):
        return Review.get_or_none(
            Review.user == user
        )
    
    @classmethod
    def get_by_user_and_book(cls, user, book):
        return Review.get_or_none(
            Review.user == user,
            Review.book == book
        )
    
    @classmethod
    def create(cls, user, book, desc):
        if cls.get_by_user_and_book(user, book):
            return False
        return Review.create(
            user=user,
            book=book,
            desc=desc
        )

