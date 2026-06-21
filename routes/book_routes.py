from flask import Blueprint, request, jsonify
from models import db, Book

book_bp = Blueprint("book_bp", __name__)

#get_books
@book_bp.route('/books', methods=['GET'])
def get_books():

    books = Book.query.all()

    result = []

    for book in books:
        result.append({
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "year": book.year,
            "genre": book.genre,
            "isbn": book.isbn,
            "total_copies": book.total_copies,
            "available_copies": book.available_copies
        })

    return jsonify({
    "success": True,
    "count" : len(result),
    "books": result
    }
), 200


# Add Book
@book_bp.route('/books', methods=['POST'])
def add_book():

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body is required"
        }), 400

    title = data.get("title")
    author = data.get("author")
    genre = data.get("genre")
    isbn = data.get("isbn")
    year = data.get("year")
    total_copies = data.get("total_copies")

    if not all([title, author, genre, isbn]):
        return jsonify({
            "success": False,
            "message": "Title, author, genre and ISBN are required"
        }), 400

    if year is None or total_copies is None:
        return jsonify({
            "success": False,
            "message": "Year and Total Copies are required"
        }), 400

    if not isinstance(year, int):
        return jsonify({
            "success": False,
            "message": "Year must be an integer"
        }), 400

    if not isinstance(total_copies, int):
        return jsonify({
            "success": False,
            "message": "Total Copies must be an integer"
        }), 400

    if year <= 0:
        return jsonify({
            "success": False,
            "message": "Invalid year"
        }), 400

    if total_copies <= 0:
        return jsonify({
            "success": False,
            "message": "Total Copies must be greater than 0"
        }), 400

    existing_book = Book.query.filter_by(isbn=isbn).first()

    if existing_book:
        return jsonify({
            "success": False,
            "message": "Book with this ISBN already exists"
        }), 409

    new_book = Book(
        title=title,
        author=author,
        genre=genre,
        isbn=isbn,
        year=year,
        total_copies=total_copies,
        available_copies=total_copies
    )

    db.session.add(new_book)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Book added successfully",
        "book": {
            "id": new_book.id,
            "title": new_book.title,
            "author": new_book.author,
            "genre": new_book.genre,
            "isbn": new_book.isbn,
            "year": new_book.year,
            "total_copies": new_book.total_copies,
            "available_copies": new_book.available_copies
        }
    }), 201


# Get Single Book
@book_bp.route('/books/<int:id>', methods=['GET'])
def get_book(id):

    book = db.session.get(Book, id)

    if not book:
        return jsonify({
            "success": False,
            "message": "Book not found"
        }), 404

    return jsonify({
        "success": True,
        "book": {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "year": book.year,
        }
    }), 200


# Update Book
@book_bp.route('/books/<int:id>', methods=['PUT'])
def update_book(id):

    book = db.session.get(Book, id)

    if not book:
        return jsonify({
            "success": False,
            "message": "Book not found"
        }), 404

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body is required"
        }), 400

    title = data.get("title")
    author = data.get("author")
    genre = data.get("genre")
    isbn = data.get("isbn")
    year = data.get("year")
    total_copies = data.get("total_copies")

    if not all([title, author, genre, isbn]):
        return jsonify({
            "success": False,
            "message": "Title, Author, Genre and ISBN are required"
        }), 400

    if year is None or total_copies is None:
        return jsonify({
            "success": False,
            "message": "Year and Total Copies are required"
        }), 400

    if not isinstance(year, int):
        return jsonify({
            "success": False,
            "message": "Year must be an integer"
        }), 400

    if not isinstance(total_copies, int):
        return jsonify({
            "success": False,
            "message": "Total Copies must be an integer"
        }), 400

    if total_copies <= 0:
        return jsonify({
            "success": False,
            "message": "Total Copies must be greater than 0"
        }), 400

    existing_book = Book.query.filter_by(isbn=isbn).first()

    if existing_book and existing_book.id != id:
      return jsonify({
        "success": False,
        "message": "Another book with this ISBN already exists"
    }), 409

    borrowed = book.total_copies - book.available_copies

    if total_copies < borrowed:
        return jsonify({
            "success": False,
            "message": f"Cannot reduce total copies below borrowed copies ({borrowed})"
        }), 400

    book.title = title
    book.author = author
    book.genre = genre
    book.isbn = isbn
    book.year = year
    book.total_copies = total_copies
    book.available_copies = total_copies - borrowed

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Book updated successfully",
        "book": {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "genre": book.genre,
            "isbn": book.isbn,
            "year": book.year,
            "total_copies": book.total_copies,
            "available_copies": book.available_copies
        }
    }), 200


# Delete Book
@book_bp.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):

    book = db.session.get(Book, id)

    if not book:
        return jsonify({
            "success": False,
            "message": "Book not found"
        }), 404

    db.session.delete(book)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Book deleted successfully"
    }), 200


