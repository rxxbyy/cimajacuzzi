from typing import Callable, Any
import os
import secrets
import sqlite3
from flask import (Flask, render_template, g, session, request,
    redirect, url_for)
from forms import RegisterForm

__all__ = ['app']

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_urlsafe())

# Configuring database
DATABASE = f'{os.path.abspath(os.getcwd())}/cimajacuzzi.db'

def get_db() -> object | Any:
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row

    return db

@app.teardown_appcontext
def close_connection(expection) -> None:
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index() -> Callable:
    return render_template('index.html', session=session)

@app.route('/register', methods=['GET', 'POST'])
def register() -> Callable:
    reg_form = RegisterForm()

    if request.method == "POST" and reg_form.validate_on_submit():
        session['username'] = request.form['username']
        return redirect(url_for('index'))

    return render_template('register.html', reg_form=reg_form)

@app.route('/logout', methods=['GET'])
def logout() -> Callable:
    session.pop('username', None)
    return redirect(url_for('index'))
