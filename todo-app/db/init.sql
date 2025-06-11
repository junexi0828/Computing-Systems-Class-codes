CREATE TABLE IF NOT EXISTS todos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    priority INT DEFAULT 2,
    due_date DATETIME,
    is_completed BOOLEAN DEFAULT FALSE,
    category VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE INDEX idx_due_date ON todos (due_date);
CREATE INDEX idx_category ON todos (category);

INSERT INTO todos (title, description, priority, due_date, category)
VALUES ('샘플 할 일', '이것은 샘플입니다.', 1, '2025-12-31', '개인'); 