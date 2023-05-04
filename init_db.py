from app import app, get_db

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as FILE:
            db.cursor().executescript(FILE.read())
        db.commit()

if __name__ == '__main__':
    init_db()