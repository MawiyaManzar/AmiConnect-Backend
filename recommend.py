import os
import psycopg2
from flask import Blueprint, jsonify
from auth_utils import jwt_required  # Import from auth_utils
from dotenv import load_dotenv

load_dotenv()

bp = Blueprint('recommend', __name__)
DB_URL = os.getenv('DATABASE_URL')

# Helper to get DB connection
def get_conn():
    return psycopg2.connect(DB_URL)

def fetch_user_profile(cur, user_id):
    cur.execute('''SELECT id, name, department, year, connection_type FROM users WHERE id=%s''', (user_id,))
    user = cur.fetchone()
    if not user:
        return None
    cur.execute('SELECT i.name FROM interests i JOIN user_interests ui ON i.id=ui.interest_id WHERE ui.user_id=%s', (user_id,))
    interests = set(r[0] for r in cur.fetchall())
    cur.execute('SELECT s.name FROM skills s JOIN user_skills us ON s.id=us.skill_id WHERE us.user_id=%s', (user_id,))
    skills = set(r[0] for r in cur.fetchall())
    cur.execute('SELECT l.name FROM learning_goals l JOIN user_learning_goals ul ON l.id=ul.learning_goal_id WHERE ul.user_id=%s', (user_id,))
    learning_goals = set(r[0] for r in cur.fetchall())
    return {
        'id': user[0],
        'name': user[1],
        'department': user[2],
        'year': user[3],
        'connection_type': user[4],
        'interests': interests,
        'skills': skills,
        'learning_goals': learning_goals
    }

def similarity_score(user, other):
    score = 0
    # Common interests: +30 per match
    score += 30 * len(user['interests'] & other['interests'])
    # Skill-Learning Goal match: +20 per match (A's skill in B's learning goal or vice versa)
    skill_goal_matches = (user['skills'] & other['learning_goals']) | (other['skills'] & user['learning_goals'])
    score += 20 * len(skill_goal_matches)
    # Same department: +15
    if user['department'] == other['department']:
        score += 15
    # Same year: +10
    if user['year'] == other['year']:
        score += 10
    return score

@bp.route('/recommend/<int:user_id>', methods=['GET'])
@jwt_required
def recommend(user_id):
    try:
        conn = get_conn()
        with conn.cursor() as cur:
            user = fetch_user_profile(cur, user_id)
            if not user:
                return jsonify({'error': 'User not found'}), 404
            # Fetch all other users
            cur.execute('SELECT id FROM users WHERE id != %s', (user_id,))
            others = [r[0] for r in cur.fetchall()]
            recommendations = []
            for oid in others:
                other = fetch_user_profile(cur, oid)
                if not other:
                    continue
                score = similarity_score(user, other)
                recommendations.append({
                    'id': other['id'],
                    'name': other['name'],
                    'department': other['department'],
                    'year': other['year'],
                    'connection_type': other['connection_type'],
                    'score': score,
                    'interests': list(other['interests']),
                    'skills': list(other['skills']),
                    'learning_goals': list(other['learning_goals'])
                })
            # Sort by score descending, take top 5-10
            recommendations = sorted(recommendations, key=lambda x: x['score'], reverse=True)[:10]
            return jsonify({'recommendations': recommendations}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn: conn.close()
