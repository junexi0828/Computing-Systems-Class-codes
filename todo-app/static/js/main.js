document.addEventListener('DOMContentLoaded', () => {
    loadTodos();
    setupEventListeners();
});

function setupEventListeners() {
    document.getElementById('todoForm').addEventListener('submit', handleSubmit);
    document.getElementById('searchInput').addEventListener('input', handleSearch);
}

async function loadTodos() {
    try {
        const response = await fetch('/todos');
        const todos = await response.json();
        displayTodos(todos);
    } catch (error) {
        console.error('Error loading todos:', error);
    }
}

function displayTodos(todos) {
    const todoList = document.getElementById('todoList');
    todoList.innerHTML = '';
    
    todos.forEach(todo => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>
                <input type="checkbox" class="form-check-input" 
                    ${todo.is_completed ? 'checked' : ''} 
                    onchange="toggleComplete(${todo.id})">
            </td>
            <td class="${todo.is_completed ? 'completed' : ''}">${todo.title}</td>
            <td class="${todo.is_completed ? 'completed' : ''}">${todo.description || ''}</td>
            <td class="priority-${getPriorityClass(todo.priority)}">${getPriorityText(todo.priority)}</td>
            <td>${todo.due_date ? new Date(todo.due_date).toLocaleDateString() : ''}</td>
            <td>${todo.category || ''}</td>
            <td>
                <div class="btn-group btn-group-sm">
                    <button class="btn btn-outline-primary" onclick="editTodo(${todo.id})">수정</button>
                    <button class="btn btn-outline-danger" onclick="deleteTodo(${todo.id})">삭제</button>
                </div>
            </td>
        `;
        todoList.appendChild(row);
    });
}

function getPriorityClass(priority) {
    switch (parseInt(priority)) {
        case 1: return 'high';
        case 2: return 'medium';
        case 3: return 'low';
        default: return 'medium';
    }
}

function getPriorityText(priority) {
    switch (parseInt(priority)) {
        case 1: return '높음';
        case 2: return '중간';
        case 3: return '낮음';
        default: return '중간';
    }
}

async function handleSubmit(event) {
    event.preventDefault();
    
    const todo = {
        title: document.getElementById('title').value,
        description: document.getElementById('description').value,
        priority: document.getElementById('priority').value,
        due_date: document.getElementById('dueDate').value,
        category: document.getElementById('category').value
    };
    
    try {
        const response = await fetch('/todos', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(todo)
        });
        
        if (response.ok) {
            event.target.reset();
            loadTodos();
        }
    } catch (error) {
        console.error('Error creating todo:', error);
    }
}

async function toggleComplete(id) {
    try {
        const response = await fetch(`/todos/${id}/complete`, {
            method: 'PATCH'
        });
        
        if (response.ok) {
            loadTodos();
        }
    } catch (error) {
        console.error('Error toggling todo:', error);
    }
}

async function deleteTodo(id) {
    if (!confirm('정말 삭제하시겠습니까?')) return;
    
    try {
        const response = await fetch(`/todos/${id}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            loadTodos();
        }
    } catch (error) {
        console.error('Error deleting todo:', error);
    }
}

async function editTodo(id) {
    try {
        const response = await fetch(`/todos/${id}`);
        const todo = await response.json();
        
        document.getElementById('title').value = todo.title;
        document.getElementById('description').value = todo.description || '';
        document.getElementById('priority').value = todo.priority;
        document.getElementById('dueDate').value = todo.due_date ? todo.due_date.split('T')[0] : '';
        document.getElementById('category').value = todo.category || '';
        
        // 폼 제출 핸들러를 수정 모드로 변경
        const form = document.getElementById('todoForm');
        form.onsubmit = async (e) => {
            e.preventDefault();
            
            const updatedTodo = {
                title: document.getElementById('title').value,
                description: document.getElementById('description').value,
                priority: document.getElementById('priority').value,
                due_date: document.getElementById('dueDate').value,
                category: document.getElementById('category').value
            };
            
            try {
                const response = await fetch(`/todos/${id}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(updatedTodo)
                });
                
                if (response.ok) {
                    form.reset();
                    form.onsubmit = handleSubmit; // 폼 핸들러를 원래대로 복원
                    loadTodos();
                }
            } catch (error) {
                console.error('Error updating todo:', error);
            }
        };
    } catch (error) {
        console.error('Error loading todo:', error);
    }
}

function handleSearch(event) {
    const searchTerm = event.target.value.toLowerCase();
    const rows = document.querySelectorAll('#todoList tr');
    
    rows.forEach(row => {
        const title = row.cells[1].textContent.toLowerCase();
        const description = row.cells[2].textContent.toLowerCase();
        
        if (title.includes(searchTerm) || description.includes(searchTerm)) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
} 