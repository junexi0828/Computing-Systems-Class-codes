-- Todo App 데이터베이스 초기화 스크립트

-- 데이터베이스 생성 (이미 docker-compose에서 생성됨)
-- CREATE DATABASE IF NOT EXISTS todo_db;

-- 사용자 테이블
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    avatar_url VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    is_admin BOOLEAN DEFAULT FALSE,
    role VARCHAR(20) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_users_username (username),
    INDEX idx_users_email (email),
    INDEX idx_users_is_active (is_active)
);

-- 할 일 테이블
CREATE TABLE IF NOT EXISTS todos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    priority VARCHAR(20) DEFAULT '중간',
    category VARCHAR(50) DEFAULT '개인',
    due_date DATETIME,
    completed BOOLEAN DEFAULT FALSE,
    completed_at DATETIME,
    is_public BOOLEAN DEFAULT FALSE,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (parent_id) REFERENCES todos(id) ON DELETE SET NULL,
    INDEX idx_todos_user_id (user_id),
    INDEX idx_todos_priority (priority),
    INDEX idx_todos_category (category),
    INDEX idx_todos_completed (completed),
    INDEX idx_todos_due_date (due_date),
    INDEX idx_todos_is_public (is_public),
    INDEX idx_todos_parent_id (parent_id)
);

-- 태그 테이블
CREATE TABLE IF NOT EXISTS tags (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    name VARCHAR(50) NOT NULL,
    color VARCHAR(7) DEFAULT '#007bff',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_tags_user_id (user_id),
    INDEX idx_tags_name (name),
    UNIQUE KEY unique_user_tag (user_id, name)
);

-- 할 일-태그 연결 테이블
CREATE TABLE IF NOT EXISTS todo_tags (
    id INT AUTO_INCREMENT PRIMARY KEY,
    todo_id INT NOT NULL,
    tag_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (todo_id) REFERENCES todos(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE,
    UNIQUE KEY unique_todo_tag (todo_id, tag_id)
);

-- 초기 데이터 삽입 (선택사항)
-- INSERT INTO users (username, email, password_hash, full_name) VALUES
-- ('admin', 'admin@example.com', 'hashed_password', '관리자');