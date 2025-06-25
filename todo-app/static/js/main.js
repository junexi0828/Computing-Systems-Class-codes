// API 엔드포인트
const API_BASE_URL = '/api';

// DOM 요소
const todoList = document.getElementById('todoList');
const filterForm = document.getElementById('filterForm');
const addTodoForm = document.getElementById('addTodoForm');
const saveTodoBtn = document.getElementById('saveTodoBtn');
const refreshBtn = document.getElementById('refreshBtn');
const addTodoModal = new bootstrap.Modal(document.getElementById('addTodoModal'));

// 유틸리티 함수
function formatDate(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleString('ko-KR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function isOverdue(dueDate) {
    if (!dueDate) return false;
    return new Date(dueDate) < new Date();
}

function getPriorityClass(priority) {
    switch (priority) {
        case '높음': return 'high';
        case '중간': return 'medium';
        case '낮음': return 'low';
        default: return 'medium';
    }
}

// 할 일 아이템 렌더링
function renderTodoItem(todo) {
    const isOverdueTodo = isOverdue(todo.due_date);
    const priorityClass = getPriorityClass(todo.priority);
    
    return `
        <div class="list-group-item todo-item ${todo.completed ? 'completed' : ''} priority-${priorityClass}" data-id="${todo.id}">
            <div class="d-flex justify-content-between align-items-center">
                <div class="d-flex align-items-center">
                    <div class="form-check me-3">
                        <input class="form-check-input" type="checkbox" ${todo.completed ? 'checked' : ''} 
                               onchange="toggleComplete(${todo.id})">
                    </div>
                    <div>
                        <h6 class="todo-title mb-1">${todo.title}</h6>
                        ${todo.description ? `<p class="mb-1 text-muted">${todo.description}</p>` : ''}
                        <div class="d-flex gap-2">
                            <span class="priority-badge ${priorityClass}">${todo.priority}</span>
                            <span class="category-badge">${todo.category}</span>
                            ${todo.due_date ? `
                                <span class="due-date ${isOverdueTodo ? 'overdue' : ''}">
                                    <i class="bi bi-calendar"></i> ${formatDate(todo.due_date)}
                                </span>
                            ` : ''}
                        </div>
                    </div>
                </div>
                <div class="todo-actions">
                    <button class="btn btn-sm btn-outline-danger" onclick="deleteTodo(${todo.id})">
                        <i class="bi bi-trash"></i>
                    </button>
                </div>
            </div>
        </div>
    `;
}

// 통계 렌더링
function renderStatistics(stats) {
    // 진행률 업데이트
    const progressBar = document.querySelector('.progress-bar');
    progressBar.style.width = `${stats.completion_rate}%`;
    progressBar.textContent = `${Math.round(stats.completion_rate)}%`;

    // 우선순위별 통계
    const priorityStats = document.getElementById('priorityStats');
    priorityStats.innerHTML = Object.entries(stats.priority_stats)
        .map(([priority, count]) => `
            <div class="stat-item">
                <span class="stat-label">${priority}</span>
                <span class="badge bg-primary">${count}</span>
            </div>
        `).join('');

    // 카테고리별 통계
    const categoryStats = document.getElementById('categoryStats');
    categoryStats.innerHTML = Object.entries(stats.category_stats)
        .map(([category, count]) => `
            <div class="stat-item">
                <span class="stat-label">${category}</span>
                <span class="badge bg-secondary">${count}</span>
            </div>
        `).join('');
}

// API 호출 함수
async function fetchTodos(filters = {}) {
    const queryParams = new URLSearchParams(filters).toString();
    const response = await fetch(`${API_BASE_URL}/todos?${queryParams}`);
    if (!response.ok) throw new Error('할 일 목록을 불러오는데 실패했습니다');
    return response.json();
}

async function fetchStatistics() {
    const response = await fetch(`${API_BASE_URL}/todos/statistics`);
    if (!response.ok) throw new Error('통계를 불러오는데 실패했습니다');
    return response.json();
}

async function createTodo(data) {
    const response = await fetch(`${API_BASE_URL}/todos`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
    if (!response.ok) throw new Error('할 일을 추가하는데 실패했습니다');
    return response.json();
}

async function toggleComplete(id) {
    const response = await fetch(`${API_BASE_URL}/todos/${id}/complete`, {
        method: 'PATCH'
    });
    if (!response.ok) throw new Error('상태 변경에 실패했습니다');
    return response.json();
}

async function deleteTodo(id) {
    if (!confirm('정말 삭제하시겠습니까?')) return;
    
    const response = await fetch(`${API_BASE_URL}/todos/${id}`, {
        method: 'DELETE'
    });
    if (!response.ok) throw new Error('삭제에 실패했습니다');
    await refreshTodos();
}

// 이벤트 핸들러
async function refreshTodos() {
    try {
        const formData = new FormData(filterForm);
        const filters = Object.fromEntries(formData.entries());
        
        const [todos, stats] = await Promise.all([
            fetchTodos(filters),
            fetchStatistics()
        ]);
        
        todoList.innerHTML = todos.map(renderTodoItem).join('');
        renderStatistics(stats);
    } catch (error) {
        alert(error.message);
    }
}

// 이벤트 리스너
filterForm.addEventListener('submit', (e) => {
    e.preventDefault();
    refreshTodos();
});

saveTodoBtn.addEventListener('click', async () => {
    try {
        const formData = new FormData(addTodoForm);
        const data = Object.fromEntries(formData.entries());
        
        await createTodo(data);
        addTodoModal.hide();
        addTodoForm.reset();
        await refreshTodos();
    } catch (error) {
        alert(error.message);
    }
});

refreshBtn.addEventListener('click', refreshTodos);

// 초기 로드
document.addEventListener('DOMContentLoaded', refreshTodos); 