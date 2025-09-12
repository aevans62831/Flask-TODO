from flask import Flask, render_template, request, redirect, url_for
from models import *
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db.init_app(app)

@app.route('/')
def index():
    todos = Todo.query.all()
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add():
    task = request.form.get('task')
    new_todo = Todo(task=task)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    todo = Todo.query.get(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:todo_id>', methods=['GET', 'POST'])
def edit(todo_id):
    todo = Todo.query.get(todo_id)
    if request.method == 'POST':
        todo.task = request.form.get('task')
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', todo=todo)

@app.route('/toggle_complete/<int:todo_id>', methods=['POST'])
def toggle_complete(todo_id):
    todo = Todo.query.get(todo_id)
    todo.completed = not todo.completed
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()
