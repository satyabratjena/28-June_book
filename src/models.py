from src import db
from dataclasses import dataclass
from marshmallow import Schema, fields

@dataclass
class Book(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    author_id: int = db.Column(db.Integer, nullable=True)
    title: str = db.Column(db.String(100), nullable=False)
    cover_image: str = db.Column(db.String(100), nullable=True)
    pages: int = db.Column(db.Integer, nullable=False)
    releaseDate: str = db.Column(db.String(100), nullable=False)
    isbn: str = db.Column(db.String(100), nullable=True)

class BookSchema(Schema):
    class Meta:
        fields = ("author_id", "title", "cover_image", "pages", "releaseDate", "isbn")

books_schema = BookSchema()

# class PostBookSchema(BookSchema):
#     cka