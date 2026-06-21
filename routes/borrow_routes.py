from flask import Blueprint, request, jsonify
from datetime import date, timedelta
from models import db, Book, BorrowRecord
borrow_bp = Blueprint("borrow_bp", __name__)




@borrow_bp.route('/borrow', methods=['POST'])
def borrow_book():

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body is required"
        }), 400

    borrower_name = data.get("borrower_name")
    borrower_email = data.get("borrower_email")
    book_id = data.get("book_id")

    if not borrower_name or not borrower_email or not book_id:
        return jsonify({
            "success": False,
            "message": "Borrower Name, Borrower Email and Book ID are required"
        }), 400

    book = book = db.session.get(Book, book_id)

    if not book:
        return jsonify({
            "success": False,
            "message": "Book not found"
        }), 404

    if book.available_copies <= 0:
        return jsonify({
            "success": False,
            "message": "Book is currently unavailable"
        }), 400

    borrow = BorrowRecord(
        borrower_name=borrower_name,
        borrower_email=borrower_email,
        borrow_date=date.today(),
        due_date=date.today() + timedelta(days=14),
        book_id=book.id
    )

    book.available_copies -= 1

    db.session.add(borrow)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Book borrowed successfully",
        "borrow": {
            "borrow_id": borrow.id,
            "book": book.title,
            "borrower_name": borrow.borrower_name,
            "borrower_email": borrow.borrower_email,
            "borrow_date": str(borrow.borrow_date),
            "due_date": str(borrow.due_date)
        }
    }), 201

@borrow_bp.route('/return/<int:borrow_id>', methods=['POST'])
def return_book(borrow_id):

    borrow = borrow = db.session.get(BorrowRecord, borrow_id)

    if not borrow:
        return jsonify({
            "success": False,
            "message": "Borrow record not found"
        }), 404

    if borrow.returned:
        return jsonify({
            "success": False,
            "message": "Book already returned"
        }), 400

    book = db.session.get(Book, borrow.book_id)

    borrow.returned = True
    borrow.return_date = date.today()

    book.available_copies += 1

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Book returned successfully",
        "return": {
            "borrow_id": borrow.id,
            "book": book.title,
            "returned_on": str(borrow.return_date),
            "available_copies": book.available_copies
        }
    }), 200

@borrow_bp.route('/borrow-history', methods=['GET'])
def borrow_history():

    records = db.session.query(BorrowRecord).all()

    history = []

    for record in records:

        history.append({
            "borrow_id": record.id,
            "book": record.book.title,
            "borrower_name": record.borrower_name,
            "borrower_email": record.borrower_email,
            "borrow_date": str(record.borrow_date),
            "due_date": str(record.due_date),
            "returned": record.returned,
            "return_date": str(record.return_date) if record.return_date else None
        })

    return jsonify({
        "success": True,
        "count": len(history),
        "history": history
    }), 200

@borrow_bp.route('/overdue', methods=['GET'])
def overdue_books():

    today = date.today()

    overdue = db.session.query(BorrowRecord).filter(
        BorrowRecord.returned == False,
        BorrowRecord.due_date < today
    ).all()

    books = []

    for record in overdue:

        books.append({
            "borrow_id": record.id,
            "book": record.book.title,
            "borrower_name": record.borrower_name,
            "borrower_email": record.borrower_email,
            "borrow_date": str(record.borrow_date),
            "due_date": str(record.due_date)
        })

    return jsonify({
        "success": True,
        "count": len(books),
        "overdue_books": books
    }), 200

@borrow_bp.route('/fine/<int:borrow_id>', methods=['GET'])
def calculate_fine(borrow_id):

    borrow = db.session.get(BorrowRecord, borrow_id)

    if not borrow:
        return jsonify({
            "success": False,
            "message": "Borrow record not found"
        }), 404

    if borrow.returned:
        return jsonify({
            "success": True,
            "message": "Book already returned",
            "fine": 0
        }), 200

    today = date.today()

    if today <= borrow.due_date:
        return jsonify({
            "success": True,
            "late_days": 0,
            "fine": 0
        }), 200

    late_days = (today - borrow.due_date).days

    fine = late_days * 10

    return jsonify({
        "success": True,
        "borrow_id": borrow.id,
        "book": borrow.book.title,
        "borrower": borrow.borrower_name,
        "late_days": late_days,
        "fine": fine
    }), 200

@borrow_bp.route('/dashboard', methods=['GET'])
def dashboard():

    total_books = Book.query.count()

    available_books = db.session.query(
        db.func.sum(Book.available_copies)
    ).scalar() or 0

    borrowed_books = db.session.query(BorrowRecord).filter_by(returned=False).count()

    returned_books = db.session.query(BorrowRecord).filter_by(returned=True).count()

    overdue_books = db.session.query(BorrowRecord).filter(
        BorrowRecord.returned == False,
        BorrowRecord.due_date < date.today()
    ).count()

    return jsonify({
        "success": True,
        "dashboard": {
            "total_books": total_books,
            "available_books": available_books,
            "borrowed_books": borrowed_books,
            "returned_books": returned_books,
            "overdue_books": overdue_books
        }
    }), 200