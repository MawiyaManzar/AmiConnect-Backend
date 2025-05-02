import os
import tempfile
import pytest
import json
from flask import Flask
from app import app as flask_app
from auth import bp as auth_bp
from users import bp as users_bp
from recommend import bp as recommend_bp

@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()
    flask_app.config['TESTING'] = True
    flask_app.config['WTF_CSRF_ENABLED'] = False
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
    client = flask_app.test_client()
    yield client
    os.close(db_fd)
    os.unlink(db_path)

def test_signup_success(client):
    data = {
        "name": "Test User",
        "email": "testuser@s.amity.edu",
        "password": "TestPassword123!",
        "gender": "Male",
        "department": "BTech",
        "year": 1,
        "connection_type": "Study Partner",
        "interests": ["Web Development (Frontend)", "Data Science"],
        "skills": ["Python", "JavaScript"],
        "learning_goals": ["Machine Learning"]
    }
    response = client.post("/signup", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 201
    assert response.json["message"] == "Signup successful"

def test_signup_invalid_email(client):
    data = {
        "name": "Test User",
        "email": "notamity@gmail.com",
        "password": "TestPassword123!",
        "gender": "Male",
        "department": "BTech",
        "year": 1,
        "connection_type": "Study Partner",
        "interests": ["Web Development (Frontend)"],
        "skills": ["Python"],
        "learning_goals": ["Machine Learning"]
    }
    response = client.post("/signup", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 400
    assert "Invalid Amity email format" in response.json["error"]

def test_signup_duplicate_email(client):
    data = {
        "name": "Test User",
        "email": "testuser@s.amity.edu",
        "password": "TestPassword123!",
        "gender": "Male",
        "department": "BTech",
        "year": 1,
        "connection_type": "Study Partner",
        "interests": ["Web Development (Frontend)"],
        "skills": ["Python"],
        "learning_goals": ["Machine Learning"]
    }
    client.post("/signup", data=json.dumps(data), content_type="application/json")
    response = client.post("/signup", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 400
    assert "Email already registered" in response.json["error"]

def test_login_success(client):
    signup_data = {
        "name": "Test User",
        "email": "testlogin@s.amity.edu",
        "password": "TestPassword123!",
        "gender": "Male",
        "department": "BTech",
        "year": 1,
        "connection_type": "Study Partner",
        "interests": ["Web Development (Frontend)"],
        "skills": ["Python"],
        "learning_goals": ["Machine Learning"]
    }
    client.post("/signup", data=json.dumps(signup_data), content_type="application/json")
    login_data = {"email": "testlogin@s.amity.edu", "password": "TestPassword123!"}
    response = client.post("/login", data=json.dumps(login_data), content_type="application/json")
    assert response.status_code == 200
    assert "token" in response.json
    assert "user_id" in response.json

def test_login_invalid_credentials(client):
    login_data = {"email": "doesnotexist@s.amity.edu", "password": "wrongpass"}
    response = client.post("/login", data=json.dumps(login_data), content_type="application/json")
    assert response.status_code == 401
    assert "Invalid credentials" in response.json["error"]

def test_users_endpoint_requires_auth(client):
    response = client.get("/users")
    assert response.status_code == 401 or response.status_code == 403

def test_users_endpoint_success(client):
    signup_data = {
        "name": "Test User",
        "email": "testusers@s.amity.edu",
        "password": "TestPassword123!",
        "gender": "Male",
        "department": "BTech",
        "year": 1,
        "connection_type": "Study Partner",
        "interests": ["Web Development (Frontend)"],
        "skills": ["Python"],
        "learning_goals": ["Machine Learning"]
    }
    client.post("/signup", data=json.dumps(signup_data), content_type="application/json")
    login_data = {"email": "testusers@s.amity.edu", "password": "TestPassword123!"}
    login_resp = client.post("/login", data=json.dumps(login_data), content_type="application/json")
    token = login_resp.json["token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/users", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_recommend_endpoint_requires_auth(client):
    response = client.get("/recommend/1")
    assert response.status_code == 401 or response.status_code == 403
