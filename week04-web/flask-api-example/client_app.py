from flask import Flask, render_template, request, redirect, url_for
import requests
import json

app = Flask(__name__)

# API 서버 주소
API_URL = 'http://localhost:5000/api'

@app.route('/')
def index():
    # API 서버에서 모든 책 정보 가져오기
    response = requests.get(f'{API_URL}/books')
    books = response.json()
    
    # 템플릿에 책 데이터 전달하여 렌더링
    return render_template('index.html', books=books)

@app.route('/book/<int:book_id>')
def book_detail(book_id):
    # API 서버에서 특정 책 정보 가져오기
    response = requests.get(f'{API_URL}/books/{book_id}')
    book = response.json()
    
    if 'error' in book:
        return render_template('error.html', message=book['error'])
    
    # 템플릿에 책 데이터 전달하여 렌더링
    return render_template('book_detail.html', book=book)

@app.route('/book/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        # 폼 데이터 가져오기
        title = request.form.get('title')
        author = request.form.get('author')
        year = request.form.get('year', type=int)
        
        # API 서버에 새 책 추가 요청
        book_data = {'title': title, 'author': author, 'year': year}
        response = requests.post(
            f'{API_URL}/books',
            headers={'Content-Type': 'application/json'},
            data=json.dumps(book_data)
        )
        
        if response.status_code == 201:
            # 책 추가 성공 시 메인 페이지로 리다이렉트
            return redirect(url_for('index'))
        else:
            # 에러 발생 시 에러 페이지 표시
            return render_template('error.html', message='책을 추가하는 데 실패했습니다.')
    
    # GET 요청이면 책 추가 폼 표시
    return render_template('add_book.html')

@app.route('/book/edit/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    if request.method == 'POST':
        # 폼 데이터 가져오기
        title = request.form.get('title')
        author = request.form.get('author')
        year = request.form.get('year', type=int)
        
        # API 서버에 책 수정 요청
        book_data = {'title': title, 'author': author, 'year': year}
        response = requests.put(
            f'{API_URL}/books/{book_id}',
            headers={'Content-Type': 'application/json'},
            data=json.dumps(book_data)
        )
        
        if response.status_code == 200:
            # 책 수정 성공 시 해당 책 상세 페이지로 리다이렉트
            return redirect(url_for('book_detail', book_id=book_id))
        else:
            # 에러 발생 시 에러 페이지 표시
            return render_template('error.html', message='책을 수정하는 데 실패했습니다.')
    
    # GET 요청이면 현재 책 정보 가져와서 수정 폼 표시
    response = requests.get(f'{API_URL}/books/{book_id}')
    book = response.json()
    
    if 'error' in book:
        return render_template('error.html', message=book['error'])
    
    return render_template('edit_book.html', book=book)

@app.route('/book/delete/<int:book_id>')
def delete_book(book_id):
    # API 서버에 책 삭제 요청
    response = requests.delete(f'{API_URL}/books/{book_id}')
    
    if response.status_code == 200:
        # 책 삭제 성공 시 메인 페이지로 리다이렉트
        return redirect(url_for('index'))
    else:
        # 에러 발생 시 에러 페이지 표시
        return render_template('error.html', message='책을 삭제하는 데 실패했습니다.')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001) 