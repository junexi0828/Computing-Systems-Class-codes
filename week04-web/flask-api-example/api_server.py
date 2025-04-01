from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 크로스 오리진 요청 허용

# 간단한 데이터베이스 역할을 하는 리스트
books = [
    {'id': 1, 'title': '파이썬 프로그래밍', 'author': '김파이', 'year': 2021},
    {'id': 2, 'title': '웹 개발의 기초', 'author': '이웹돌', 'year': 2022},
    {'id': 3, 'title': '플라스크 마스터', 'author': '박플라', 'year': 2023},
    {'id': 4, 'title': '웹 프로그래밍', 'author': '최성철', 'year': 2023}

]

# 모든 책 정보를 반환하는 API 엔드포인트
@app.route('/api/books', methods=['GET'])
def get_books():
    return jsonify(books)

@app.route('/', methods=['GET'])
def index():
    return "Hello, World!"

# 특정 ID의 책 정보를 반환하는 API 엔드포인트
@app.route('/api/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = next((book for book in books if book['id'] == book_id), None)
    if book:
        return jsonify(book)
    return jsonify({'error': '책을 찾을 수 없습니다.'}), 404

# 새 책을 추가하는 API 엔드포인트
@app.route('/api/books', methods=['POST'])
def add_book():
    if not request.json or 'title' not in request.json:
        return jsonify({'error': '유효하지 않은 데이터입니다.'}), 400
    
    # 새 책의 ID 생성 (현재 최대 ID + 1)
    new_id = max(book['id'] for book in books) + 1
    
    book = {
        'id': new_id,
        'title': request.json['title'],
        'author': request.json.get('author', ''),
        'year': request.json.get('year', 0)
    }
    
    books.append(book)
    return jsonify(book), 201

# 책 정보를 수정하는 API 엔드포인트
@app.route('/api/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = next((book for book in books if book['id'] == book_id), None)
    if not book:
        return jsonify({'error': '책을 찾을 수 없습니다.'}), 404
    
    if not request.json:
        return jsonify({'error': '유효하지 않은 데이터입니다.'}), 400
    
    book['title'] = request.json.get('title', book['title'])
    book['author'] = request.json.get('author', book['author'])
    book['year'] = request.json.get('year', book['year'])
    
    return jsonify(book)

# 책을 삭제하는 API 엔드포인트
@app.route('/api/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = next((book for book in books if book['id'] == book_id), None)
    if not book:
        return jsonify({'error': '책을 찾을 수 없습니다.'}), 404
    
    books.remove(book)
    return jsonify({'result': True})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) #localhost:5000
