import os
from Ulo import create_app, db

app = create_app()
if not os.path.exists('uploads'):
    os.makedirs('uploads')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # app.run(debug=True)