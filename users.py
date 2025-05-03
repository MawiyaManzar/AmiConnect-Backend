import os
import psycopg2
from flask import Blueprint, request, jsonify
from auth_utils import jwt_required  
from dotenv import load_dotenv

load_dotenv()

bp = Blueprint('users', __name__)
DB_URL = os.getenv('DATABASE_URL')

def get_conn():
    return psycopg2.connect(DB_URL)

@bp.route('/users', methods=['GET'])
@jwt_required
def get_users():
    department = request.args.get('department')
    year = request.args.get('year')
    query = '''SELECT u.id, u.name, u.email, u.gender, u.department, u.year, u.connection_type, u.created_at
               FROM users u'''
    filters = []
    params = []
    if department:
        filters.append('u.department=%s')
        params.append(department)
    if year:
        filters.append('u.year=%s')
        params.append(year)
    if filters:
        query += ' WHERE ' + ' AND '.join(filters)
    query += ' ORDER BY u.created_at DESC'
    try:
        conn = get_conn()
        with conn.cursor() as cur:
            cur.execute(query, tuple(params))
            users = [
                {
                    'id': row[0],
                    'name': row[1],
                    'email': row[2],
                    'gender': row[3],
                    'department': row[4],
                    'year': row[5],
                    'connection_type': row[6],
                    'created_at': row[7].isoformat() if row[7] else None
                }
                for row in cur.fetchall()
            ]
        return jsonify(users), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn: conn.close()

@bp.route('/users/<int:user_id>', methods=['GET'])
@jwt_required
def get_user(user_id):
    try:
        conn = get_conn()
        with conn.cursor() as cur:
            cur.execute('''
                SELECT id, name, email, gender, department, year, connection_type, created_at
                FROM users
                WHERE id = %s
            ''', (user_id,))
            user = cur.fetchone()
            if not user:
                return jsonify({'error': 'User not found'}), 404
            return jsonify({
                'id': user[0],
                'name': user[1],
                'email': user[2],
                'gender': user[3],
                'department': user[4],
                'year': user[5],
                'connection_type': user[6],
                'created_at': user[7].isoformat() if user[7] else None
            }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn: conn.close()
