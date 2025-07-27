import os
import json
import jwt
from http.server import BaseHTTPRequestHandler

# Configuration
SECRET_KEY = os.environ.get('SECRET_KEY', 'default-secret-key')

def verify_token(token):
    """Verify JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload.get('user_id')
    except jwt.InvalidTokenError:
        return None

class handler(BaseHTTPRequestHandler):
    def _send_json_response(self, status, data):
        """Helper to send JSON with proper headers"""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def _get_user_id(self):
        """Extract and verify JWT token"""
        auth_header = self.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return None
        token = auth_header.split(' ')[1]
        return verify_token(token)

    def do_POST(self):
        """Save user configuration"""
        try:
            user_id = self._get_user_id()
            if not user_id:
                self._send_json_response(401, {'error': 'Invalid or missing token'})
                return

            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            config_data = json.loads(post_data.decode('utf-8'))

            # (In a real app, save config_data to database)

            response_data = {
                'success': True,
                'message': 'Configuration saved successfully',
                'user_id': user_id
            }
            self._send_json_response(200, response_data)

        except Exception as e:
            self._send_json_response(500, {'error': str(e)})

    def do_GET(self):
        """Load user configuration"""
        try:
            user_id = self._get_user_id()
            if not user_id:
                self._send_json_response(401, {'error': 'Invalid or missing token'})
                return

            # (In a real app, load config from database)
            response_data = {
                'assemblyai_api_key': '',
                'gemini_api_key': '',
                'user_id': user_id
            }
            self._send_json_response(200, response_data)

        except Exception as e:
            self._send_json_response(500, {'error': str(e)})

    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
