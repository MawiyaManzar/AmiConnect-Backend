import os
import re
import psycopg2
import bcrypt
import jwt
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify, current_app
from dotenv import load_dotenv

load_dotenv()

bp = Blueprint('auth', __name__)
DB_URL = os.getenv('DATABASE_URL')
SECRET_KEY = os.getenv('SECRET_KEY')

AMITY_EMAIL_REGEX = re.compile(r'^[\w.-]+@s\.amity\.edu$')

# Helper to get DB connection
def get_conn():
    return psycopg2.connect(DB_URL)

@bp.route('/signup', methods=['POST', 'OPTIONS'])
def signup():
        if request.method == 'OPTIONS':
            response = jsonify()
            response.status_code = 200
            return response
        data = request.json
        required_fields = ['name', 'email', 'password', 'gender', 'department', 'year', 'connection_type', 'interests', 'skills', 'learning_goals']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing field: {field}'}), 400

        email = data['email'].strip().lower()
        if not AMITY_EMAIL_REGEX.match(email):
            return jsonify({'error': 'Invalid Amity email format'}), 400

        # Hash password
        password_hash = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt()).decode('utf-8')

        try:
            conn = get_conn()
            with conn.cursor() as cur:
                cur.execute('SELECT id FROM users WHERE email=%s', (email,))
                if cur.fetchone():
                    return jsonify({'error': 'Email already registered'}), 400
                cur.execute('''INSERT INTO users (name, email, password_hash, gender, department, year, connection_type)
                            VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING id''',
                            (data['name'], email, password_hash, data['gender'], data['department'], data['year'], data['connection_type']))
                user_id = cur.fetchone()[0]
                # Insert interests
                for interest in data['interests']:
                    cur.execute('SELECT id FROM interests WHERE name=%s', (interest,))
                    res = cur.fetchone()
                    if res:
                        interest_id = res[0]
                    else:
                        cur.execute('INSERT INTO interests (name) VALUES (%s) RETURNING id', (interest,))
                        interest_id = cur.fetchone()[0]
                    cur.execute('INSERT INTO user_interests (user_id, interest_id) VALUES (%s, %s) ON CONFLICT DO NOTHING', (user_id, interest_id))
                # Insert skills
                for skill in data['skills']:
                    cur.execute('SELECT id FROM skills WHERE name=%s', (skill,))
                    res = cur.fetchone()
                    if res:
                        skill_id = res[0]
                    else:
                        cur.execute('INSERT INTO skills (name) VALUES (%s) RETURNING id', (skill,))
                        skill_id = cur.fetchone()[0]
                    cur.execute('INSERT INTO user_skills (user_id, skill_id) VALUES (%s, %s) ON CONFLICT DO NOTHING', (user_id, skill_id))
                # Insert learning goals
                for goal in data['learning_goals']:
                    cur.execute('SELECT id FROM learning_goals WHERE name=%s', (goal,))
                    res = cur.fetchone()
                    if res:
                        goal_id = res[0]
                    else:
                        cur.execute('INSERT INTO learning_goals (name) VALUES (%s) RETURNING id', (goal,))
                        goal_id = cur.fetchone()[0]
                    cur.execute('INSERT INTO user_learning_goals (user_id, learning_goal_id) VALUES (%s, %s) ON CONFLICT DO NOTHING', (user_id, goal_id))
            conn.commit()
            return jsonify({'message': 'Signup successful'}), 201
        except Exception as e:
            if conn: conn.rollback()
            return jsonify({'error': str(e)}), 500
        finally:
            if conn: conn.close()

@bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400
    try:
        conn = get_conn()
        with conn.cursor() as cur:
            cur.execute('SELECT id, password_hash FROM users WHERE email=%s', (email,))
            row = cur.fetchone()
            if not row:
                return jsonify({'error': 'Invalid credentials'}), 401
            user_id, password_hash = row
            if not bcrypt.checkpw(password.encode(), password_hash.encode('utf-8')):
                return jsonify({'error': 'Invalid credentials'}), 401
            # Create JWT token
            payload = {
                'user_id': user_id,
                'exp': datetime.now() + timedelta(days=1)
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
            return jsonify({'token': token, 'user_id': user_id}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn: conn.close()
