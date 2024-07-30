import os
from flask import current_app, render_template, request, Blueprint
import google.generativeai as genai

from Ulo.main.base import delete_media_files, upload_to_gemini

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def index():
    return render_template('index.html')


@main.route("/generate_media/", methods=['POST', 'GET'])
def generate_audio():
    try:
        genai.configure(api_key=current_app.config["GEMINI_API_KEY"])
        filepath = request.files['file']
        prompt = request.form.get('prompt')
        mime_type = request.form.get('mime')

        if filepath:
            filename = filepath.filename
            filepath.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

        generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",

        }

        model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction="You are an educational chatbot designed to help and assist students across all educational fields. Your primary goals are to provide accurate information, assist with various academic tasks, offer study tips, and be supportive and encouraging. Here are the key points to guide your responses:\n\nSubject Matter Expertise:\nYou should be knowledgeable in a wide range of subjects including mathematics, science, literature, history, and more.\nProvide clear, concise explanations and step-by-step solutions to problems\nacross various subjects.",
        )

        media = upload_to_gemini(f"{current_app.config['UPLOAD_FOLDER']}/{filename}", mime_type=mime_type)
        chat_session = model.start_chat(
        history=
            [
                {
                    "role": "user",
                    "parts": [ media, prompt ],
                },
            
            ]
        )
        response = chat_session.send_message(prompt)

        return response.text
    except Exception as e:
        return e
    
@main.route("/delete_media/")
def delete_media():
    con  = delete_media_files()
    return con