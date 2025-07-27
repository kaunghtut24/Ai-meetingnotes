import os
import json
import secrets
import hashlib
from datetime import datetime, timedelta
from http.server import BaseHTTPRequestHandler
import jwt

SECRET_KEY = os.environ.get("SECRET_KEY", secrets.token_hex(32))

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Generate a dummy user ID
            user_id = hashlib.sha256(os.urandom(16)).hexdigest()[:16]

            token = jwt.encode({
                'user_id': user_id,
                'exp': datetime.utcnow() + timedelta(hours=24),
                'iat': datetime.utcnow()
            }, SECRET_KEY, algorithm='HS256')

            response = {
                'token': token,
                'user_id': user_id,
                'expires_in': 86400
            }

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
            self.end_headers()

            self.wfile.write(json.dumps(response).encode())

        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()
