from typing import Callable, Any
import os
import secrets
import sqlite3

from passlib.hash import pbkdf2_sha256

from flask import (Flask, render_template, session, request,
    redirect, url_for)
from forms import AuthForm, ProductForm, HourForm

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
    conn = get_db_connection()

    sellers = conn.execute('SELECT * FROM seller').fetchall()

    conn.commit()
    conn.close()

    return render_template('index.html', session=session, sellers=sellers)

@app.route('/seller/<seller_name>')
def display_seller(seller_name: str):
    conn = get_db_connection()
    seller_products = conn.execute('SELECT seller_name, product_name, product_price, product_desc, product_exists FROM seller INNER JOIN product ON seller_id=product_owner '
                              'WHERE seller_name=?', (seller_name,)).fetchall()
    conn.commit()
    conn.close()
    print(seller_products)
    return render_template('seller.html', seller_products=seller_products, seller_name=seller_name)

@app.route('/auth', methods=['GET', 'POST'])
def auth() -> Callable:
    auth_form = AuthForm(request.form)

    error = None
    if request.method == 'POST' and auth_form.validate_on_submit():
        conn = get_db_connection()

        seller_name = auth_form.seller_name.data
        seller_pass = pbkdf2_sha256.hash(auth_form.seller_pass.data)
    
        found_user = conn.execute('SELECT seller_id, seller_name, seller_pass FROM seller WHERE seller_name=?',
                                  (seller_name,)).fetchone()

        if found_user is None:
            cur = conn.cursor()

            cur.execute("INSERT INTO seller VALUES (NULL, ?, ?, ?, ?)",
                        (seller_name, seller_pass, 0, 0))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

        real_user_pass = found_user[2]
        if pbkdf2_sha256.verify(auth_form.seller_pass.data, real_user_pass):
            session['user_id'] = found_user[0]
            session['username'] = found_user[1]
            return redirect(url_for('index'))

        error = 'Contraseña incorrecta'
    
    return render_template('auth.html', auth_form=auth_form, error=error)


@app.route('/panel')
def panel() -> Callable:
    if 'username' not in session:
        return redirect(url_for('index'))


    conn = get_db_connection()
    products = conn.execute('SELECT * FROM product WHERE product_owner = ?', (session.get('user_id'),)).fetchall()

    product_form = ProductForm(request.form)
    schedule_form = HourForm(request.form)
    
    return render_template('panel.html', 
                           session=session,
                           product_form=product_form,
                           schedule_form=schedule_form,
                           products=products)

@app.route('/panel/add_product')
def add_product():
    if 'username' not in session:
        return redirect(url_for('index'))

    owner_id = session.get('user_id')
    product_name = request.args['product_name']
    product_price = request.args['product_price']
    product_desc = request.args['product_desc']
    product_exists = request.args.get('product_exists', False)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO product (product_id, product_owner, product_name, product_price, '
                   'product_desc, product_exists) VALUES (NULL, ?, ?, ?, ?, ?)',
                   (owner_id, product_name, product_price, product_desc, product_exists))
    conn.commit()
    conn.close()

    return redirect(url_for('panel'))

@app.route('/panel/edit_product/<product_id>', methods=['GET', 'POST'])
def edit_product(product_id: int):
    product_form = ProductForm(request.form)

    conn = get_db_connection()
    cur_product = conn.execute('SELECT * FROM product WHERE product_id=?', (product_id,)).fetchone()

    if request.method == 'POST' and product_form.validate_on_submit():
        product_name = product_form.product_name.data
        product_price = product_form.product_price.data
        product_desc = product_form.product_desc.data
        product_exists = product_form.product_exists.data

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('UPDATE product SET product_name=?, product_price=?, product_desc=?,'
                       ' product_exists=? WHERE product_id=?',
                       (product_name, product_price, product_desc, product_exists, product_id))
        conn.commit()
        conn.close()
        return redirect(url_for('panel'))

    return render_template('edit_product.html',
                           product_form=product_form,
                           product_id=product_id,
                           cur_product=cur_product)

@app.route('/panel/delete_product/<product_id>')
def delete_product(product_id: int):

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM product WHERE product_id = ?', (product_id,))
    conn.commit()
    conn.close()

    return redirect(url_for('panel'))

@app.route('/panel/set_hour')
def set_hour():
    if 'username' not in session:
        return redirect(url_for('index'))
    

    conn = get_db_connection()
    cursor = conn.cursor()

    start_hour = request.args['start_hour']
    leaving_hour = request.args['leaving_hour']

    cursor.execute('UPDATE seller SET start_hour = ?, end_hour = ? WHERE seller_id = ?',
                    (start_hour, leaving_hour, session.get('user_id')))
    conn.commit()
    conn.close()

    return redirect(url_for('panel'))

@app.route('/logout', methods=['GET'])
def logout() -> Callable:
    session.clear()
    return redirect(url_for('index'))
