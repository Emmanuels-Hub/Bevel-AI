from flask import render_template, request, Blueprint, jsonify
from Ulo import db, bcrypt
from Ulo.model import User, Admin

bevel = Blueprint('bevel', __name__)


@bevel.route("/")
@bevel.route("/home")
def index():
    return render_template('index.html')

# Admin section

@bevel.route("/register/<sch>/", methods=['POST', 'GET'])
def register(sch):
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    school_name = data.get('school_name')

    auth = Admin.query.filter_by(email=email).first()
    if auth:
        js = {'satusCode': 419, 'status': 'warning', 'message': 'Email Already Exists.'}
    else:
        hash_password = bcrypt.generate_password_hash(password).decode('utf-8') 
        data = Admin(email=email, password=hash_password, school_name=school_name)
        db.session.add(data)
        db.session.commit()
        js = {'statusCode': 100, 'status':'success', 'message': 'Account created successful'}
    return jsonify(js)


@bevel.route("/login/<sch>/", methods=['POST', 'GET'])
def login(sch):
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    auth = Admin.query.filter_by(email=email).first()
    if auth and bcrypt.check_password_hash(auth.password, password):
        js = {'statusCode':100, 'status' : 'success', 'message': 'User logged in'}
    else:
        js = {'statusCode': 404, 'status':'failed', 'message': 'Incorrect Login details.'}
    return jsonify(js)



# Users Sections

@bevel.route("/login_user/<sch>/", methods=['POST', 'GET'])
def login_user(sch):
    if sch == 'Bevel':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        auth = User.query.filter_by(email=email).first()

        if auth and bcrypt.check_password_hash(auth.password, password):
            js = {'statusCode':100, 'status' : 'success', 'message': 'User logged in'}
        else:
            js = {'statusCode': 404, 'status':'failed', 'message': 'Incorrect Login details.'}
        return jsonify(js)


@bevel.route("/create_user/<sch>/", methods=['POST', 'GET'])
def create_user(sch):
    # info = request.get_json()

    # email = info.get('email')
    # password = info.get('password')
    # name = info.get('name')
    # firstname = info.get('firstname')
    # lastname = info.get('lastname')

    email = 'Justin'
    password = 'qwerty'
    name = 'Bevel'
    firstname = 'John'
    lastname = 'Paul'

    auth = User.query.filter_by(email=email).first()
    if auth:
        js = {'satusCode': 419, 'status': 'warning', 'message': 'Email Already Exists.'}
    else:
        
        hash_password = bcrypt.generate_password_hash(password).decode('utf-8') 
        data = User(
            email=email,
            password= hash_password,
            school_name=name,
            firstname=firstname,
            lastname=lastname)
        db.session.add(data)
        db.session.commit()
        js = {'statusCode': 100, 'status':'success', 'message': 'Account created successful'}
    return jsonify(js)


@bevel.route("/delete_user/<sch>/", methods=['POST', 'GET'])
def delete_user(sch):
    info = request.get_json()
    email = info.get('email')
    data = User.query.filter_by(email=email).first()
    delt = User.query.get(data.id)
    db.session.delete(delt)
    db.session.commit()
    js = {'statusCode': 100, 'status':'success', 'message': 'Account Deleted successful'}
    return jsonify(js)


