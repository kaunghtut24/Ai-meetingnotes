from flask import Flask, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Load secret keys from environment
SECRET_KEY = os.environ.get('SECRET_KEY')
assemblyai_key = os.environ.get('ASSEMBLYAI_API_KEY')  # ✅ This was missing

@app.route('/api/assemblyai-token', methods=['GET'])
def get_assemblyai_token():
    if not assemblyai_key:
        return jsonify({'error': 'AssemblyAI API key not found'}), 500

    # For now, just return the key as a token (replace with secure logic if needed)
    return jsonify({'token': assemblyai_key})
