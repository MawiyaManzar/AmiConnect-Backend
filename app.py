# AmiConnect Backend - Flask App Skeleton
from flask import Flask
from flask_cors import CORS
import os
from auth import bp as auth_bp
from users import bp as users_bp
from recommend import bp as recommend_bp
import jwt
from functools import wraps
from flask import request, jsonify
from dotenv import load_dotenv
from auth_utils import jwt_required  # Import from auth_utils

load_dotenv()
DB_URL = os.getenv('DATABASE_URL')
SECRET_KEY = os.getenv('SECRET_KEY')
app = Flask(__name__)
app.config['ENV'] = os.getenv('FLASK_ENV', 'production')
CORS(app)

app.register_blueprint(auth_bp)
app.register_blueprint(users_bp)
app.register_blueprint(recommend_bp)



@app.route('/')
def index():
    return {'status': 'AmiConnect backend running'}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
