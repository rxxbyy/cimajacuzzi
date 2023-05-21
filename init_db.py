#!/usr/bin/env python
from app import app, get_db

def init_db():
    """ Initialize schemas on database """
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as FILE:
            db.cursor().executescript(FILE.read())
        db.commit()

# Make sure this script can only be executed directly 
if __name__ == '__main__':
    init_db()
