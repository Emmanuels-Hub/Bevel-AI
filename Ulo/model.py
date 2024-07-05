from Ulo import db

sub = ['standard', 'premium', 'gold']
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)
    school_name = db.Column(db.String(200), nullable=False)
    firstname = db.Column(db.String(200), nullable=False)
    lastname = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'User({self.email}, {self.firstname}, {self.lastname})'
    
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)
    school_name = db.Column(db.String(200), nullable=False)
    sub = db.Column(db.String(50), default="standard", nullable=False)

    def __repr__(self):
        return f'Admin({self.email})'