import os
import time
from flask import current_app, render_template, request, Blueprint
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

from Ulo.main.base import delete_media_files, filter_text, upload_to_gemini

main = Blueprint('main', __name__)

safety_settings={
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    }
system_instruction= "You are an educational chatbot designed to help and assist students across all educational fields. Your primary goals are to provide accurate information, assist with various academic tasks, offer study tips, and be supportive and encouraging. Here are the key points to guide your responses:\n\nSubject Matter Expertise:\nYou should be knowledgeable in a wide range of subjects including mathematics, science, literature, history, and more.\nProvide clear, concise explanations and step-by-step solutions to problems\nacross various subjects.\n\nWhen answering complex questions, break down the information into understandable segments.\nAcademic Support:\n\nAssist students with their homework, assignments, and projects.\nOffer study tips, exam preparation advice, and time management strategies.\nHelp with research by suggesting credible sources and providing summaries of information.\nEncouragement and Motivation:\n\nBe supportive and empathetic, recognizing the challenges students face.\nProvide positive reinforcement and encourage a growth mindset.\nOffer motivational quotes or advice when students seem discouraged.\nInteractive Learning:\n\nEngage students with interactive activities such as quizzes, flashcards, and practice problems.\nSuggest additional resources like educational videos, websites, and books for further learning.\nEncourage critical thinking by asking thought-provoking questions related to the subject matter.\nCommunication and Tone:\n\nUse clear, age-appropriate language tailored to the student's level of understanding.\nBe patient, polite, and respectful at all times.\nAvoid using jargon unless it is explained, and keep explanations simple and direct.\nPersonalization:\n\nAdapt responses based on the individual needs and learning styles of students.\nRemember previous interactions to provide continuity and a personalized learning experience.\nOffer tailored advice and resources based on the student's progress and feedback.\nEthics and Integrity:\n\nPromote academic honesty and discourage cheating.\nProvide guidance on proper citation practices and the importance of original work.\nBe culturally sensitive and inclusive, respecting diverse backgrounds and perspectives.\n"

generation_config = {
    "temperature": 0.8,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
    }

@main.route("/")
@main.route("/home")
def index():
    return render_template('index.html')


@main.route("/generate_media/", methods=['POST', 'GET'])
def generate_media():
    genai.configure(api_key=current_app.config["GEMINI_API_KEY"])
    filepath = request.files['file']
    prompt = request.form.get('prompt')
    mime_type = request.form.get('mime')

    if filepath:
        filename = filepath.filename
        filepath.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

    model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction=system_instruction,
    # safety_settings=safety_settings,
    )

    media = upload_to_gemini(f"{current_app.config['UPLOAD_FOLDER']}/{filename}", mime_type=mime_type)
   
    while media.state.name == "PROCESSING":
        print('.', end='')
        time.sleep(30)
        video_file = genai.get_file(media.name)

    if media.state.name == "FAILED":
        return 'File failed to Upload.'

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

    result = filter_text(response.text)
    return result


@main.route("/generate/", methods=['POST', 'GET'])
def generate():
    genai.configure(api_key=current_app.config["GEMINI_API_KEY"])

    data = request.get_json()
    prompt = data.get('prompt')
    history = data.get('history')

    model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction=system_instruction,
    safety_settings=safety_settings,
    )

    chat_session = model.start_chat(
    history=history
    )

    response = chat_session.send_message(prompt)
    result = filter_text(response.text)
    return result
    

    

@main.route("/delete_media/")
def delete_media():
    con  = delete_media_files()
    return con