from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import *
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.secret_key = 'your_secret_key'
db.init_app(app)

@app.route('/')
def index():
    if 'user_id' not in session.keys():
        return redirect(url_for('login'))
    if session.get('user_id') is None:
        return redirect(url_for('login'))
    todos = Todo.query.filter_by(user_id=session['user_id']).all()
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    task = request.form.get('task')
    new_todo = Todo(task=task, user_id=session['user_id'])
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if session['user_id'] != Todo.query.get(todo_id).user_id:
        flash('You do not have permission to delete this task.')
        return redirect(url_for('index'))
    todo = Todo.query.get(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:todo_id>', methods=['GET', 'POST'])
def edit(todo_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if session['user_id'] != Todo.query.get(todo_id).user_id:
        flash('You do not have permission to edit this task.')
        return redirect(url_for('index'))

    todo = Todo.query.get(todo_id)
    if request.method == 'POST':
        task_value = request.form.get('task')
        date_value = request.form.get('date')
        if task_value:
            todo.task = task_value
        if date_value:
            todo.date = datetime.strptime(date_value, '%Y-%m-%d')
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('edit.html', todo=todo)

@app.route('/toggle_complete/<int:todo_id>', methods=['POST'])
def toggle_complete(todo_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    todo = Todo.query.get(todo_id)
    todo.completed = not todo.completed
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. Please log in.')
        login(autologin_id=user.id)
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login(autologin_id=False):
    if autologin_id:
        session['user_id'] = autologin_id
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            return redirect(url_for('index'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
def logout():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    session.pop('user_id', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()
