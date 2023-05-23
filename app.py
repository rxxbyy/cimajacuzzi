from typing import Callable, Any
import os
import secrets
import sqlite3
import hashlib

from flask import (Flask, render_template, session, request,
    redirect, url_for, flash)
from forms import AuthForm

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_urlsafe())

#
# Setting server database
#
DATABASE_PATH = f'{os.path.abspath(os.getcwd())}/cimajacuzzi.db'

def get_db_connection() -> object | Any:
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    
    return conn

# 
# Flask Endpoints
# 
@app.route('/')
def index() -> Callable:
    """ Route server endpoint. It serves 'index.html' template. """
    return render_template('index.html', session=session)

@app.route('/auth', methods=['GET', 'POST'])
def auth() -> Callable:
    auth_form = AuthForm(request.form)

    if request.method == 'POST' and auth_form.validate_on_submit():
        conn = get_db_connection()

        username = auth_form.username.data
    
        found_user = conn.execute('SELECT username FROM user WHERE username=?', (username,)).fetchone()

        if found_user is None:
            cur = conn.cursor()

            cur.execute("INSERT INTO user (username) VALUES (?)", (username, ))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

        session['username'] = username

        return redirect(url_for('index'))
    
    return render_template('auth.html', auth_form=auth_form)

@app.route('/logout', methods=['GET'])
def logout() -> Callable:
    session.pop('username', None)
    return redirect(url_for('index'))
