from flask import Blueprint, request

from src.models import Book,books_schema
from src import db

book_api = Blueprint("book_api", __name__, url_prefix="/books")

class BookException(Exception):
    def __init__(self, message, code=400):
        self.message = message
        self.code = code

@book_api.errorhandler(BookException)
def invalid_book(e):
    return {"error": "Invalid Insertion of Book: {e}"}, 405

@book_api.route("/", methods=["POST"])
def create_book():
    data = request.json
    if isinstance(data, dict):
        data = [data]
    
    for items in data:
        author_id = items.get("author_id")
        title = items.get("title")
        cover_image = items.get("cover_image")
        pages = items.get("pages")
        releaseDate = items.get("release_date")
        isbn = items.get("isbn")

        try:
            book = Book(
                author_id=author_id,
                title=title,
                cover_image=cover_image,
                pages=pages,
                releaseDate=releaseDate,
                isbn=isbn,
            )
            db.session.add(book)
        except BookException as e:
            db.session.rollback()
            return {"error": str(e)}, 500
    db.session.commit()

    return {
        "message": "book has been added successfully"
    }



