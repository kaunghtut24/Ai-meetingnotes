from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Load secret keys from environment
SECRET_KEY = os.environ.get('SECRET_KEY')
gemini_key = os.environ.get('GEMINI_API_KEY')  # ✅ This is what was missing

@app.route('/api/gemini', methods=['POST'])
def gemini_generate():
    if not gemini_key:
        return jsonify({'error': 'Gemini API key not found'}), 500

    try:
        data = request.get_json()
        text = data.get('text', '')

        genai.configure(api_key=gemini_key)
        model = genai.GenerativeModel('gemini-pro')

        response = model.generate_content(text)
        return jsonify({'response': response.text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
