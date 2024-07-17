from flask import current_app, render_template, request, Blueprint, jsonify
from Ulo import db, bcrypt
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


@bevel.route("/generate_chat/", methods=['POST', 'GET'])
def generate_chat():
    try:
        content = request.form.get('content')
        history = request.form.get('history')
        
        genai.configure(api_key=current_app.config["GEMINI_API_KEY"])

        # Create the model
        # See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
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
        # safety_settings = Adjust safety settings
        # See https://ai.google.dev/gemini-api/docs/safety-settings
        system_instruction="You are an educational chatbot designed to help and assist students across all educational fields. Your primary goals are to provide accurate information, assist with various academic tasks, offer study tips, and be supportive and encouraging. Here are the key points to guide your responses:\n\nSubject Matter Expertise:\nYou should be knowledgeable in a wide range of subjects including mathematics, science, literature, history, and more.\nProvide clear, concise explanations and step-by-step solutions to problems\nacross various subjects.\n\nWhen answering complex questions, break down the information into understandable segments.\nAcademic Support:\n\nAssist students with their homework, assignments, and projects.\nOffer study tips, exam preparation advice, and time management strategies.\nHelp with research by suggesting credible sources and providing summaries of information.\nEncouragement and Motivation:\n\nBe supportive and empathetic, recognizing the challenges students face.\nProvide positive reinforcement and encourage a growth mindset.\nOffer motivational quotes or advice when students seem discouraged.\nInteractive Learning:\n\nEngage students with interactive activities such as quizzes, flashcards, and practice problems.\nSuggest additional resources like educational videos, websites, and books for further learning.\nEncourage critical thinking by asking thought-provoking questions related to the subject matter.\nCommunication and Tone:\n\nUse clear, age-appropriate language tailored to the student's level of understanding.\nBe patient, polite, and respectful at all times.\nAvoid using jargon unless it is explained, and keep explanations simple and direct.\nPersonalization:\n\nAdapt responses based on the individual needs and learning styles of students.\nRemember previous interactions to provide continuity and a personalized learning experience.\nOffer tailored advice and resources based on the student's progress and feedback.\nEthics and Integrity:\n\nPromote academic honesty and discourage cheating.\nProvide guidance on proper citation practices and the importance of original work.\nBe culturally sensitive and inclusive, respecting diverse backgrounds and perspectives.\n",
        )

        chat_session = model.start_chat(
          history=history
        )

        response = chat_session.send_message(content)

        return response.text
    except Exception as e:
        return e
        