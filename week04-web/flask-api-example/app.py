from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 간단한 도서 데이터베이스 (메모리)
books = [
    {"id": 1, "title": "파이썬 프로그래밍", "author": "홍길동", "year": 2020},
    {"id": 2, "title": "웹 개발의 기초", "author": "김철수", "year": 2021}
]

@app.route('/api/books', methods=['GET'])
def get_books():
    return jsonify(books)

@app.route('/api/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = next((book for book in books if book['id'] == book_id), None)
    if book is None:
        return jsonify({"error": "도서를 찾을 수 없습니다."}), 404
    return jsonify(book)

@app.route('/api/books', methods=['POST'])
def create_book():
    if not request.json or 'title' not in request.json:
        return jsonify({"error": "제목이 필요합니다."}), 400
    
    book = {
        'id': books[-1]['id'] + 1 if books else 1,
        'title': request.json['title'],
        'author': request.json.get('author', ''),
        'year': request.json.get('year', 2024)
    }
    books.append(book)
    return jsonify(book), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 