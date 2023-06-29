# Below are install imports
from flask import Blueprint, request, url_for
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

# Below are Custom error
from src.models import Book,BookSchema
from src import db

book_api = Blueprint("book_api", __name__, url_prefix="/books")

# Below are some custom error handlers
class BookException(Exception):
    def __init__(self, message, code=400):
        self.message = message
        self.code = code

class InvalidException(Exception):
    def __init__(self, message, code=400):
        self.message = message
        self.code = code

@book_api.errorhandler(BookException)
def invalid_book(e):
    return {"error": "Invalid Insertion of Book: {e}"}, 405

@book_api.errorhandler(InvalidException)
def error_invalid_book(e):
    return {"error": "Invalid data: {e}"}, 405

@book_api.route("/", methods=["GET"])
@book_api.route("/<book_id>", methods=["GET"])
def get_books(book_id=None):
    title = request.args.get("title")
    author_id = request.args.get("author_id")
    releaseDate = request.args.get("release_date")
    sort = request.args.get("sort", "title")
    order = request.args.get("order", "asc")
    page = request.args.get("page",default=1, type=int)
    limit = request.args.get("limit", default=3, type=int)

    query = Book.query

    if book_id:
        query = query.filter(Book.id == book_id)
        if not query:
            raise BookException(f"{id} id doesn't exist")
    
    query = query.order_by(getattr(getattr(Book, sort),order)())

    if title:
        title = title.capitalize()
        query = query.filter(Book.title.startswith("title"))
    if author_id:
        query = query.filter(Book.author.ilike("author_id"))
    if releaseDate:
        query = query.filter(Book.releaseDate == releaseDate)

    books = query.pagination(page=page, limit=limit, error_out=False)

    schema = BookSchema(many=True)
    show_book_schemas = schema.dump(books)

    if books.has_next:
        next_page = url_for("book_api.get_books", page=books.next_num, external=True)
    else:
        next_page = None

    return {
        "books": show_book_schemas,
        "total_books": books.total,
        "page": books.page,
        "next_page": next_page
    }, 200

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
        releaseDate = items.get("releaseDate")
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

@book_api.route("/", methods=["PUT"])
@book_api.route("/<book_id>", methods=["PUT"])
def update_books(book_id):

    book_data = Book.query.filter_by(book_id=id).first()
    
    if not book_data:
        raise InvalidException
    book_data.author_id = book_data.author_id or request.json.get('author_id')
    book_data.title = book_data.title or request.json.get('title')
    book_data.cover_image = book_data.cover_image or request.json.get('cover_image')
    book_data.pages = book_data.pages or request.json.get('pages')
    book_data.releaseDate = book_data.releaseDate or request.json.get('releaseDate')
    book_data.isbn = book_data.isbn or request.json.get('isbn')

    db.session.add(book_data)
    db.session.commit()

    return {"status": True, "message": f" {book_id} ID got updated successfully"}


@book_api.route("/", methods=["DELETE"])
@book_api.route("/<book_id>", methods=["DELETE"])
def delete_books(book_id):
    book_data = Book.query.filter_by(id=book_id).first()

    if not book_data:
        raise InvalidException
    db.session.delete(book_data)
    db.session.commit()

    return {"status": True, "message": "The deletion of Id was successful"}