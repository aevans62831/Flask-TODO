from flask import Flask, render_template, request, session, redirect, url_for
from models import *
app = Flask(__name__)
app.secret_key = ""
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db.init_app(app)

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/user/<name>')
def hello_user(name):
    return render_template('index.html', name=name)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username
        return redirect(url_for('profile'))
    return '''
        <form method="post">
            <p><input type=text name=username></p>
            <p><input type=submit value=Login></p>
        </form>
    '''

@app.route('/profile')
def profile():
    if 'username' in session:
        return f'Logged in as {session["username"]}'
    return 'You are not logged in.'

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run()
