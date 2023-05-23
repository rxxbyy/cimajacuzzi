#!/usr/bin/env python
from app import app, get_db_connection

def init_db():
    """ Initialize schemas on database """
    with app.app_context():
        conn = get_db_connection()
        with app.open_resource('schema.sql', mode='r') as FILE:
            conn.executescript(FILE.read())
        conn.commit()

# Make sure this script can only be executed directly 
if __name__ == '__main__':
    init_db()
