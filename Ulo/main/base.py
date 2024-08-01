import glob
import google.generativeai as genai
import os

def upload_to_gemini(path, mime_type=None):
        file = genai.upload_file(path, mime_type=mime_type)
        print(f"Uploaded file '{file.display_name}' as: {file.uri}")
        return file

def delete_media_files():
    try:
        files = glob.glob(os.path.join('uploads', '*'))
        for file in files:
            os.remove(file)
        return 'Deleted Successful'
    except Exception as e:
        return e
    
def filter_text(text):
     result = text.replace('**','')
     result = result.replace('*', '')
     return result