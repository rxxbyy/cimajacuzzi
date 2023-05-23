from typing import Callable, Any
import os
import secrets
import sqlite3

from passlib.hash import pbkdf2_sha256

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

    error = None
    if request.method == 'POST' and auth_form.validate_on_submit():
        conn = get_db_connection()

        seller_name = auth_form.seller_name.data
        seller_pass = pbkdf2_sha256.hash(auth_form.seller_pass.data)
    
        found_user = conn.execute('SELECT seller_name, seller_pass FROM seller WHERE seller_name=?', (seller_name,)).fetchone()

        if found_user is None:
            cur = conn.cursor()

            cur.execute("INSERT INTO seller (seller_name, seller_pass) VALUES (?, ?)",
                        (seller_name, seller_pass))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

        real_user_pass = found_user[1]
        if pbkdf2_sha256.verify(auth_form.seller_pass.data, real_user_pass):
            session['username'] = found_user[0]
            return redirect(url_for('index'))

        error = 'Contraseña incorrecta'
    
    return render_template('auth.html', auth_form=auth_form, error=error)

@app.route('/logout', methods=['GET'])
def logout() -> Callable:
    session.pop('username', None)
    return redirect(url_for('index'))
