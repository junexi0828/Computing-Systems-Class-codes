from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # 세션 관리를 위한 시크릿 키

# 데이터베이스 초기화
def init_db():
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    
    # 사용자 테이블 생성
    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # 포스트 테이블 생성
    c.execute('''
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        user_id INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
    # 댓글 테이블 생성
    c.execute('''
    CREATE TABLE IF NOT EXISTS comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT NOT NULL,
        post_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (post_id) REFERENCES posts (id),
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
    conn.commit()
    conn.close()

# 데이터베이스 연결 함수
def get_db_connection():
    conn = sqlite3.connect('blog.db')
    conn.row_factory = sqlite3.Row  # 딕셔너리 형태로 결과 반환
    return conn

# 사용자 인증 관련 함수
def is_logged_in():
    return 'user_id' in session

# 사용자 이름 가져오기
def get_username(user_id):
    conn = get_db_connection()
    user = conn.execute('SELECT username FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    return user['username'] if user else None

# 메인 페이지
@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('''
        SELECT p.id, p.title, p.content, p.created_at, u.username 
        FROM posts p JOIN users u ON p.user_id = u.id
        ORDER BY p.created_at DESC
    ''').fetchall()
    conn.close()
    
    return render_template('index.html', posts=posts, is_logged_in=is_logged_in())

# 사용자 등록
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        # 비밀번호 해싱
        hashed_password = generate_password_hash(password)
        
        conn = get_db_connection()
        try:
            conn.execute(
                'INSERT INTO users (username, password, email) VALUES (?, ?, ?)',
                (username, hashed_password, email)
            )
            conn.commit()
            flash('회원가입이 완료되었습니다. 로그인해주세요.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('이미 사용 중인 사용자 이름 또는 이메일입니다.', 'danger')
        finally:
            conn.close()
    
    return render_template('register.html')

# 로그인
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('로그인되었습니다.', 'success')
            return redirect(url_for('index'))
        else:
            flash('사용자 이름 또는 비밀번호가 올바르지 않습니다.', 'danger')
    
    return render_template('login.html')

# 로그아웃
@app.route('/logout')
def logout():
    session.clear()
    flash('로그아웃되었습니다.', 'info')
    return redirect(url_for('index'))

# 새 포스트 작성
@app.route('/post/new', methods=['GET', 'POST'])
def new_post():
    if not is_logged_in():
        flash('포스트를 작성하려면 로그인이 필요합니다.', 'warning')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        user_id = session['user_id']
        
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO posts (title, content, user_id) VALUES (?, ?, ?)',
            (title, content, user_id)
        )
        conn.commit()
        conn.close()
        
        flash('포스트가 작성되었습니다.', 'success')
        return redirect(url_for('index'))
    
    return render_template('new_post.html')

# 포스트 상세 보기
@app.route('/post/<int:post_id>')
def post_detail(post_id):
    conn = get_db_connection()
    post = conn.execute('''
        SELECT p.id, p.title, p.content, p.created_at, p.user_id, u.username 
        FROM posts p JOIN users u ON p.user_id = u.id
        WHERE p.id = ?
    ''', (post_id,)).fetchone()
    
    if not post:
        conn.close()
        flash('포스트를 찾을 수 없습니다.', 'danger')
        return redirect(url_for('index'))
    
    comments = conn.execute('''
        SELECT c.id, c.content, c.created_at, c.user_id, u.username 
        FROM comments c JOIN users u ON c.user_id = u.id
        WHERE c.post_id = ?
        ORDER BY c.created_at ASC
    ''', (post_id,)).fetchall()
    
    conn.close()
    
    return render_template(
        'post_detail.html', 
        post=post, 
        comments=comments, 
        is_logged_in=is_logged_in(),
        is_author=is_logged_in() and session['user_id'] == post['user_id']
    )

# 포스트 수정
@app.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
def edit_post(post_id):
    if not is_logged_in():
        flash('포스트를 수정하려면 로그인이 필요합니다.', 'warning')
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    
    if not post:
        conn.close()
        flash('포스트를 찾을 수 없습니다.', 'danger')
        return redirect(url_for('index'))
    
    # 작성자만 수정 가능
    if post['user_id'] != session['user_id']:
        conn.close()
        flash('다른 사용자의 포스트는 수정할 수 없습니다.', 'danger')
        return redirect(url_for('post_detail', post_id=post_id))
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        conn.execute(
            'UPDATE posts SET title = ?, content = ? WHERE id = ?',
            (title, content, post_id)
        )
        conn.commit()
        conn.close()
        
        flash('포스트가 수정되었습니다.', 'success')
        return redirect(url_for('post_detail', post_id=post_id))
    
    conn.close()
    return render_template('edit_post.html', post=post)

# 포스트 삭제
@app.route('/post/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    if not is_logged_in():
        flash('포스트를 삭제하려면 로그인이 필요합니다.', 'warning')
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    
    if not post:
        conn.close()
        flash('포스트를 찾을 수 없습니다.', 'danger')
        return redirect(url_for('index'))
    
    # 작성자만 삭제 가능
    if post['user_id'] != session['user_id']:
        conn.close()
        flash('다른 사용자의 포스트는 삭제할 수 없습니다.', 'danger')
        return redirect(url_for('post_detail', post_id=post_id))
    
    # 먼저 해당 포스트의 모든 댓글 삭제
    conn.execute('DELETE FROM comments WHERE post_id = ?', (post_id,))
    
    # 포스트 삭제
    conn.execute('DELETE FROM posts WHERE id = ?', (post_id,))
    conn.commit()
    conn.close()
    
    flash('포스트가 삭제되었습니다.', 'success')
    return redirect(url_for('index'))

# 댓글 작성
@app.route('/post/<int:post_id>/comment', methods=['POST'])
def add_comment(post_id):
    if not is_logged_in():
        flash('댓글을 작성하려면 로그인이 필요합니다.', 'warning')
        return redirect(url_for('login'))
    
    content = request.form['content']
    user_id = session['user_id']
    
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    
    if not post:
        conn.close()
        flash('포스트를 찾을 수 없습니다.', 'danger')
        return redirect(url_for('index'))
    
    conn.execute(
        'INSERT INTO comments (content, post_id, user_id) VALUES (?, ?, ?)',
        (content, post_id, user_id)
    )
    conn.commit()
    conn.close()
    
    flash('댓글이 작성되었습니다.', 'success')
    return redirect(url_for('post_detail', post_id=post_id))

# 댓글 삭제
@app.route('/comment/<int:comment_id>/delete', methods=['POST'])
def delete_comment(comment_id):
    if not is_logged_in():
        flash('댓글을 삭제하려면 로그인이 필요합니다.', 'warning')
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    comment = conn.execute('''
        SELECT c.*, p.id as post_id FROM comments c
        JOIN posts p ON c.post_id = p.id
        WHERE c.id = ?
    ''', (comment_id,)).fetchone()
    
    if not comment:
        conn.close()
        flash('댓글을 찾을 수 없습니다.', 'danger')
        return redirect(url_for('index'))
    
    # 작성자만 삭제 가능
    if comment['user_id'] != session['user_id']:
        conn.close()
        flash('다른 사용자의 댓글은 삭제할 수 없습니다.', 'danger')
        return redirect(url_for('post_detail', post_id=comment['post_id']))
    
    conn.execute('DELETE FROM comments WHERE id = ?', (comment_id,))
    conn.commit()
    conn.close()
    
    flash('댓글이 삭제되었습니다.', 'success')
    return redirect(url_for('post_detail', post_id=comment['post_id']))

# 사용자 프로필
@app.route('/profile/<username>')
def profile(username):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    
    if not user:
        conn.close()
        flash('사용자를 찾을 수 없습니다.', 'danger')
        return redirect(url_for('index'))
    
    posts = conn.execute('''
        SELECT * FROM posts WHERE user_id = ? ORDER BY created_at DESC
    ''', (user['id'],)).fetchall()
    
    conn.close()
    
    return render_template('profile.html', user=user, posts=posts, is_logged_in=is_logged_in())

# 검색 기능
@app.route('/search')
def search():
    query = request.args.get('query', '')
    if not query:
        return redirect(url_for('index'))
    
    search_term = f'%{query}%'
    conn = get_db_connection()
    posts = conn.execute('''
        SELECT p.id, p.title, p.content, p.created_at, u.username 
        FROM posts p JOIN users u ON p.user_id = u.id
        WHERE p.title LIKE ? OR p.content LIKE ?
        ORDER BY p.created_at DESC
    ''', (search_term, search_term)).fetchall()
    conn.close()
    
    return render_template('search_results.html', posts=posts, query=query, is_logged_in=is_logged_in())

if __name__ == '__main__':
    if not os.path.exists('blog.db'):
        init_db()
    app.run(debug=True, host='0.0.0.0', port=5000) 