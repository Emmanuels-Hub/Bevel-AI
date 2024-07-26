from flask import current_app, render_template, request, Blueprint, jsonify
from Ulo import db, bcrypt
from Ulo.bevel.base import upload_to_gemini
from Ulo.model import User, Admin
import os
import google.generativeai as genai

bevel = Blueprint('bevel', __name__)


@bevel.route("/")
@bevel.route("/home")
def index():
    return render_template('index.html')

# Admin ection

@bevel.route("/register/<email>/<password>/<name>", methods=['POST', 'GET'])
def register(email, password, name):
    auth = Admin.query.filter_by(email=email).first()
    if auth:
        js = {'satusCode': 419, 'status': 'warning', 'message': 'Email Already Exists.'}
    else:
        hash_password = bcrypt.generate_password_hash(password).decode('utf-8') 
        data = Admin(email=email, password=hash_password, school_name=name)
        db.session.add(data)
        db.session.commit()
        js = {'statusCode': 100, 'status':'success', 'message': 'Account created successful'}
    return jsonify(js)


@bevel.route("/login/<email>/<password>", methods=['POST', 'GET'])
def login(email, password):
    data = Admin.query.filter_by(email=email).first()
    if data and bcrypt.check_password_hash(data.password, password):
        js = {'statusCode':100, 'status' : 'success', 'message': 'User logged in'}
    else:
        js = {'statusCode': 404, 'status':'failed', 'message': 'Incorrect Login details.'}
    return jsonify(js)



# Users Sections

@bevel.route("/login_user/", methods=['POST', 'GET'])
def login_user():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    data = User.query.filter_by(email=email).first()

    if data and bcrypt.check_password_hash(data.password, password):
        js = {'statusCode':100, 'status' : 'success', 'message': 'User logged in'}
    else:
        js = {'statusCode': 404, 'status':'failed', 'message': 'Incorrect Login details.'}
    return jsonify(js)


@bevel.route("/create_user/", methods=['POST', 'GET'])
def create_user():
    # data = request.get_json()

    # email = data.get('email')
    # password = data.get('password')
    # name = data.get('name')
    # firstname = data.get('firstname')
    # lastname = data.get('lastname')
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


@bevel.route("/delete_user/<email>", methods=['POST', 'GET'])
def delete_user(email):
    data = User.query.filter_by(email=email).first()
    delt = User.query.get(data.id)
    db.session.delete(delt)
    db.session.commit()
    js = {'statusCode': 100, 'status':'success', 'message': 'Account Deleted successful'}
    return jsonify(js)


@bevel.route("/generate_audio/", methods=['POST', 'GET'])
def generate_audio():
    try:
        genai.configure(api_key=current_app.config["GEMINI_API_KEY"])
        filepath = ''
        prompt = 'Hello Here'
        mime_type = ''
        generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
        }

        model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        generation_config=generation_config,
        )

        files = [
        upload_to_gemini(filepath, mime_type=mime_type),
        ]

        chat_session = model.start_chat(
        history=[]
        )
        response = chat_session.send_message(prompt)

        return response.text
    except Exception as e:
        return e
        