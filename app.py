from flask import Flask, jsonify, request
from models import db, Book, BorrowRecord
from datetime import date, timedelta
from config import Config
from routes.book_routes import book_bp
from routes.borrow_routes import borrow_bp

app = Flask(__name__)

# Database Configuration
app.config.from_object(Config)

db.init_app(app)
app.register_blueprint(book_bp)
app.register_blueprint(borrow_bp)

# Home Route
@app.route('/')
def home():
    return jsonify({
        "success": True,
        "message": "Library Management API is Running!"
    })


# Create Database Tables
with app.app_context():
    db.create_all()


# Run Flask App
if __name__ == '__main__':
    app.run(debug=True)