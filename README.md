# 📚 Library Management API

A RESTful Library Management API built with Flask, SQLAlchemy, and SQLite. It provides book inventory management, borrowing and returning books, overdue tracking, fine calculation, and library dashboard analytics.

## 🚀 Features

* Book CRUD Operations
* Book Borrow & Return
* Borrow History
* Overdue Book Tracking
* Fine Calculation
* Library Dashboard
* ISBN Validation
* Modular Flask Architecture
* RESTful API Design

## 🛠 Tech Stack

* Python
* Flask
* SQLAlchemy
* SQLite

## 📌 API Endpoints

* GET /books
* POST /books
* GET /books/<id>
* PUT /books/<id>
* DELETE /books/<id>
* POST /borrow
* POST /return/<borrow_id>
* GET /borrow-history
* GET /overdue
* GET /fine/<borrow_id>
* GET /dashboard

## ▶️ Run Locally

```bash

Create virtual environment:

python -m venv venv

Activate environment:

.\venv\Scripts\Activate.ps1

Install dependencies:

pip install -r requirements.txt

Run application:

python app.py

Server:

http://127.0.0.1:5000
