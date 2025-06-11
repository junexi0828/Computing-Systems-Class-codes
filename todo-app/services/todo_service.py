from models.todo import db, Todo

def get_all_todos():
    return Todo.query.all()

def get_todo_by_id(todo_id):
    return Todo.query.get_or_404(todo_id)

def create_todo(data):
    todo = Todo(**data)
    db.session.add(todo)
    db.session.commit()
    return todo

def update_todo(todo, data):
    for key, value in data.items():
        setattr(todo, key, value)
    db.session.commit()
    return todo

def delete_todo(todo):
    db.session.delete(todo)
    db.session.commit() 