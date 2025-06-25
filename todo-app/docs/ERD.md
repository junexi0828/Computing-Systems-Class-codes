# 확장된 TODO 애플리케이션 ERD

## 📊 데이터베이스 스키마

### 1. 사용자 관리 (users)
```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    avatar_url VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    role ENUM('admin', 'user') DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_is_active (is_active)
);
```

### 2. 할 일 관리 (todos) - 기존 확장
```sql
CREATE TABLE todos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    priority ENUM('높음', '중간', '낮음') DEFAULT '중간',
    category VARCHAR(50) DEFAULT '개인',
    due_date DATETIME,
    completed BOOLEAN DEFAULT FALSE,
    completed_at DATETIME,
    is_public BOOLEAN DEFAULT FALSE,
    parent_id INT NULL,  -- 서브태스크 지원
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (parent_id) REFERENCES todos(id) ON DELETE CASCADE,

    INDEX idx_user_id (user_id),
    INDEX idx_priority (priority),
    INDEX idx_category (category),
    INDEX idx_completed (completed),
    INDEX idx_due_date (due_date),
    INDEX idx_is_public (is_public),
    INDEX idx_parent_id (parent_id)
);
```

### 3. 할 일 공유 (todo_shares)
```sql
CREATE TABLE todo_shares (
    id INT AUTO_INCREMENT PRIMARY KEY,
    todo_id INT NOT NULL,
    shared_by INT NOT NULL,  -- 공유한 사용자
    shared_with INT NOT NULL,  -- 공유받은 사용자
    permission ENUM('read', 'write', 'admin') DEFAULT 'read',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (todo_id) REFERENCES todos(id) ON DELETE CASCADE,
    FOREIGN KEY (shared_by) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (shared_with) REFERENCES users(id) ON DELETE CASCADE,

    UNIQUE KEY unique_share (todo_id, shared_with),
    INDEX idx_todo_id (todo_id),
    INDEX idx_shared_with (shared_with)
);
```

### 4. 할 일 태그 (tags)
```sql
CREATE TABLE tags (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    name VARCHAR(50) NOT NULL,
    color VARCHAR(7) DEFAULT '#007bff',  -- HEX 색상
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,

    UNIQUE KEY unique_user_tag (user_id, name),
    INDEX idx_user_id (user_id)
);
```

### 5. 할 일-태그 연결 (todo_tags)
```sql
CREATE TABLE todo_tags (
    id INT AUTO_INCREMENT PRIMARY KEY,
    todo_id INT NOT NULL,
    tag_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (todo_id) REFERENCES todos(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE,

    UNIQUE KEY unique_todo_tag (todo_id, tag_id),
    INDEX idx_todo_id (todo_id),
    INDEX idx_tag_id (tag_id)
);
```

### 6. 할 일 히스토리 (todo_history)
```sql
CREATE TABLE todo_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    todo_id INT NOT NULL,
    user_id INT NOT NULL,
    action ENUM('created', 'updated', 'completed', 'deleted', 'shared') NOT NULL,
    old_values JSON,
    new_values JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (todo_id) REFERENCES todos(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,

    INDEX idx_todo_id (todo_id),
    INDEX idx_user_id (user_id),
    INDEX idx_action (action),
    INDEX idx_created_at (created_at)
);
```

### 7. 알림 설정 (notifications)
```sql
CREATE TABLE notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    todo_id INT,
    type ENUM('due_soon', 'overdue', 'shared', 'reminder') NOT NULL,
    title VARCHAR(200) NOT NULL,
    message TEXT,
    is_read BOOLEAN DEFAULT FALSE,
    scheduled_at DATETIME,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (todo_id) REFERENCES todos(id) ON DELETE CASCADE,

    INDEX idx_user_id (user_id),
    INDEX idx_todo_id (todo_id),
    INDEX idx_is_read (is_read),
    INDEX idx_scheduled_at (scheduled_at)
);
```

### 8. 사용자 설정 (user_settings)
```sql
CREATE TABLE user_settings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    theme ENUM('light', 'dark', 'auto') DEFAULT 'light',
    language VARCHAR(10) DEFAULT 'ko',
    timezone VARCHAR(50) DEFAULT 'Asia/Seoul',
    notification_email BOOLEAN DEFAULT TRUE,
    notification_push BOOLEAN DEFAULT TRUE,
    default_priority ENUM('높음', '중간', '낮음') DEFAULT '중간',
    default_category VARCHAR(50) DEFAULT '개인',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

## 🔗 관계도

```
users (1) ←→ (N) todos
users (1) ←→ (N) tags
users (1) ←→ (N) todo_shares
users (1) ←→ (1) user_settings
users (1) ←→ (N) notifications

todos (1) ←→ (N) todo_shares
todos (1) ←→ (N) todo_tags
todos (1) ←→ (N) todo_history
todos (1) ←→ (N) notifications
todos (1) ←→ (N) todos (parent-child)

tags (1) ←→ (N) todo_tags
```

## 📈 주요 기능별 테이블 활용

### 1. 사용자 관리
- `users`: 회원가입, 로그인, 프로필 관리
- `user_settings`: 개인 설정 관리

### 2. 할 일 관리
- `todos`: 기본 CRUD, 서브태스크 지원
- `tags`: 태그 기반 분류
- `todo_tags`: 할 일과 태그 연결

### 3. 협업 기능
- `todo_shares`: 할 일 공유 및 권한 관리
- `todo_history`: 변경 이력 추적

### 4. 알림 시스템
- `notifications`: 다양한 알림 타입 지원

### 5. 통계 및 분석
- 모든 테이블의 데이터를 활용한 고급 통계
- 사용자별, 기간별, 카테고리별 분석